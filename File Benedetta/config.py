"""
config.py  —  configurazione della pulizia dei file ADNI.

A COSA SERVE
    Sostituisce il vecchio file Excel ADNI_variables_statistics.xlsx.
    Contiene solo DECISIONI e DATI (cosa tenere, come rinominare, quali soglie),
    mai LOGICA. La logica sta tutta in pipeline.py.

    Regola per capire dove va una cosa:
        e' una DECISIONE o un DATO?  -> qui (o in un file JSON esterno)
        e' un CALCOLO?               -> pipeline.py, e non si scrive a mano

    Corrispondenza col vecchio mondo:
        parameter                    -> catalog.json: domain   (gruppo della variabile)
        orig_variable_code -> code   -> catalog.json: chiave = nome standard, aliases = grezzi
        Unit                         -> catalog.json: unit (UCUM)
        metadati_fattori/norm        -> catalog.json: role
        soglie a mano nelle celle    -> POLICY + campi di DatasetConfig
"""
from __future__ import annotations
from dataclasses import dataclass, field, fields
from pathlib import Path
from typing import Optional
import json
import numpy as np

_HERE = Path(__file__).parent


# ---------------------------------------------------------------------------
# 1. POLICY  —  regole globali (prima erano numeri sparsi dentro le celle)
# ---------------------------------------------------------------------------
# [D027] Segnaposto di "dato mancante", in due livelli:
#  - MISSING_STRINGS: testi che sono SEMPRE un mancante, in ogni file e colonna;
#  - codici NUMERICI: sono un mancante solo in certi file. In ADNIMERGE, per esempio,
#    -4 e -1 sono valori VERI di RAVLT_learning/forgetting (differenze di punteggio):
#    trattarli come mancanti cancellava dati validi. Per questo i codici numerici si
#    dichiarano per file (DatasetConfig.missing_codes); senza dichiarazione vale il default,
#    cioe' il comportamento di prima.
MISSING_STRINGS = ["Unknown", "unknown", "NA", "N/A"]
DEFAULT_MISSING_CODES = ["-4", -4, 9999, 9999.0]
CENSORED_PREFIXES = (">", "<")          # biomarcatori CSF: ">1700", "<200"

# Soglia usata SOLO dal report profile(): etichetta 'keep'/'drop', NON cancella nulla.
MISSING_KEEP_THRESHOLD = 0.65
# Soglia usata dall'AZIONE distruttiva di cleaning 2 (drop_sparse_columns):
# quota minima di validi per TENERE davvero una colonna. Volutamente separata
# dalla precedente: una e' un'etichetta nel report, l'altra cancella dati.
SPARSE_KEEP_THRESHOLD = 0.65
# Soggetti con >1 visita sotto i quali il file e' trattato come 'single visit'
# (ex soglia hardcoded nel notebook cleaning2).  [spostata qui dalla riga di Rossana]
MULTIVISIT_MIN_SUBJECTS = 10

# [D029] Date note solo come mese/anno (es. PTDOB "07/1940"): giorno imputato a META' mese,
# cosi' l'errore sull'eta' e' centrato (max ±15 giorni) invece che sempre in eccesso.
# Si applica SOLO alle variabili con date_precision='month' nel catalogo e SOLO ai valori
# scritti come MM/YYYY: le date complete non vengono toccate.
DOB_IMPUTED_DAY = 15
# [D030] Decimali dell'eta' calcolata (notes_CP B.4).
AGE_ROUND_DECIMALS = 1
# [D019] Controllo di coerenza: se una variabile e' presa dal file (misurata) ma si potrebbe
# anche calcolare, si confrontano i due valori; oltre questa differenza la riga va a log.
# AGE: ±0,5 anni (6 mesi). Variabili non elencate: nessun controllo.
DERIVED_CHECK_TOLERANCE = {"AGE": 0.5}


# ---------------------------------------------------------------------------
# 2. cutoffs.json  —  caricato SOLO se serve (dataset con compute_atn=True).
#    ADNIMERGE non calcola l'ATN, quindi per ADNIMERGE questo file NON serve
#    e non viene nemmeno letto. Serve solo ai file CSF (UPENNBIOMK...).
# ---------------------------------------------------------------------------
_CUTOFFS = None


def cutoff(var: str, method: str = "unknown", path: str = "cutoffs.json"):
    """Legge cutoffs.json alla prima chiamata. Se manca -> errore esplicito."""
    global _CUTOFFS
    if _CUTOFFS is None:
        p = _HERE / path
        if not p.exists():
            raise FileNotFoundError(
                f"'{path}' non trovato in {_HERE}. Serve solo ai dataset con "
                f"compute_atn=True; ADNIMERGE non lo richiede."
            )
        _CUTOFFS = json.loads(p.read_text())
    entry = _CUTOFFS.get(var)
    return entry.get(method, entry.get("unknown")) if isinstance(entry, dict) else entry


# Assi ATN di default (caso CSF): quale marcatore e in che verso definisce A / T / N.
# 'below' = positivo quando il valore e' SOTTO la soglia (es. Abeta42 basso = amiloide+).
# Per plasma/PET si passa un atn_axes diverso nel DatasetConfig (i marcatori cambiano).
ATN_AXES_CSF = {
    "A": ("AB42_CSF",  "below"),
    "T": ("PT181_CSF", "above"),
    "N": ("TTAU_CSF",  "above"),
}


# ---------------------------------------------------------------------------
# 2b. ranges.json  —  range di validita' [min, max, direzione] per colonna,
#     in tre sezioni: 'normalization' (scale/biomarcatori, alcuni per-metodo),
#     'volume' (volumi e %ICV), 'cofattori' (es. APOE_4).
#     A differenza di cutoffs.json NON trasformano i dati: nel vecchio codice
#     (automated_merge.py) arricchiscono i METADATI dei file mergiati. Sono dati
#     tabulari, quindi restano un FILE letto dal config, non dict dentro il .py.
#     [accorpa i vecchi normalization_settings/volume_values/cofattori_values.json]
# ---------------------------------------------------------------------------
RANGES_FILE = "ranges.json"
SETTINGS_SECTIONS = ("normalization", "volume", "cofattori")
_RANGES_CACHE = None


def load_settings(name: str) -> dict:
    """Restituisce una sezione di ranges.json ('normalization'|'volume'|'cofattori').
    Legge il file una volta sola. Se manca -> {} (serve al merge, non blocca il cleaning)."""
    global _RANGES_CACHE
    if _RANGES_CACHE is None:
        p = _HERE / RANGES_FILE
        _RANGES_CACHE = json.loads(p.read_text()) if p.exists() else {}
    return _RANGES_CACHE.get(name, {})


def column_ranges(columns, name: str, method: str = None) -> dict:
    """Per le colonne PRESENTI, restituisce {col: [min, max, direzione]}, risolvendo
    il metodo per le voci annidate per-assay. E' il cuore riusabile dei filter_*
    di automated_merge, ma config-driven e in un posto solo."""
    s = load_settings(name)
    out = {}
    for col in columns:
        v = s.get(col)
        if v is None:
            continue
        if isinstance(v, list):
            out[col] = v
        elif isinstance(v, dict):
            if method and method.lower() in v:
                out[col] = v[method.lower()]
            elif "unknown" in v:
                out[col] = v["unknown"]
    return out


