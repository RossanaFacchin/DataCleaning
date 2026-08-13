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
UNKNOWN_SENTINELS = ["Unknown", "unknown", "NA", "N/A", "-4", -4, 9999, 9999.0]
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
# ---------------------------------------------------------------------------
# 3. RECODE  —  categorie -> ETICHETTE STANDARD (stringhe), non numeri.
#    [nota Chiara #3] mappare a stringhe standard rende le dummy leggibili
#    (DX_CN, GENDER_male) e non costringe a ri-convertire in numeri dopo.
#    Chiavi = NOMI STANDARD (il recode gira DOPO il rename, vedi nota #4).
# ---------------------------------------------------------------------------
RECODE = {
    "GENDER":    {"Male": "male", "Female": "female"},
    "MARRY":     {"Married": "married", "Divorced": "divorced", "Widowed": "widowed",
                  "Never married": "never_married", "Unknown": np.nan},
    "ETHNICITY": {"Hisp/Latino": "hisp", "Not Hisp/Latino": "not_hisp", "Unknown": np.nan},
    "RACE":      {"White": "white", "Black": "black", "Asian": "asian",
                  "Am Indian/Alaskan": "amind", "Hawaiian/Other PI": "hawaiian",
                  "More than one": "mixed", "Unknown": np.nan},
    "DX":        {"CN": "CN", "MCI": "MCI", "Dementia": "Dementia"},
}


# ---------------------------------------------------------------------------
# 4. CATALOG  —  le variabili di interesse, INDICIZZATE PER NOME STANDARD.
#    [nota Chiara #4] la chiave e' il nome standard (scritto una volta sola);
#    'aliases' elenca i nomi grezzi noti nei vari file. La mappa grezzo->standard
#    per il rename si GENERA da qui (rename_map), con controllo anti-collisione
#    a import-time. Aggiungere un sinonimo nuovo = appendere a 'aliases', in un
#    solo posto, senza duplicare parameter/unit/role e senza typo del nome standard.
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Var:
    parameter: str
    unit: Optional[str] = None
    role: Optional[str] = None          # 'predittore' | 'normalizzazione' | None
    aliases: tuple = ()                  # nomi grezzi noti (grezzo -> questa chiave standard)


