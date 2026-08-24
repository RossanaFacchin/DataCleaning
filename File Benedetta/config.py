"""
config.py  —  configurazione di ADNI cleaning per il dataset ADNIMERGE.

A COSA SERVE
    Sostituisce il vecchio file Excel ADNI_variables_statistics.xlsx.
    Contiene solo DECISIONI e DATI (cosa tenere, come rinominare, quali soglie),
    mai LOGICA. La logica sta tutta in pipeline.py.

    Regola per capire dove va una cosa:
        e' una DECISIONE o un DATO?  -> qui (o in un file JSON esterno)
        e' un CALCOLO?               -> pipeline.py, e non si scrive a mano

    Corrispondenza col vecchio mondo:
        parameter                    -> Var.parameter   (gruppo della variabile)
        orig_variable_code -> code   -> Var.rename      (nome standard)
        Unit                         -> Var.unit
        metadati_fattori/norm        -> Var.role
        soglie a mano nelle celle    -> POLICY + campi di DatasetConfig
"""
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
import json
import numpy as np

_HERE = Path(__file__).parent


# ---------------------------------------------------------------------------
# 1. POLICY  —  regole globali (prima erano numeri sparsi dentro le celle)
# ---------------------------------------------------------------------------
UNKNOWN_SENTINELS = ["Unknown", "unknown", "NA", "N/A", "-4", -4, 9999, 9999.0, -1, "-1"]
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
RECODE = {
    "PTGENDER": {"Male": 1, "Female": 0, 1: 1, "1": 1, 2: 0, "2": 0},
    "PTMARRY":  {"Married": 1, "Divorced": 2, "Widowed": 3,
                 "Never married": 0, "Unknown": np.nan, 1: 1, "1": 1,
                 2: 3, "2": 3, 3: 2, "3": 2, 4: 0, "4": 0, 
                 5: np.nan, "5": np.nan,6: 1, "6": 1,},
    "PTETHCAT": {"Hisp/Latino": 1, "Not Hisp/Latino": 0, "Unknown": np.nan,
                 1: 1, "1": 1, 2: 0, "2": 0, 3: np.nan, "3": np.nan,},
    "PTRACCAT": {"White": 5, "Black": 4, "Asian": 2, "Am Indian/Alaskan": 1,
                 "Hawaiian/Other PI": 3, "More than one": 0, "Unknown": np.nan, 
                 1: 1, "1": 1, 2: 2, "2": 2,  3: 3, "3": 3, 4: 4, "4": 4, 
                 5: 5, "5": 5, 6: 0, "6": 0, 7: np.nan, "7": np.nan,
                 8: 3, "8": 3, 9: 3, "9": 3,},
    "DX":       {"CN": 0, "MCI": 1, "Dementia": 2},
}



# ---------------------------------------------------------------------------
# 4. CATALOG  —  le variabili di interesse (ex tabella del support file Excel).
#    Per ogni variabile: gruppo, nome standard, unita', ruolo.
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Var:
    parameter: str
    rename: Optional[str] = None
    unit: Optional[str] = None
    role: Optional[str] = None          # 'predittore' | 'normalizzazione' | None