# ---------------------------------------------------------------------------
# 3. RECODE  —  stringhe categoriche -> codici (ex funzioni categorize_*).
#    Le classi sono lette da ADNIMERGE; i codici seguono la convenzione del
#    notebook (README 5.1), non una nuova.
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# 3. RECODE  —  categorie -> ETICHETTE STANDARD (stringhe), non numeri.
#    [nota Chiara #3] mappare a stringhe standard rende le dummy leggibili
#    (DX_CN, GENDER_male) e non costringe a ri-convertire in numeri dopo.
#    Chiavi = NOMI STANDARD (il recode gira DOPO il rename, vedi nota #4).
# ---------------------------------------------------------------------------
def _codes(mapping: dict) -> dict:
    """Codici numerici di un file (es. PTDEMOG): ogni codice vale sia come numero sia come
    testo (1 e "1"), perche' la stessa colonna puo' essere letta come float o come stringa."""
    out = {}
    for code, label in mapping.items():
        out[code] = label
        out[str(code)] = label
    return out


# RECODE per SORGENTE [D018]: {file_code | "*": {variabile standard: {grezzo: etichetta}}}.
# "*" vale per tutti i file; la mappa del file specifico si aggiunge sopra (e vince).
# Le etichette di arrivo sono i 'levels' del catalogo (che danno anche il codice numerico).
RECODE = {
    "*": {                                       # stringhe come in ADNIMERGE
        "GENDER":    {"Male": "male", "Female": "female"},
        "MARRY":     {"Married": "married", "Divorced": "divorced", "Widowed": "widowed",
                      "Never married": "never_married", "Unknown": np.nan},
        "ETHNICITY": {"Hisp/Latino": "hisp", "Not Hisp/Latino": "not_hisp", "Unknown": np.nan},
        "RACE":      {"White": "white", "Black": "black", "Asian": "asian",
                      "Am Indian/Alaskan": "amind", "Hawaiian/Other PI": "hawaiian",
                      "More than one": "mixed", "Unknown": np.nan},
        "DX":        {"CN": "CN", "MCI": "MCI", "Dementia": "Dementia"},
    },
    "PTDEMOG": {                                 # codici numerici, dalla collega [D031]
        "GENDER":    _codes({1: "male", 2: "female"}),
        "MARRY":     _codes({1: "married", 2: "widowed", 3: "divorced", 4: "never_married",
                             5: np.nan, 6: "married"}),
        "ETHNICITY": _codes({1: "hisp", 2: "not_hisp", 3: np.nan}),
        "RACE":      {**_codes({1: "amind", 2: "asian", 3: "hawaiian", 4: "black", 5: "white",
                                6: "mixed", 7: np.nan, 8: "hawaiian", 9: "hawaiian"}),
                      "/": "mixed"},
    },
}

# Valori multipli in una sola cella (es. RACE "1|5" in PTDEMOG = piu' razze): se il valore
# contiene il separatore, diventa l'etichetta indicata. [D031]
RECODE_MULTI = {"RACE": ("|", "mixed")}


def recode_map(var: str, file_code: Optional[str] = None) -> dict:
    """Mappa grezzo -> etichetta per una variabile: quella generica ("*") + quella del file."""
    return {**RECODE["*"].get(var, {}), **RECODE.get(file_code, {}).get(var, {})}


# ---------------------------------------------------------------------------
# 4. CATALOGO  —  catalog.json, unica fonte di verita' sulle variabili [D006, D018].
#    Chiave = nome standard. Ogni voce dice COSA e' la variabile (definizione, unita',
#    ruolo, ciclo di vita, codici standard) e DA DOVE viene:
#      - aliases: colonne grezze 'DATASET:FILE.colonna' (FILE='*' = tutti i file);
#      - derived: come si calcola, lista di modi di calcolo in ordine di preferenza.
#    E' un DATO, quindi sta in un file JSON letto qui (come cutoffs/ranges), non nel .py.
#    Caricato alla prima richiesta e validato: un errore nel JSON ferma tutto con un
#    messaggio chiaro invece di produrre un rename sbagliato in silenzio.
# ---------------------------------------------------------------------------
CATALOG_FILE = "catalog.json"
SCOPES = ("cleaning", "merge", "output")        # [D032] fin dove vive la variabile


@dataclass(frozen=True)
class Var:
    domain: str                                  # ID, Visit, Demographic, Cognitive, Imaging, Biomarker...
    definition: str
    unit: Optional[str] = None                   # notazione UCUM (a = anni, mm3, pg/mL, {score})
    role: Optional[str] = None                   # predittore | normalizzazione | metodo | qualita | ...
    scope: str = "output"                        # cleaning | merge | output  [D032]
    dtype: Optional[str] = None                  # 'date' -> convertita da parse_dates
    date_precision: Optional[str] = None         # 'month' -> valori MM/YYYY, giorno imputato [D029]
    aliases: tuple = ()                          # 'DATASET:FILE.colonna'  [D017]
    derived: tuple = ()                          # ({"from": [...], "by": "..."}, ...)  [D019]
    levels: Optional[dict] = None                # categoriche: {"etichetta": codice_intero}
    method_col: Optional[str] = None             # colonna con il metodo di misura della riga
    omop_concept_id: Optional[int] = None        # codici standard: SOLO se verificati [passo 6]
    vocab_code: Optional[str] = None
    admapper_ref: Optional[str] = None
    standard_match: str = "none"                 # exact | broader | approximate | none
    note: str = ""
    log_ref: tuple = ()                          # ID in DECISIONI.md


def parse_alias(alias: str) -> tuple[str, str, str]:
    """'ADNI:ADNIMERGE.ABETA' -> ('ADNI', 'ADNIMERGE', 'ABETA'); il nome nudo 'X' vale '*:*.X'."""
    if ":" not in alias:
        return "*", "*", alias
    dataset, rest = alias.split(":", 1)
    if "." not in rest:
        raise ValueError(f"alias '{alias}': formato atteso DATASET:FILE.colonna")
    file_code, column = rest.split(".", 1)
    return dataset, file_code, column


def alias_level(key) -> int:
    """0 = file preciso, 1 = tutti i file del dataset, 2 = tutti i dataset (vince il piu' basso)."""
    dataset, file_code, _ = key
    return 2 if dataset == "*" else 1 if file_code == "*" else 0


_CATALOG = None
_ALIASES = None                                  # {(dataset, file, colonna): nome standard}


def load_catalog(path=None) -> dict[str, Var]:
    """Legge catalog.json e lo valida. Errore esplicito se: campo sconosciuto, scope non valido,
    voce senza aliases ne' derived, alias malformato, stesso alias per due variabili."""
    p = Path(path) if path else _HERE / CATALOG_FILE
    if not p.exists():
        raise FileNotFoundError(f"'{p.name}' non trovato in {p.parent}: e' il catalogo delle variabili.")
    raw = json.loads(p.read_text(encoding="utf-8"))
    allowed = {f.name for f in fields(Var)}
    catalog, seen, errors = {}, {}, []
    for name, attrs in raw.items():
        if name.startswith("_"):                 # _templates, _istruzioni: ignorati
            continue
        unknown = set(attrs) - allowed
        if unknown:
            errors.append(f"{name}: campi non previsti {sorted(unknown)}")
            continue
        attrs = dict(attrs)
        attrs["aliases"] = tuple(attrs.get("aliases") or ())
        attrs["derived"] = tuple(attrs.get("derived") or ())
        attrs["log_ref"] = tuple(attrs.get("log_ref") or ())
        if not attrs["aliases"] and not attrs["derived"]:
            errors.append(f"{name}: serve almeno uno tra 'aliases' e 'derived'")
        if attrs.get("scope", "output") not in SCOPES:
            errors.append(f"{name}: scope '{attrs.get('scope')}' non valido {SCOPES}")
        for alias in attrs["aliases"]:
            try:
                key = parse_alias(alias)
            except ValueError as e:
                errors.append(f"{name}: {e}")
                continue
            if key in seen and seen[key] != name:
                errors.append(f"alias '{alias}' assegnato sia a '{seen[key]}' sia a '{name}'")
            seen[key] = name
        try:
            catalog[name] = Var(**attrs)
        except TypeError as e:
            errors.append(f"{name}: {e}")
    if errors:
        raise ValueError(f"{p.name} non valido:\n  " + "\n  ".join(errors))
    return catalog