CATALOG: dict[str, Var] = {
    "RID":         Var("ID", aliases=("RID",)),
    "PTID":        Var("ID", aliases=("PTID",)),
    "COLPROT":     Var("Cohort", aliases=("COLPROT",)),
    "VISCODE":     Var("Visit", aliases=("VISCODE",)),
    "EXAMDATE":    Var("Visit", aliases=("EXAMDATE",)),
    "AGE":         Var("Demographic", unit="years", aliases=("AGE",)),
    "GENDER":      Var("Demographic", aliases=("PTGENDER", "SEX", "Gender")),
    "EDUCATION":   Var("Demographic", unit="years", aliases=("PTEDUCAT",)),
    "MARRY":       Var("Demographic", aliases=("PTMARRY",)),
    "ETHNICITY":   Var("Demographic", aliases=("PTETHCAT",)),
    "RACE":        Var("Demographic", aliases=("PTRACCAT",)),
    "APOE4":       Var("Genetic", role="predittore", aliases=("APOE4",)),
    "DX":          Var("Diagnosis", aliases=("DX",)),
    "MMSE":        Var("Cognitive", role="predittore", aliases=("MMSE",)),
    "CDRSB":       Var("Cognitive", role="predittore", aliases=("CDRSB",)),
    "ADAS13":      Var("Cognitive", role="predittore", aliases=("ADAS13",)),
    "Ventricles":  Var("Imaging", unit="mm3", aliases=("Ventricles",)),
    "Hippocampus": Var("Imaging", unit="mm3", role="predittore", aliases=("Hippocampus",)),
    "WholeBrain":  Var("Imaging", unit="mm3", aliases=("WholeBrain",)),
    "ICV":         Var("Imaging", unit="mm3", role="normalizzazione", aliases=("ICV",)),
    "FLDSTRENG":   Var("Imaging", aliases=("FLDSTRENG",)),
    "FSVERSION":   Var("Imaging", aliases=("FSVERSION",)),
    # biomarcatori CSF: la chiave standard = chiave di cutoffs.json
    "AB42_CSF":    Var("Biomarker", unit="pg/mL", role="predittore", aliases=("ABETA",)),
    "TTAU_CSF":    Var("Biomarker", unit="pg/mL", role="predittore", aliases=("TAU",)),
    "PT181_CSF":   Var("Biomarker", unit="pg/mL", role="predittore", aliases=("PTAU",)),
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
    # [nota Chiara #1] scarta la riga se MANCA anche UNA sola di queste (any-none),
    # es. ID o data: e' diverso da essential_columns (che scarta se TUTTE mancano).
    required_all_present: list[str] = field(default_factory=list)
    essential_columns: list[str] = field(default_factory=list)   # tieni riga se >=1 valorizzata (NOMI STANDARD)
    also_required: list[str] = field(default_factory=list)       # 2° filtro (AND): richiedi questa (NOMI STANDARD)
    recode_columns: list[str] = field(default_factory=list)      # colonne da passare a RECODE (NOMI STANDARD)
    # rinomina PER-FILE: sovrascrive/estende il CATALOG globale, senza toccarlo.
    # e' cio' che permette a piu' grezzi (NF_LIGHT, PLASMA_NFL) di finire sullo
    # stesso nome standard (NFL_PL) senza inquinare il catalogo condiviso.
    rename: dict[str, str] = field(default_factory=dict)
    # colonne-costante da stampare (ARMONIZZAZIONE): il metodo/assay e' il file,
    # non una colonna -> lo si assegna qui.  es. {"METHOD_PLASMA": "simoa"}
    constant_columns: dict[str, str] = field(default_factory=dict)
    # rapporti derivati generici: {nome_nuovo: (numeratore, denominatore)} in nomi standard
    derived_ratios: dict[str, tuple] = field(default_factory=dict)
    decensor_biomarkers: bool = False   # ">1700"/"<200" -> numerico (file CSF/plasma)
    decensor_columns: list[str] = field(default_factory=list)     # NOMI STANDARD (decensor gira post-rename)
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
        """CATALOG globale < rename di CATEGORIA < override per-file (il piu' specifico vince)."""
        cat_map = CATEGORY_RENAME.get(self.category, {}) if self.category else {}
        return {**rename_map(), **cat_map, **self.rename}


ADNIMERGE = DatasetConfig(
    file_code="ADNIMERGE",
    source="ADNIMERGE_05Mar2026.csv",          # SEMPRE il file grezzo: cleaning1 legge il raw
    viscode_reference="VISCODE",

    # cleaning 1 -----------------------------------------------------------
    required_all_present=["RID"],              # [#1] scarta la riga se manca l'ID
    essential_columns=["APOE4", "MMSE", "Ventricles", "Hippocampus", "AGE"],
    also_required=["DX"],
    recode_columns=["GENDER", "MARRY", "ETHNICITY", "RACE", "DX"],   # NOMI STANDARD (rename-first)
    recompute_age=True,
    clean_fs_fields=True,
    # compute_atn resta False: nel notebook l'ATN e' solo per i file CSF, non ADNIMERGE

    # cleaning 2 / 3 -------------------------------------------------------
    drop_sparse_columns=True,                  # come faceva Rossana (remove_param_few_subjects)
    make_dummies=True,
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
        "RID", "COLPROT", "VISCODE", "EXAMDATE", "AGE",
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
    rename={                                                # -> nomi canonici _PL
        "NF_LIGHT": "NFL_PL",
        "ABETA42":  "AB42_PL",
        "ABETA40":  "AB40_PL",
        "GFAP":     "GFAP",
    },
    # METODO: distinto da C2N. CONFERMA l'assay reale: se questo pannello e' il Simoa
    # 4-plex usa "simoa"/"quanterix" (ma allora e' lo STESSO metodo NfL di Blennow ->
    # non si armonizza, si concatena); "adx_vumc" e' un placeholder sicuro e distinto.
    constant_columns={"METHOD_PLASMA": "adx_vumc"},
    derived_ratios={"AB4240_PL": ("AB42_PL", "AB40_PL")},
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
    rename={"PLASMA_NFL": "NFL_PL"},                        # STESSO nome di ADX -> armonizzabile
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
    rename={
        "pT217_C2N":        "PT217_PL",
        "npT217_C2N":       "nPT217_PL",
        "AB42_C2N":         "AB42_PL",          # STESSO nome di ADX -> Abeta armonizzabile fra i due
        "AB40_C2N":         "AB40_PL",
        "AB42_AB40_C2N":    "AB4240_PL",        # rapporto gia' nel file: si rinomina, non si ricalcola
        "pT217_npT217_C2N": "PT217_nPT217_PL",
        "APS2_C2N":         "APS2",
        "APOE_C2N":         "APOE",
    },
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
    rename={               # grezzo -> standard (VERIFICA, dedotto da parameter)
        'PHASE': 'COLPROT',
    },
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
    rename={               # grezzo -> standard (VERIFICA, dedotto da parameter)
        'VISITAGE': 'AGE',
        'HISPANIC': 'ETHNICITY',
        'MARISTAT': 'MARRY',
        'DIAN_APOE': 'APOE4',
        'CDRSUM': 'CDRSB',
        'DIAN_MMSE': 'MMSE',
    },
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
    rename={               # grezzo -> standard (VERIFICA, dedotto da parameter)
        'PHASE': 'COLPROT',
        'PHC_Education': 'EDUCATION',
        'PHC_Ethnicity': 'ETHNICITY',
        'PHC_Sex': 'GENDER',
        'PHC_Diagnosis': 'DX',
        'PHC_Age_Biomarker': 'AGE',
        'AB42_RAW': 'AB42_CSF',
        'Tau_RAW': 'TTAU_CSF',
        'pTau_RAW': 'PT181_CSF',
    },
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
    rename={               # grezzo -> standard (VERIFICA, dedotto da parameter)
        'PHASE': 'COLPROT',
        'GENOTYPE': 'APOE4',
    },
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
    rename={               # grezzo -> standard (VERIFICA, dedotto da parameter)
        'PHASE': 'COLPROT',
        'CDGLOBAL': 'CDRSB',
    },
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
    rename={               # grezzo -> standard (VERIFICA, dedotto da parameter)
        'PHASE': 'COLPROT',
        'DIAGNOSIS': 'DX',
    },
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
    rename={               # grezzo -> standard (VERIFICA, dedotto da parameter)
        'BETA_AMYLOID_1_40': 'AB40_CSF',
        'BETA_AMYLOID_1_42': 'AB42_CSF',
        'BETA_AMYLOID_42_40': 'AB4240_CSF',
    },
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
    rename={               # grezzo -> standard (VERIFICA, dedotto da parameter)
        'PHASE': 'COLPROT',
        'FAQTOTAL': 'FAQ',
    },
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
    rename={               # grezzo -> standard (VERIFICA, dedotto da parameter)
        'ABETA42': 'AB42_CSF',
        'ABETA40': 'AB40_CSF',
        'ABETA42_40': 'AB4240_CSF',
    },
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
    rename={               # grezzo -> standard (VERIFICA, dedotto da parameter)
        'ABETA40': 'AB40_CSF',
        'ABETA42': 'AB42_CSF',
        'TAU': 'TTAU_CSF',
    },
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
    rename={               # grezzo -> standard (VERIFICA, dedotto da parameter)
        'PHASE': 'COLPROT',
        'MMSCORE': 'MMSE',
    },
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
    rename={               # grezzo -> standard (VERIFICA, dedotto da parameter)
        'PHASE': 'COLPROT',
    },
    keep_columns=['COLPROT', 'RID', 'VISCODE2', 'VISDATE', 'update_stamp'],
)

# ======================================================================
# PTDEMOG   [categoria: cofactor]
#   dall'Excel: 9 keep, 0 drop
#   collisioni risolte tenendo il grezzo (VERIFICA): [('PTRACCAT', 'ETHNICITY')]
# ----------------------------------------------------------------------
PTDEMOG = DatasetConfig(
    file_code="PTDEMOG",
    source="PTDEMOG_25Jul2025.csv",                 # <-- METTI il nome file reale
    category='cofactor',
    rename={               # grezzo -> standard (VERIFICA, dedotto da parameter)
        'PHASE': 'COLPROT',
        'PTGENDER': 'GENDER',
        'PTMARRY': 'MARRY',
        'PTEDUCAT': 'EDUCATION',
        'PTETHCAT': 'ETHNICITY',
    },
    keep_columns=['COLPROT', 'RID', 'VISDATE', 'GENDER', 'MARRY', 'EDUCATION', 'ETHNICITY', 'PTRACCAT', 'VISCODE2'],
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
    rename={               # grezzo -> standard (VERIFICA, dedotto da parameter)
        'ABETA42': 'AB42_CSF',
        'TOTALTAU': 'TTAU_CSF',
    },
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
    rename={               # grezzo -> standard (VERIFICA, dedotto da parameter)
        'PHASE': 'COLPROT',
    },
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
    rename={               # grezzo -> standard (VERIFICA, dedotto da parameter)
        'PHASE': 'COLPROT',
    },
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
    rename={               # grezzo -> standard (VERIFICA, dedotto da parameter)
        'STUDY': 'COLPROT',
        'ABETA': 'AB42_CSF',
        'AB40': 'AB40_CSF',
        'TAU': 'TTAU_CSF',
        'PTAU': 'PT181_CSF',
        'A4240': 'AB4240_CSF',
    },
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
    rename={               # grezzo -> standard (VERIFICA, dedotto da parameter)
        'ABETA': 'AB42_CSF',
        'TAU': 'TTAU_CSF',
        'PTAU': 'PT181_CSF',
    },
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
    rename={               # grezzo -> standard (VERIFICA, dedotto da parameter)
        'PHASE': 'COLPROT',
        'ABETA42': 'AB42_CSF',
        'TAU': 'TTAU_CSF',
        'PTAU': 'PT181_CSF',
    },
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
    rename={               # grezzo -> standard (VERIFICA, dedotto da parameter)
        'ABETA40': 'AB40_CSF',
        'ABETA42CRM': 'AB42_CSF',
    },
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
# 5e. CATEGORY_RENAME — rename PER CATEGORIA (risolve i biomarcatori ambigui per
#     matrice). Lo STESSO nome grezzo mappa a standard diversi secondo la categoria:
#     ABETA42 -> AB42_PL nei plasma, -> AB42_CSF nei CSF. Non puo' stare nel CATALOG
#     globale (collisione), quindi vive qui e si applica ai file di quella categoria.
#     Precedenza (in effective_rename): CATALOG globale < categoria < rename per-file.
#     BOZZA: verifica/estendi con Chiara i mapping clinici.
# ---------------------------------------------------------------------------
CATEGORY_RENAME = {
    "plasma": {
        "NF_LIGHT": "NFL_PL", "PLASMA_NFL": "NFL_PL",
        "ABETA42": "AB42_PL", "AB42": "AB42_PL",
        "ABETA40": "AB40_PL", "AB40": "AB40_PL",
        "TAU": "TTAU_PL", "PTAU": "PT181_PL",
    },
    "csf": {
        "ABETA": "AB42_CSF", "ABETA42": "AB42_CSF",
        "TAU": "TTAU_CSF", "PTAU": "PT181_CSF",
    },
    "pet": {
        "META_TEMPORAL_SUVR": "TAU_METAROI", "SUMMARYSUVR": "SUMMARY_SUVR",
        "CENTILOIDS": "AMY_CENTILOIDS",
    },
}


# ---------------------------------------------------------------------------
# 6. Helper derivati
# ---------------------------------------------------------------------------
def _build_rename_map() -> dict[str, str]:
    """Reverse-map alias(grezzo) -> nome standard. [nota Chiara #4] Con controllo
    anti-collisione: se due variabili standard rivendicano lo stesso alias -> errore
    esplicito a import-time, invece di un rename ambiguo silenzioso."""
    m: dict[str, str] = {}
    for std, v in CATALOG.items():
        for alias in v.aliases:
            if alias in m and m[alias] != std:
                raise ValueError(
                    f"CATALOG: alias '{alias}' condiviso da '{m[alias]}' e '{std}'. "
                    f"Un alias grezzo puo' mappare a un solo nome standard."
                )
            m[alias] = std
    return m


RENAME = _build_rename_map()          # costruita (e validata) all'import


def rename_map() -> dict[str, str]:
    """Mappa grezzo -> standard (esclude le identita' std->std, inutili al rename)."""
    return {raw: std for raw, std in RENAME.items() if raw != std}


def columns_in(parameter: str) -> list[str]:
    return [name for name, v in CATALOG.items() if v.parameter == parameter]


def volume_columns(icv_column: str = "ICV") -> list[str]:
    """Volumi da normalizzare su ICV: unita' mm3, ICV escluso (nomi standard stabili)."""
    return [name for name, v in CATALOG.items()
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