CATALOG: dict[str, Var] = {
    "RID":      Var("ID"),
    "PTID":     Var("ID"),#potrebbe essere tolto
    "COLPROT":  Var("Cohort"),
    "PHASE":    Var("Cohort"),                      #riga aggiunta fasi PTDEMOG fr
    "VISCODE":  Var("Visit"),
    "VISCODE2": Var("Visit"),                       #riga aggiunta PTDEMOG fr
    "VISDATE":  Var("Visit", rename="EXAMDATE"),                       #riga aggiunta PTDEMOG fr
    "EXAMDATE": Var("Visit"),
    "AGE":      Var("Demographic", unit="years"),
    "PTGENDER": Var("Demographic", rename="GENDER"),
    "PTDOP":    Var("Demographic"),               #riga aggiunta mese/anno PTDEMOG fr
    "PTEDUCAT": Var("Demographic", rename="EDUCATION", unit="years"),
    "PTMARRY":  Var("Demographic", rename="MARRY"),
    "PTETHCAT": Var("Demographic", rename="ETHNICITY"),
    "PTRACCAT": Var("Demographic", rename="RACE"),
    "APOE4":    Var("Genetic", role="predittore"),
    "DX":       Var("Diagnosis"),
    "MMSE":     Var("Cognitive", role="predittore"),
    "CDRSB":    Var("Cognitive", role="predittore"),
    "ADAS13":   Var("Cognitive", role="predittore"),
    "Ventricles":  Var("Imaging", unit="mm3"),
    "Hippocampus": Var("Imaging", unit="mm3", role="predittore"),
    "WholeBrain":  Var("Imaging", unit="mm3"),
    "ICV":         Var("Imaging", unit="mm3", role="normalizzazione"),
    "FLDSTRENG":   Var("Imaging"),
    "FSVERSION":   Var("Imaging"),
    # biomarcatori CSF: rename = chiavi di cutoffs.json (usati solo dai file CSF)
    "ABETA":    Var("Biomarker", rename="AB42_CSF",  unit="pg/mL", role="predittore"),
    "TAU":      Var("Biomarker", rename="TTAU_CSF",  unit="pg/mL", role="predittore"),
    "PTAU":     Var("Biomarker", rename="PT181_CSF", unit="pg/mL", role="predittore"),
    "PTADBEG":      Var("Demographic"),               #riga aggiunta  PTDEMOG fr
    "PTCOGBEG":     Var("Demographic"),               #riga aggiunta  PTDEMOG fr             
    "PTADDX":       Var("Diagnosis"),                 #riga aggiunta  PTDEMOG fr               
    "HAS_QC_ERROR": Var("QC"),                        #riga aggiunta  PTDEMOG fr               
    "update_stamp": Var("Metadata"),                  #riga aggiunta  PTDEMOG fr
}


# ---------------------------------------------------------------------------
# 5. DATASET  —  la "scheda d'identita'" del file, fedele al blocco ADNIMERGE
#    di adni_cleaning1.ipynb (celle 222-224) + il blocco cleaning 2/3.
# ---------------------------------------------------------------------------
@dataclass
class DatasetConfig:
    file_code: str
    source: str
    id_column: str = "RID"
    date_column: str = "EXAMDATE"
    viscode_reference: Optional[str] = "VISCODE"
    cohort_column: str = "COLPROT"

    # --- identita' per il merge ---
    category: Optional[str] = None      # 'plasma'|'csf'|'pet'|'volumes'|'scale'|'cofactor'

    # --- cleaning 1 ---
    essential_columns: list[str] = field(default_factory=list)   # tieni riga se >=1 valorizzata
    also_required: list[str] = field(default_factory=list)       # 2° filtro (AND): richiedi questa
    recode_columns: list[str] = field(default_factory=list)      # quali colonne passare a RECODE
    # rinomina PER-FILE: sovrascrive/estende il CATALOG globale, senza toccarlo.
    # e' cio' che permette a NF_LIGHT e PLASMA_NFL (file diversi) di finire
    # entrambi in NFL_plasma senza inquinare il catalogo condiviso.
    rename: dict[str, str] = field(default_factory=dict)
    # colonne-costante da stampare (ARMONIZZAZIONE): il metodo/assay e' il file,
    # non una colonna -> lo si assegna qui.  es. {"METHOD_PLASMA": "simoa"}
    constant_columns: dict[str, str] = field(default_factory=dict)
    # rapporti derivati generici: {nome_nuovo: (numeratore, denominatore)} in nomi standard
    derived_ratios: dict[str, tuple] = field(default_factory=dict)
    decensor_biomarkers: bool = False   # ">1700"/"<200" -> numerico (file CSF/plasma)
    decensor_columns: list[str] = field(default_factory=list)     # nomi GREZZI (decensor gira pre-rename)
    recompute_age: bool = False         # AGE_bl + Δtempo -> AGE per visita
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

    def __post_init__(self):
        # i nomi di output derivano da file_code se non specificati a mano
        if self.output_cleaned1 is None:
            self.output_cleaned1 = f"{self.file_code}_cleaned_01.csv"
        if self.output_cleaned2 is None:
            self.output_cleaned2 = f"{self.file_code}_cleaned_02.csv"
        if self.report_file is None:
            self.report_file = f"{self.file_code}_report.csv"

    def effective_rename(self) -> dict[str, str]:
        """CATALOG globale + override per-file. Il per-file vince sui conflitti."""
        return {**rename_map(), **self.rename}