def catalog() -> dict[str, Var]:
    """Il catalogo (letto e validato alla prima chiamata, poi in cache)."""
    global _CATALOG, _ALIASES
    if _CATALOG is None:
        _CATALOG = load_catalog()
        _ALIASES = {parse_alias(a): name for name, v in _CATALOG.items() for a in v.aliases}
    return _CATALOG


def rename_map_for(dataset: str, file_code: Optional[str] = None,
                   keep_identity: bool = False) -> dict[str, str]:
    """Mappa grezzo -> standard per un file, con la precedenza [D017]:
    tutti i dataset (*:*) < tutto il dataset (DATASET:*) < file preciso (DATASET:FILE).
    Con file_code=None restituisce solo i livelli generici; keep_identity=True tiene anche
    le voci grezzo == standard (servono al generatore di bozze per riconoscere le colonne)."""
    catalog()
    out = {}
    for level in (2, 1, 0):                      # dal piu' generico al piu' specifico: vince l'ultimo
        for (ds, fc, col), std in _ALIASES.items():
            if alias_level((ds, fc, col)) != level:
                continue
            if ds not in ("*", dataset) or (level == 0 and fc != file_code):
                continue
            out[col] = std
    return out if keep_identity else {raw: std for raw, std in out.items() if raw != std}


def alias_overrides() -> list[tuple]:
    """Colonne rivendicate da variabili diverse a livelli diversi (lecito: vince il piu'
    specifico). Restituisce [(colonna, [(alias, variabile), ...])] per il controllo umano."""
    catalog()
    by_col = {}
    for key, std in _ALIASES.items():
        by_col.setdefault(key[2], []).append((key, std))
    out = []
    for col, items in by_col.items():
        if len({std for _, std in items}) > 1:
            out.append((col, [(f"{k[0]}:{k[1]}.{k[2]}", s) for k, s in sorted(items, key=lambda x: alias_level(x[0]))]))
    return out


def derived_vars() -> dict[str, Var]:
    """Variabili calcolate (hanno almeno un modo di calcolo in 'derived')."""
    return {n: v for n, v in catalog().items() if v.derived}


def date_vars() -> dict[str, Var]:
    """Variabili di tipo data (dtype='date')."""
    return {n: v for n, v in catalog().items() if v.dtype == "date"}


def scope_vars(scope: str) -> list[str]:
    """Nomi standard con un certo ciclo di vita [D032]."""
    return [n for n, v in catalog().items() if v.scope == scope]


def encode(series, var: str):
    """Etichetta standard -> codice intero secondo i 'levels' del catalogo (Int64, NaN ammessi)."""
    levels = catalog()[var].levels or {}
    return series.map(levels).astype("Int64")


def decode(series, var: str):
    """Codice intero -> etichetta standard (inverso di encode)."""
    inverse = {code: label for label, code in (catalog()[var].levels or {}).items()}
    return series.map(inverse)


# ---------------------------------------------------------------------------
# 5. DATASET  —  la "scheda d'identita'" del file, fedele al blocco ADNIMERGE
#    di adni_cleaning1.ipynb (celle 222-224) + il blocco cleaning 2/3.
# ---------------------------------------------------------------------------
@dataclass
class DatasetConfig:
    file_code: str                      # = FILE negli alias 'DATASET:FILE.colonna' del catalogo
    source: str
    dataset: str = "ADNI"               # = DATASET negli alias [D017]
    id_column: str = "RID"
    date_column: str = "EXAMDATE"
    viscode_reference: Optional[str] = "VISCODE"
    cohort_column: str = "COLPROT"

    # --- identita' per il merge ---
    category: Optional[str] = None      # 'plasma'|'csf'|'pet'|'volumes'|'scale'|'cofactor'

    # --- cleaning 1 ---
    # [D016] colonne GREZZE tolte appena caricato il file, prima del rename: es. VISCODE nei
    # file che hanno anche VISCODE2 (che viene rinominata VISCODE).
    drop_columns: list[str] = field(default_factory=list)
    # [D028] righe scartate per valore, NOMI STANDARD (dopo il rename): es. screen fail
    # {"VISCODE": ["f"]}.
    drop_rows: dict[str, list] = field(default_factory=dict)
    # [D027] codici numerici di "mancante" di questo file; None -> config.DEFAULT_MISSING_CODES.
    missing_codes: Optional[list] = None
    # (le date da convertire e la precisione mese/anno ora vengono dal catalogo:
    #  dtype='date', date_precision='month' [D029])
    # [nota Chiara #1] scarta la riga se MANCA anche UNA sola di queste (any-none),
    # es. ID o data: e' diverso da essential_columns (che scarta se TUTTE mancano).
    required_all_present: list[str] = field(default_factory=list)
    essential_columns: list[str] = field(default_factory=list)   # tieni riga se >=1 valorizzata (NOMI STANDARD)
    also_required: list[str] = field(default_factory=list)       # 2° filtro (AND): richiedi questa (NOMI STANDARD)
    recode_columns: list[str] = field(default_factory=list)      # colonne da passare a RECODE (NOMI STANDARD)
    # (il rename per-file e' ora un alias 'ADNI:<file_code>.<colonna>' in catalog.json [D017];
    #  i rapporti e l'eta' sono variabili 'derived' del catalogo, calcolate quando servono [D019])
    # colonne di metodo della riga, riempite con un valore per tutto il file [D020]
    # es. {"METHOD_PLASMA": "simoa"}
    constant_columns: dict[str, str] = field(default_factory=dict)
    decensor_biomarkers: bool = False   # ">1700"/"<200" -> numerico (file CSF/plasma)
    decensor_columns: list[str] = field(default_factory=list)     # NOMI STANDARD (decensor gira post-rename)
    clean_fs_fields: bool = False       # FLDSTRENG/FSVERSION: estrai parte numerica
    compute_atn: bool = False           # rapporti + profilo ATN (solo file CSF)
    atn_method: str = "unknown"
    atn_axes: Optional[dict] = None     # {asse: (marcatore, 'below'|'above')}; None -> ATN_AXES_CSF

    # --- cleaning 2 / 3  (le decisioni che Rossana aveva scritto a mano) -------
    drop_sparse_columns: bool = False           # scarta colonne sotto SPARSE_KEEP_THRESHOLD
    make_dummies: bool = False                  # one-hot delle categoriche
    dummy_columns: list[str] = field(default_factory=list)      # ex REF_LIST
    remove_single_visit: bool = False           # scarta soggetti con 1 sola visita
    keep_even_single_visit: bool = False        # eccezione (file anagrafici/genetici: PTDEMOG/APOERES)
    volume_row_keys: list[str] = field(default_factory=list)    # scarta riga se TUTTE queste sono NaN
    normalize_icv: bool = False                 # volumi -> % di ICV
    icv_column: str = "ICV"
    keep_columns: list[str] = field(default_factory=list)       # whitelist finale (NOMI STANDARD, post-rename)

    # --- output (decisioni, non calcoli) --------------------------------------
    output_cleaned1: Optional[str] = None
    output_cleaned2: Optional[str] = None
    report_file: Optional[str] = None
    runlog_file: Optional[str] = None           # [D015] log di esecuzione (contiene RID: resta locale)

    def __post_init__(self):
        # i nomi di output derivano da file_code se non specificati a mano
        if self.output_cleaned1 is None:
            self.output_cleaned1 = f"{self.file_code}_cleaned_01.csv"
        if self.output_cleaned2 is None:
            self.output_cleaned2 = f"{self.file_code}_cleaned_02.csv"
        if self.report_file is None:
            self.report_file = f"{self.file_code}_report.csv"
        if self.runlog_file is None:
            self.runlog_file = f"{self.file_code}_runlog.json"

    def effective_rename(self) -> dict[str, str]:
        """Mappa grezzo -> standard per questo file, dagli alias del catalogo [D017]:
        *:* < DATASET:* < DATASET:<file_code> (il piu' specifico vince)."""
        return rename_map_for(self.dataset, self.file_code)


ADNIMERGE = DatasetConfig(
    file_code="ADNIMERGE",
    source="ADNIMERGE_05Mar2026.csv",          # SEMPRE il file grezzo: cleaning1 legge il raw
    viscode_reference="VISCODE",

    # cleaning 1 -----------------------------------------------------------
    # [D027] tabella gia' derivata, usa NA veri: nessun codice numerico di mancante.
    # (-4/-1 in RAVLT_learning/forgetting sono differenze di punteggio vere)
    missing_codes=[],
    required_all_present=["RID"],              # [#1] scarta la riga se manca l'ID
    # AGE grezza di ADNIMERGE e' l'eta' al baseline: dopo il rename si chiama AGE_bl [D019]
    essential_columns=["APOE4", "MMSE", "Ventricles", "Hippocampus", "AGE_bl"],
    also_required=["DX"],
    recode_columns=["GENDER", "MARRY", "ETHNICITY", "RACE", "DX"],   # NOMI STANDARD (rename-first)
    clean_fs_fields=True,
    # compute_atn resta False: nel notebook l'ATN e' solo per i file CSF, non ADNIMERGE

    # cleaning 2 / 3 -------------------------------------------------------
    drop_sparse_columns=True,                  # come faceva Rossana (remove_param_few_subjects)
    # [D026] dummy DOPO il merge: prima del merge una sola colonna categorica (stringa)
    # rende semplice il controllo di coerenza tra file. La funzione resta per il post-merge.
    make_dummies=False,
    dummy_columns=["GENDER", "MARRY", "ETHNICITY", "RACE", "DX"],   # nomi STANDARD, post-rename
    # [nota Chiara #9] niente drop-righe-per-volumi qui: rischia di buttare righe con
    # altri dati utili. Va fatto DOPO il merge (scarta se manca ogni valore vol/PET/CSF).
    # volume_row_keys=[...]  -> rimosso dal cleaning per singolo file.

    # --- DUE decisioni lasciate a te (vedi documento per Rossana, §"manca qualcosa"):
    #     stanno nella "base" documentata (cleaning2/cleaning3) ma cambiano i numeri,
    #     quindi le lascio OFF e le decidi tu. Sono gia' implementate in pipeline.py.
    remove_single_visit=False,                 # -> True per riprodurre cleaning2 (scarta soggetti 1 visita)
    normalize_icv=False,                       # -> True per riprodurre cleaning3 (volumi come % di ICV)

    # whitelist finale (le "colonne di Chiara"), in NOMI STANDARD post-rename.
    # Le dummy generate e le colonne calcolate (VISIT_MONTH, AGE_bl) vengono
    # tenute automaticamente dalla pipeline: NON si elencano qui a mano.
    keep_columns=[
        "RID", "COLPROT", "VISCODE", "EXAMDATE", "AGE", "AGE_bl",
        "GENDER", "MARRY", "ETHNICITY", "RACE", "DX",      # [D026] categoriche (non piu' dummy)
        "EDUCATION", "APOE4", "CDRSB", "ADAS11", "ADAS13", "MMSE",
        "RAVLT_immediate", "FAQ", "MOCA", "FLDSTRENG", "FSVERSION", "IMAGEUID",
        "Ventricles", "Hippocampus", "Entorhinal", "Fusiform", "MidTemp", "ICV",
        "update_stamp",
    ],
)


# ---------------------------------------------------------------------------
# 5b. Altri dataset — ESEMPIO: i tuoi due file plasma, descritti SOLO come config.
#     Nessuna funzione nuova, nessuna modifica al CATALOG globale.
# ---------------------------------------------------------------------------

# --- Plasma: TUTTE le misure usano i nomi canonici _PL (= chiavi di ranges/cutoffs),
#     e OGNI file ha un METODO distinto: sono le due condizioni perche' armonizzazione
#     e range funzionino. Stessa misura -> stesso nome; assay diverso -> etichetta diversa.

# ADx/VUMC — pannello NfL + Abeta42/40 + GFAP.
PLASMA_ADX_VUMC = DatasetConfig(
    file_code="PLASMA_ABETA_PROJECT_ADX_VUMC",
    source="PLASMA_ABETA_PROJECT_ADX_VUMC_11Aug2025.csv",
    category="plasma",
    date_column="EXAMDATE",
    essential_columns=["NFL_PL", "AB42_PL", "GFAP"],       # NOMI STANDARD (rename-first)
    # rename -> alias 'ADNI:<file_code>.<colonna>' in catalog.json [D017]
    # METODO: distinto da C2N. CONFERMA l'assay reale: se questo pannello e' il Simoa
    # 4-plex usa "simoa"/"quanterix" (ma allora e' lo STESSO metodo NfL di Blennow ->
    # non si armonizza, si concatena); "adx_vumc" e' un placeholder sicuro e distinto.
    constant_columns={"METHOD_PLASMA": "adx_vumc"},
    decensor_biomarkers=True,
    decensor_columns=["NFL_PL", "AB42_PL", "AB40_PL", "GFAP"],
    keep_columns=["RID", "VISCODE", "EXAMDATE",
                  "NFL_PL", "AB42_PL", "AB40_PL", "GFAP", "AB4240_PL",
                  "METHOD_PLASMA", "update_stamp"],
)

# Blennow — plasma NfL longitudinale (Simoa).
PLASMA_NFL = DatasetConfig(
    file_code="BLENNOWPLASMANFL",
    source="ADNI_BLENNOWPLASMANFLLONG_10_03_18_11Aug2025.csv",
    category="plasma",
    date_column="EXAMDATE",
    essential_columns=["NFL_PL"],                          # NOME STANDARD (rename-first)
    # rename -> alias 'ADNI:<file_code>.<colonna>' in catalog.json [D017]
    constant_columns={"METHOD_PLASMA": "simoa"},
    keep_columns=["RID", "VISCODE", "EXAMDATE", "NFL_PL", "METHOD_PLASMA", "update_stamp"],
)