ADNIMERGE = DatasetConfig(
    file_code="ADNIMERGE",
    source="ADNIMERGE_05Mar2026.csv",          # SEMPRE il file grezzo: cleaning1 legge il raw
    viscode_reference="VISCODE",

    # cleaning 1 -----------------------------------------------------------
    essential_columns=["APOE4", "MMSE", "Ventricles", "Hippocampus", "AGE"],
    also_required=["DX"],
    recode_columns=["PTGENDER", "PTMARRY", "PTETHCAT", "PTRACCAT", "DX"],
    recompute_age=True,
    clean_fs_fields=True,
    # compute_atn resta False: nel notebook l'ATN e' solo per i file CSF, non ADNIMERGE

    # cleaning 2 / 3 -------------------------------------------------------
    drop_sparse_columns=True,                  # come faceva Rossana (remove_param_few_subjects)
    make_dummies=True,
    dummy_columns=["GENDER", "MARRY", "ETHNICITY", "RACE", "DX"],   # nomi STANDARD, post-rename
    volume_row_keys=["Ventricles", "Hippocampus", "WholeBrain", "ICV"],  # scarta riga se tutte NaN

    # --- DUE decisioni lasciate a te (vedi documento per Rossana, §"manca qualcosa"):
    #     stanno nella "base" documentata (cleaning2/cleaning3) ma cambiano i numeri,
    #     quindi le lascio OFF e le decidi tu. Sono gia' implementate in pipeline.py.
    remove_single_visit=False,                 # -> True per riprodurre cleaning2 (scarta soggetti 1 visita)
    normalize_icv=False,                       # -> True per riprodurre cleaning3 (volumi come % di ICV)

    # whitelist finale (le "colonne di Chiara"), in NOMI STANDARD post-rename.
    # Le dummy generate e le colonne calcolate (VISIT_MONTH, AGE_bl) vengono
    # tenute automaticamente dalla pipeline: NON si elencano qui a mano.
    keep_columns=[
        "RID", "COLPROT", "VISCODE", "EXAMDATE", "AGE",
        "EDUCATION", "APOE4", "CDRSB", "ADAS11", "ADAS13", "MMSE",
        "RAVLT_immediate", "FAQ", "MOCA", "FLDSTRENG", "FSVERSION", "IMAGEUID",
        "Ventricles", "Hippocampus", "Entorhinal", "Fusiform", "MidTemp", "ICV",
        "update_stamp",
    ],
)

PTDEMOG = DatasetConfig(
    file_code="PTDEMOG",
    source="PTDEMOG_21Apr2026.csv",            # SEMPRE il file grezzo: cleaning1 legge il raw
    viscode_reference="VISCODE2",               # <-- DA CONFERMARE: in PTDEMOG la colonna è VISCODE2, non VISCODE, perchè più aggiornato

    # cleaning 1 -----------------------------------------------------------
    essential_columns=["PTGENDER", "PTMARRY", "PTETHCAT", "PTRACCAT"],                      
    also_required=["PTDOB"],                           # nessun secondo filtro
    recode_columns=["PTGENDER", "PTMARRY", "PTETHCAT", "PTRACCAT"],   # <-- DA CONFERMARE (niente DX qui, non presente in PTDEMOG)
    recompute_age=False,                        # non c'è AGE, solo PTDOBYY/PTDOB (mese/anno di nascita)
    clean_fs_fields=False,                      # nessun campo FreeSurfer in questo file
    # compute_atn resta False: ATN calcolato solo per i file CSF, non per PTDEMOG

    # cleaning 2 / 3 -------------------------------------------------------
    drop_sparse_columns=False,                  # <-- DA CONFERMARE: deciso che la rimozione colonne sarà automatica in pipeline, non da questo flag?
    make_dummies=True,                          # <-- DA CONFERMARE: applichi le dummy anche a PTDEMOG?
    dummy_columns=["GENDER", "MARRY", "ETHNICITY", "RACE"],   # <-- DA CONFERMARE: nomi standard post-rename, senza DX
    volume_row_keys=[],                         # non applicabile: PTDEMOG non ha colonne di volume/imaging

    remove_single_visit=False,
    normalize_icv=False,                        # non applicabile: nessun ICV in PTDEMOG
    keep_columns=[
        "PHASE", "PTID", "RID", "VISCODE2", "VISDATE", "SITEID",
        "PTGENDER", "PTDOB", "PTMARRY", "PTEDUCAT", "PTETHCAT", "PTRACCAT",
        "PTADBEG", "PTCOGBEG", "PTADDX", "HAS_QC_ERROR", "update_stamp",
    ],
)