# C2N PrecivityAD2 — spettrometria di massa: p-tau217, Abeta42/40, APS2.
PLASMA_C2N = DatasetConfig(
    file_code="C2N_PRECIVITYAD2_PLASMA",
    source="C2N_PRECIVITYAD2_PLASMA_11Aug2025.csv",
    category="plasma",
    date_column="EXAMDATE",
    essential_columns=["PT217_PL", "AB42_PL"],             # NOMI STANDARD (rename-first)
    # rename -> alias 'ADNI:<file_code>.<colonna>' in catalog.json [D017]
    constant_columns={"METHOD_PLASMA": "massospectrometry"},   # C2N = spettrometria di massa
    keep_columns=["RID", "VISCODE", "EXAMDATE",
                  "PT217_PL", "nPT217_PL", "AB42_PL", "AB40_PL",
                  "AB4240_PL", "PT217_nPT217_PL", "APS2", "APOE",
                  "METHOD_PLASMA", "update_stamp"],
)



# ---------------------------------------------------------------------------
# 5f. Dataset estratti da ADNI_variables_statistics.xlsx (keep/rename/metodo
#     dall'Excel di supporto). VERIFICA i rename biomarcatori e metti i source reali.
# ---------------------------------------------------------------------------

# ======================================================================
# ADAS   [categoria: scale]
#   dall'Excel: 7 keep, 0 drop
# ----------------------------------------------------------------------
ADAS = DatasetConfig(
    file_code="ADAS",
    source="ADAS_28Oct2025.csv",                 # <-- METTI il nome file reale
    category='scale',
    # rename -> alias 'ADNI:<file_code>.<colonna>' in catalog.json [D017]
    keep_columns=['COLPROT', 'RID', 'VISCODE2', 'VISDATE', 'TOTSCORE', 'TOTAL13', 'update_stamp'],
)

# ======================================================================
# ADNI_DIAN_COMPARISON   [categoria: volumes]
#   dall'Excel: 15 keep, 12 drop
#   collisioni risolte tenendo il grezzo (VERIFICA): [('CDRGLOB', 'CDRSB')]
# ----------------------------------------------------------------------
ADNI_DIAN_COMPARISON = DatasetConfig(
    file_code="ADNI_DIAN_COMPARISON",
    source="ADNI-DIAN_Comparison_Study_Data_Subset_05_23_22_23Oct2025.csv",                 # <-- METTI il nome file reale
    category='volumes',
    # rename -> alias 'ADNI:<file_code>.<colonna>' in catalog.json [D017]
    keep_columns=['RID', 'COLPROT', 'VISCODE2', 'EXAMDATE', 'AGE', 'GENDER', 'ETHNICITY', 'RACE', 'MARRY', 'APOE4', 'DIAN_GROUP', 'CDRSB', 'CDRGLOB', 'MMSE', 'update_stamp'],
)

# ======================================================================
# ADSP_PHC_BIOMARKER   [categoria: csf]
#   dall'Excel: 19 keep, 0 drop
#   collisioni risolte tenendo il grezzo (VERIFICA): [('PHC_Race', 'ETHNICITY'), ('PHC_AB42', 'AB42_CSF'), ('PHC_Tau', 'TTAU_CSF'), ('PHC_pTau', 'PT181_CSF')]
# ----------------------------------------------------------------------
ADSP_PHC_BIOMARKER = DatasetConfig(
    file_code="ADSP_PHC_BIOMARKER",
    source="ADSP_PHC_BIOMARKER_25Jul2025.csv",                 # <-- METTI il nome file reale
    category='csf',
    # rename -> alias 'ADNI:<file_code>.<colonna>' in catalog.json [D017]
    keep_columns=['RID', 'COLPROT', 'VISCODE2', 'DRAWDATE', 'EDUCATION', 'ETHNICITY', 'PHC_Race', 'GENDER', 'DX', 'AGE', 'AB42_CSF', 'PHC_AB42', 'TTAU_CSF', 'PHC_Tau', 'PT181_CSF', 'PHC_pTau', 'AT_class', 'Platform', 'update_stamp'],
)

# ======================================================================
# APOERES   [categoria: cofactor]
#   dall'Excel: 3 keep, 1 drop
# ----------------------------------------------------------------------
APOERES = DatasetConfig(
    file_code="APOERES",
    source="APOERES_11Aug2025.csv",                 # <-- METTI il nome file reale
    category='cofactor',
    # rename -> alias 'ADNI:<file_code>.<colonna>' in catalog.json [D017]
    keep_columns=['COLPROT', 'RID', 'APOE4'],
)

# ======================================================================
# CDR   [categoria: scale]
#   dall'Excel: 7 keep, 0 drop
# ----------------------------------------------------------------------
CDR = DatasetConfig(
    file_code="CDR",
    source="CDR_28Oct2025.csv",                 # <-- METTI il nome file reale
    category='scale',
    # rename -> alias 'ADNI:<file_code>.<colonna>' in catalog.json [D017]
    keep_columns=['COLPROT', 'RID', 'VISCODE2', 'VISDATE', 'CDRSB', 'update_stamp'],
)

# ======================================================================
# DXSUM   [categoria: cofactor]
#   dall'Excel: 4 keep, 0 drop
# ----------------------------------------------------------------------
DXSUM = DatasetConfig(
    file_code="DXSUM",
    source="DXSUM_25Jul2025.csv",                 # <-- METTI il nome file reale
    category='cofactor',
    # rename -> alias 'ADNI:<file_code>.<colonna>' in catalog.json [D017]
    keep_columns=['COLPROT', 'RID', 'EXAMDATE', 'DX'],
)

# ======================================================================
# EUROIMMUN   [categoria: csf]
#   dall'Excel: 6 keep, 0 drop
# ----------------------------------------------------------------------
EUROIMMUN = DatasetConfig(
    file_code="EUROIMMUN",
    source="EUROIMMUN_25Jul2025.csv",                 # <-- METTI il nome file reale
    category='csf',
    constant_columns={"METHOD_CSF": "elisa"},   # da Unit
    # rename -> alias 'ADNI:<file_code>.<colonna>' in catalog.json [D017]
    keep_columns=['RID', 'VISCODE2', 'EXAMDATE', 'AB40_CSF', 'AB42_CSF', 'AB4240_CSF'],
)

# ======================================================================
# FAQ   [categoria: scale]
#   dall'Excel: 6 keep, 0 drop
# ----------------------------------------------------------------------
FAQ = DatasetConfig(
    file_code="FAQ",
    source="FAQ_28Oct2025.csv",                 # <-- METTI il nome file reale
    category='scale',
    # rename -> alias 'ADNI:<file_code>.<colonna>' in catalog.json [D017]
    keep_columns=['COLPROT', 'RID', 'VISCODE2', 'VISDATE', 'FAQ', 'update_stamp'],
)

# ======================================================================
# FUJIREBIOABETA   [categoria: csf]
#   dall'Excel: 6 keep, 0 drop
# ----------------------------------------------------------------------
FUJIREBIOABETA = DatasetConfig(
    file_code="FUJIREBIOABETA",
    source="FUJIREBIOABETA_11Aug2025.csv",                 # <-- METTI il nome file reale
    category='csf',
    constant_columns={"METHOD_CSF": "lumipulse"},   # da Unit
    # rename -> alias 'ADNI:<file_code>.<colonna>' in catalog.json [D017]
    keep_columns=['RID', 'VISCODE2', 'EXAMDATE', 'AB42_CSF', 'AB40_CSF', 'AB4240_CSF'],
)