# ---------------------------------------------------------------------------
# 5b. Altri dataset — ESEMPIO: i tuoi due file plasma, descritti SOLO come config.
#     Nessuna funzione nuova, nessuna modifica al CATALOG globale.
# ---------------------------------------------------------------------------

# File 1 — pannello plasma (NfL + Abeta42/40 + GFAP).
PLASMA_PANEL = DatasetConfig(
    file_code="PLASMA_ABETA_PROJECT_ADX_VUMC",                 
    source="PLASMA_ABETA_PROJECT_ADX_VUMC_11Aug2025.csv",           # <-- il tuo CSV
    category="plasma",
    date_column="EXAMDATE",
    essential_columns=["NF_LIGHT", "ABETA42", "GFAP"],   # nomi GREZZI (pre-rename)
    rename={                                  # override per-file, non tocca il CATALOG
        "NF_LIGHT": "NFL_plasma",
        "ABETA42":  "AB42_plasma",
        "ABETA40":  "AB40_plasma",
        "GFAP":     "GFAP_plasma",
    },
    constant_columns={"METHOD_PLASMA": "panelA"},        # <-- l'assay reale del file 1
    derived_ratios={"AB42_40_plasma": ("AB42_plasma", "AB40_plasma")},
    decensor_biomarkers=True,
    decensor_columns=["NF_LIGHT", "ABETA42", "ABETA40", "GFAP"],
    keep_columns=[                            # nomi STANDARD (post-rename): l'assay-metadata si scarta da sola
        "RID", "VISCODE", "EXAMDATE",
        "NFL_plasma", "AB42_plasma", "AB40_plasma", "GFAP_plasma", "AB42_40_plasma",
        "METHOD_PLASMA", "update_stamp",
    ],
)

# File 2 — solo plasma NfL (altro assay: stessa variabile standard, metodo diverso).
PLASMA_NFL = DatasetConfig(
    file_code="BLENNOWPLASMANFL",                   # <-- codice ADNI reale
    source="ADNI_BLENNOWPLASMANFLLONG_10_03_18_11Aug2025.csv",
    category="plasma",
    date_column="EXAMDATE",
    essential_columns=["PLASMA_NFL"],
    rename={"PLASMA_NFL": "NFL_plasma"},      # STESSO nome standard del file 1 -> armonizzazione
    constant_columns={"METHOD_PLASMA": "panelB"},        # <-- assay diverso
    keep_columns=["RID", "VISCODE", "EXAMDATE", "NFL_plasma", "METHOD_PLASMA", "update_stamp"],
)

DATASETS = {d.file_code: d for d in (ADNIMERGE, PLASMA_PANEL, PLASMA_NFL, PTDEMOG)}


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
# 6. Helper derivati
# ---------------------------------------------------------------------------
def rename_map() -> dict[str, str]:
    return {name: v.rename for name, v in CATALOG.items() if v.rename}


def columns_in(parameter: str) -> list[str]:
    return [name for name, v in CATALOG.items() if v.parameter == parameter]


def volume_columns(icv_column: str = "ICV") -> list[str]:
    """Volumi da normalizzare su ICV: unita' mm3, ICV escluso (nomi stabili post-rename)."""
    return [name for name, v in CATALOG.items()
            if v.unit == "mm3" and name != icv_column]