# ======================================================================
# MESOSCALE   [categoria: csf]
#   dall'Excel: 6 keep, 0 drop
# ----------------------------------------------------------------------
MESOSCALE = DatasetConfig(
    file_code="MESOSCALE",
    source="MESOSCALE_25Jul2025.csv",                 # <-- METTI il nome file reale
    category='csf',
    constant_columns={"METHOD_CSF": "MSD, Rockville MD"},   # da Unit
    # rename -> alias 'ADNI:<file_code>.<colonna>' in catalog.json [D017]
    keep_columns=['RID', 'DRAWDTE', 'VISCODE2', 'AB40_CSF', 'AB42_CSF', 'TTAU_CSF'],
)

# ======================================================================
# MMSE   [categoria: scale]
#   dall'Excel: 6 keep, 0 drop
# ----------------------------------------------------------------------
MMSE = DatasetConfig(
    file_code="MMSE",
    source="MMSE_25Jul2025.csv",                 # <-- METTI il nome file reale
    category='scale',
    # rename -> alias 'ADNI:<file_code>.<colonna>' in catalog.json [D017]
    keep_columns=['COLPROT', 'RID', 'VISDATE', 'MMSE', 'VISCODE2', 'update_stamp'],
)

# ======================================================================
# MOCA   [categoria: scale]
#   dall'Excel: 5 keep, 1 drop
# ----------------------------------------------------------------------
MOCA = DatasetConfig(
    file_code="MOCA",
    source="MOCA_28Oct2025.csv",                 # <-- METTI il nome file reale
    category='scale',
    # rename -> alias 'ADNI:<file_code>.<colonna>' in catalog.json [D017]
    keep_columns=['COLPROT', 'RID', 'VISCODE2', 'VISDATE', 'update_stamp'],
)

# ======================================================================
# PTDEMOG   [categoria: cofactor]
#   dall'Excel: 9 keep, 0 drop
#   collisioni risolte tenendo il grezzo (VERIFICA): [('PTRACCAT', 'ETHNICITY')]
# ----------------------------------------------------------------------
PTDEMOG = DatasetConfig(
    # Portata dal branch Assignment_analysis_fr (lavoro della collega), adattata al rename-first.
    file_code="PTDEMOG",
    source="PTDEMOG_21Apr2026.csv",
    category='cofactor',
    viscode_reference="VISCODE",               # = VISCODE2 grezzo, rinominato (piu' aggiornato)

    # cleaning 1 -----------------------------------------------------------
    drop_columns=["VISCODE"],                  # [D016] tolto: si usa VISCODE2, rinominato VISCODE
    # rename -> alias 'ADNI:<file_code>.<colonna>' in catalog.json [D017]
    drop_rows={"VISCODE": ["f"]},              # [D028] screen fail
    # [D027] qui -4 e 9999 sono codici; -1 compare in PTEDUCAT e PTADBEG, ed e' un codice
    missing_codes=[-4, "-4", -1, "-1", 9999, 9999.0],
    # PTDOB (MM/YYYY) e update_stamp sono date per il catalogo; PTDOB ha date_precision
    # 'month' -> giorno 15 [D029]. AGE si calcola da PTDOB perche' il file non la riporta [D019].
    essential_columns=["GENDER", "MARRY", "ETHNICITY", "RACE"],
    also_required=["PTDOB"],                   # senza data di nascita non si calcola l'eta'
    recode_columns=["GENDER", "MARRY", "ETHNICITY", "RACE"],
    clean_fs_fields=False,

    # cleaning 2 / 3 -------------------------------------------------------
    drop_sparse_columns=False,
    make_dummies=False,                        # [D026] dummy dopo il merge
    dummy_columns=["GENDER", "MARRY", "ETHNICITY", "RACE"],
    remove_single_visit=False,
    normalize_icv=False,
    # PTDOB NON e' qui: serve solo a calcolare l'eta' ed e' un quasi-identificativo.
    keep_columns=[
        "COLPROT", "PTID", "RID", "VISCODE", "EXAMDATE",
        "GENDER", "MARRY", "EDUCATION", "ETHNICITY", "RACE", "AGE",
        "PTADBEG", "PTCOGBEG", "PTADDX", "HAS_QC_ERROR", "update_stamp",
    ],
)

# ======================================================================
# SALADAX_BIOMEDICAL   [categoria: csf]
#   dall'Excel: 5 keep, 0 drop
# ----------------------------------------------------------------------
SALADAX_BIOMEDICAL = DatasetConfig(
    file_code="SALADAX_BIOMEDICAL",
    source="SALADAX_BIOMEDICAL_11Aug2025.csv",                 # <-- METTI il nome file reale
    category='csf',
    constant_columns={"METHOD_CSF": "saladax_immun_sandwich"},   # da Unit
    # rename -> alias 'ADNI:<file_code>.<colonna>' in catalog.json [D017]
    keep_columns=['RID', 'EXAMDATE', 'VISCODE2', 'AB42_CSF', 'TTAU_CSF'],
)

# ======================================================================
# UCSDVOL   [categoria: volumes]
#   dall'Excel: 9 keep, 0 drop
# ----------------------------------------------------------------------
UCSDVOL = DatasetConfig(
    file_code="UCSDVOL",
    source="UCSDVOL_28Oct2025.csv",                 # <-- METTI il nome file reale
    category='volumes',
    keep_columns=['RID', 'VISCODE', 'EXAMDATE', 'QCPASS', 'BRAIN', 'EICV', 'VENTRICLES', 'LHIPPOC', 'RHIPPOC'],
)

# ======================================================================
# UCSFFSL   [categoria: volumes]
#   dall'Excel: 20 keep, 0 drop
# ----------------------------------------------------------------------
UCSFFSL = DatasetConfig(
    file_code="UCSFFSL",
    source="UCSFFSL_02_01_16_11Aug2025.csv",                 # <-- METTI il nome file reale
    category='volumes',
    keep_columns=['RID', 'VISCODE2', 'EXAMDATE', 'FLDSTRENG', 'IMAGEUID', 'OVERALLQC', 'TEMPQC', 'VENTQC', 'STATUS', 'ST37SV', 'ST10CV', 'ST24CV', 'ST26CV', 'ST29SV', 'ST40CV', 'ST96SV', 'ST83CV', 'ST85CV', 'ST88SV', 'ST99CV'],
)

# ======================================================================
# UCSFFSL51   [categoria: volumes]
#   dall'Excel: 20 keep, 2 drop
# ----------------------------------------------------------------------
UCSFFSL51 = DatasetConfig(
    file_code="UCSFFSL51",
    source="UCSFFSL51_03_01_22_11Aug2025.csv",                 # <-- METTI il nome file reale
    category='volumes',
    keep_columns=['RID', 'VISCODE2', 'EXAMDATE', 'COLPROT', 'IMAGEUID', 'OVERALLQC', 'TEMPQC', 'VENTQC', 'STATUS', 'ST37SV', 'ST10CV', 'ST24CV', 'ST26CV', 'ST29SV', 'ST40CV', 'ST96SV', 'ST83CV', 'ST85CV', 'ST88SV', 'ST99CV'],
)

# ======================================================================
# UCSFFSL51ALL   [categoria: volumes]
#   dall'Excel: 17 keep, 5 drop
# ----------------------------------------------------------------------
UCSFFSL51ALL = DatasetConfig(
    file_code="UCSFFSL51ALL",
    source="UCSFFSL51ALL_08_01_16_11Aug2025.csv",                 # <-- METTI il nome file reale
    category='volumes',
    keep_columns=['RID', 'VISCODE2', 'EXAMDATE', 'COLPROT', 'IMAGEUID', 'STATUS', 'ST37SV', 'ST10CV', 'ST24CV', 'ST26CV', 'ST29SV', 'ST40CV', 'ST96SV', 'ST83CV', 'ST85CV', 'ST88SV', 'ST99CV'],
)

# ======================================================================
# UCSFFSL51Y1   [categoria: volumes]
#   dall'Excel: 20 keep, 2 drop
# ----------------------------------------------------------------------
UCSFFSL51Y1 = DatasetConfig(
    file_code="UCSFFSL51Y1",
    source="UCSFFSL51Y1_08_01_16_11Aug2025.csv",                 # <-- METTI il nome file reale
    category='volumes',
    keep_columns=['RID', 'VISCODE2', 'EXAMDATE', 'COLPROT', 'IMAGEUID', 'OVERALLQC', 'TEMPQC', 'VENTQC', 'STATUS', 'ST37SV', 'ST10CV', 'ST24CV', 'ST26CV', 'ST29SV', 'ST40CV', 'ST96SV', 'ST83CV', 'ST85CV', 'ST88SV', 'ST99CV'],
)

# ======================================================================
# UCSFFSX   [categoria: volumes]
#   dall'Excel: 20 keep, 0 drop
# ----------------------------------------------------------------------
UCSFFSX = DatasetConfig(
    file_code="UCSFFSX",
    source="UCSFFSX_11_02_15_11Aug2025.csv",                 # <-- METTI il nome file reale
    category='volumes',
    keep_columns=['RID', 'VISCODE', 'EXAMDATE', 'FLDSTRENG', 'IMAGEUID', 'OVERALLQC', 'TEMPQC', 'VENTQC', 'STATUS', 'ST37SV', 'ST10CV', 'ST24CV', 'ST26CV', 'ST29SV', 'ST40CV', 'ST96SV', 'ST83CV', 'ST85CV', 'ST88SV', 'ST99CV'],
)

# ======================================================================
# UCSFFSX51   [categoria: volumes]
#   dall'Excel: 20 keep, 2 drop
# ----------------------------------------------------------------------
UCSFFSX51 = DatasetConfig(
    file_code="UCSFFSX51",
    source="UCSFFSX51_11_08_19_11Aug2025.csv",                 # <-- METTI il nome file reale
    category='volumes',
    keep_columns=['RID', 'COLPROT', 'VISCODE2', 'EXAMDATE', 'IMAGEUID', 'OVERALLQC', 'TEMPQC', 'VENTQC', 'STATUS', 'ST37SV', 'ST10CV', 'ST24CV', 'ST26CV', 'ST29SV', 'ST40CV', 'ST96SV', 'ST83CV', 'ST85CV', 'ST88SV', 'ST99CV'],
)

# ======================================================================
# UCSFFSX51_ADNI1_3T   [categoria: volumes]
#   dall'Excel: 19 keep, 0 drop
# ----------------------------------------------------------------------
UCSFFSX51_ADNI1_3T = DatasetConfig(
    file_code="UCSFFSX51_ADNI1_3T",
    source="UCSFFSX51_ADNI1_3T_02_01_16_11Aug2025.csv",                 # <-- METTI il nome file reale
    category='volumes',
    keep_columns=['RID', 'VISCODE', 'EXAMDATE', 'IMAGEUID', 'OVERALLQC', 'TEMPQC', 'VENTQC', 'STATUS', 'ST37SV', 'ST10CV', 'ST24CV', 'ST26CV', 'ST29SV', 'ST40CV', 'ST96SV', 'ST83CV', 'ST85CV', 'ST88SV', 'ST99CV'],
)

# ======================================================================
# UCSFFSX6   [categoria: volumes]
#   dall'Excel: 21 keep, 0 drop
# ----------------------------------------------------------------------
UCSFFSX6 = DatasetConfig(
    file_code="UCSFFSX6",
    source="UCSFFSX6_11Aug2025.csv",                 # <-- METTI il nome file reale
    category='volumes',
    # rename -> alias 'ADNI:<file_code>.<colonna>' in catalog.json [D017]
    keep_columns=['RID', 'COLPROT', 'VISCODE2', 'EXAMDATE', 'IMAGEUID', 'OVERALLQC', 'TEMPQC', 'VENTQC', 'HIPPOQC', 'STATUS', 'ST37SV', 'ST10CV', 'ST24CV', 'ST26CV', 'ST29SV', 'ST40CV', 'ST96SV', 'ST83CV', 'ST85CV', 'ST88SV', 'ST99CV'],
)

# ======================================================================
# UCSFFSX7   [categoria: volumes]
#   dall'Excel: 19 keep, 4 drop
# ----------------------------------------------------------------------
UCSFFSX7 = DatasetConfig(
    file_code="UCSFFSX7",
    source="UCSFFSX7_11Aug2025.csv",                 # <-- METTI il nome file reale
    category='volumes',
    # rename -> alias 'ADNI:<file_code>.<colonna>' in catalog.json [D017]
    keep_columns=['RID', 'COLPROT', 'VISCODE2', 'EXAMDATE', 'IMAGEUID', 'FIELD_STRENGTH', 'FSVER', 'STATUS', 'ST37SV', 'ST10CV', 'ST24CV', 'ST26CV', 'ST29SV', 'ST40CV', 'ST96SV', 'ST83CV', 'ST85CV', 'ST88SV', 'ST99CV'],
)

# ======================================================================
# UPENNBIOMK_ADNIDIAN_ES_2017   [categoria: csf]
#   dall'Excel: 9 keep, 0 drop
# ----------------------------------------------------------------------
UPENNBIOMK_ADNIDIAN_ES_2017 = DatasetConfig(
    file_code="UPENNBIOMK_ADNIDIAN_ES_2017",
    source="UPENNBIOMKADNIDIAN2017_09Oct2025.csv",                 # <-- METTI il nome file reale
    category='csf',
    constant_columns={"METHOD_CSF": "elecsys"},   # da Unit
    # rename -> alias 'ADNI:<file_code>.<colonna>' in catalog.json [D017]
    keep_columns=['RID', 'VISCODE2', 'EXAMDATE', 'COLPROT', 'AB42_CSF', 'AB40_CSF', 'TTAU_CSF', 'PT181_CSF', 'AB4240_CSF'],
)

# ======================================================================
# UPENNBIOMK_MASTER   [categoria: csf]
#   dall'Excel: 6 keep, 0 drop
# ----------------------------------------------------------------------
UPENNBIOMK_MASTER = DatasetConfig(
    file_code="UPENNBIOMK_MASTER",
    source="UPENNBIOMK_MASTER_23Oct2025.csv",                 # <-- METTI il nome file reale
    category='csf',
    constant_columns={"METHOD_CSF": "AlzBio3"},   # da Unit
    # rename -> alias 'ADNI:<file_code>.<colonna>' in catalog.json [D017]
    keep_columns=['RID', 'DRAWDTE', 'VISCODE', 'AB42_CSF', 'TTAU_CSF', 'PT181_CSF'],
)

# ======================================================================
# UPENNBIOMK_ROCHE_ELECSYS   [categoria: csf]
#   dall'Excel: 7 keep, 1 drop
# ----------------------------------------------------------------------
UPENNBIOMK_ROCHE_ELECSYS = DatasetConfig(
    file_code="UPENNBIOMK_ROCHE_ELECSYS",
    source="UPENNBIOMK_ROCHE_ELECSYS_09Oct2025.csv",                 # <-- METTI il nome file reale
    category='csf',
    constant_columns={"METHOD_CSF": "elecsys"},   # da Unit
    # rename -> alias 'ADNI:<file_code>.<colonna>' in catalog.json [D017]
    keep_columns=['RID', 'VISCODE2', 'EXAMDATE', 'COLPROT', 'AB42_CSF', 'TTAU_CSF', 'PT181_CSF'],
)

# ======================================================================
# UPENN_2DUPLC_CRM   [categoria: csf]
#   dall'Excel: 5 keep, 0 drop
# ----------------------------------------------------------------------
UPENN_2DUPLC_CRM = DatasetConfig(
    file_code="UPENN_2DUPLC_CRM",
    source="UPENN_2DUPLC_CRM_09Oct2025.csv",                 # <-- METTI il nome file reale
    category='csf',
    constant_columns={"METHOD_CSF": "2DUPLC_massospectometry"},   # da Unit
    # rename -> alias 'ADNI:<file_code>.<colonna>' in catalog.json [D017]
    keep_columns=['RID', 'VISCODE2', 'EXAMDATE', 'AB40_CSF', 'AB42_CSF'],
)

# ======================================================================
# UPENN_ROI_MARS   [categoria: volumes]
#   dall'Excel: 14 keep, 0 drop
# ----------------------------------------------------------------------
UPENN_ROI_MARS = DatasetConfig(
    file_code="UPENN_ROI_MARS",
    source="UPENNROI_MARS_06_01_16_09Oct2025.csv",                 # <-- METTI il nome file reale
    category='volumes',
    keep_columns=['RID', 'VISCODE', 'EXAMDATE', 'IMAGE_UID', 'STATUS', 'R702', 'R525', 'R517', 'R122', 'R123', 'R116', 'R117', 'R47', 'R48'],
)



# ---------------------------------------------------------------------------
# 5c. MERGE per categoria — scheletro config-driven (il motore sta in pipeline).
#     Le REGOLE di risoluzione conflitti sono decisioni di Chiara: vanno qui,
#     non nel codice.  'strategy' e 'buffer_days' li confermi tu.
# ---------------------------------------------------------------------------
@dataclass
class MergeConfig:
    join_keys: list[str] = field(default_factory=lambda: ["RID", "EXAMDATE"])
    buffer_days: int = 80                     # match di visita entro N giorni
    method_column: Optional[str] = None       # colonna che distingue gli assay
    # come trattare la STESSA misura da metodi diversi:
    #   'suffix_by_method' -> NFL_plasma_panelA / NFL_plasma_panelB (niente perdita, niente pooling)
    #   'prefer'           -> tieni un metodo solo, secondo method_priority
    #   'most_recent'      -> tieni la riga con update_stamp piu' recente
    strategy: str = "suffix_by_method"
    method_priority: list[str] = field(default_factory=list)


CATEGORY_MERGE = {
    "plasma": MergeConfig(method_column="METHOD_PLASMA", strategy="suffix_by_method"),
    # "csf":   MergeConfig(method_column="METHOD_CSF", ...),
    # "pet":   MergeConfig(method_column="METHOD_PET", ...),
    # "volumes": MergeConfig(join_keys=["RID","EXAMDATE","FSVERSION"], ...),
}


# ---------------------------------------------------------------------------
# 5d. ARMONIZZAZIONE per categoria — stadio che precede il merge largo.
#     Idea: si impilano i file puliti (long, una riga per metodo), e per ogni
#     misura si portano TUTTI i metodi sulla scala di un metodo di riferimento,
#     calibrando sui campioni-ponte (stesso soggetto-visita misurato da 2 metodi).
#     Le DECISIONI (riferimento, strategia, covariate) stanno qui; i coefficienti
#     stimati NON si scrivono a mano: li calcola la pipeline e li salva in un
#     artefatto (harmonization_fit.json), cosi' la conversione e' auditabile.
# ---------------------------------------------------------------------------
@dataclass
class HarmonizeConfig:
    method_column: str = "METHOD_PLASMA"
    reference: Optional[str] = None                 # metodo su cui si collassa la scala
    strategy: str = "deming"                        # 'deming' | 'passing_bablok' | 'none'
    measurands: Optional[list] = None               # misure da armonizzare; None -> auto (numeriche multi-metodo)
    reference_overrides: dict = field(default_factory=dict)   # {misura: metodo} se il rif cambia per misura
    buffer_days: int = 80                           # tolleranza per appaiare le visite fra metodi
    min_bridge: int = 40                            # sotto -> converte ma AVVISA che il ponte e' debole


HARMONIZE = {
    # per il plasma: riferimento = spettrometria di massa (C2N) per l'Abeta;
    # NFL/GFAP/PT217/APS2 hanno un solo metodo -> passano invariati in automatico.
    "plasma": HarmonizeConfig(
        method_column="METHOD_PLASMA",
        reference="massospectrometry",
        strategy="deming",
    ),
}


# ---------------------------------------------------------------------------
# 6. Helper derivati dal catalogo
#    (CATEGORY_RENAME e i rename per-file sono stati migrati in alias qualificati in
#     catalog.json il 20/10/2026 [D017]: unica fonte di verita'.)
# ---------------------------------------------------------------------------
def columns_in(domain: str) -> list[str]:
    return [name for name, v in catalog().items() if v.domain == domain]


def volume_columns(icv_column: str = "ICV") -> list[str]:
    """Volumi da normalizzare su ICV: unita' mm3, ICV escluso (nomi standard stabili)."""
    return [name for name, v in catalog().items()
            if v.unit == "mm3" and name != icv_column]


DATASETS = {d.file_code: d for d in (
    ADNIMERGE,
    PLASMA_ADX_VUMC,
    PLASMA_NFL,
    PLASMA_C2N,
    ADAS,
    ADNI_DIAN_COMPARISON,
    ADSP_PHC_BIOMARKER,
    APOERES,
    CDR,
    DXSUM,
    EUROIMMUN,
    FAQ,
    FUJIREBIOABETA,
    MESOSCALE,
    MMSE,
    MOCA,
    PTDEMOG,
    SALADAX_BIOMEDICAL,
    UCSDVOL,
    UCSFFSL,
    UCSFFSL51,
    UCSFFSL51ALL,
    UCSFFSL51Y1,
    UCSFFSX,
    UCSFFSX51,
    UCSFFSX51_ADNI1_3T,
    UCSFFSX6,
    UCSFFSX7,
    UPENNBIOMK_ADNIDIAN_ES_2017,
    UPENNBIOMK_MASTER,
    UPENNBIOMK_ROCHE_ELECSYS,
    UPENN_2DUPLC_CRM,
    UPENN_ROI_MARS,
)}