"""
config.py  —  configurazione di ADNI cleaning 1 per il dataset ADNIMERGE.

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
MISSING_KEEP_THRESHOLD = 0.65           # sotto questa quota di validi -> 'drop' nel report


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


# ---------------------------------------------------------------------------
# 3. RECODE  —  stringhe categoriche -> codici (ex funzioni categorize_*).
#    Le classi sono lette da ADNIMERGE; i codici seguono la convenzione del
#    notebook (README 5.1), non una nuova.
# ---------------------------------------------------------------------------
RECODE = {
    "PTGENDER": {"Male": 1, "Female": 0},
    "PTMARRY":  {"Married": 1, "Divorced": 2, "Widowed": 3,
                 "Never married": 0, "Unknown": np.nan},
    "PTETHCAT": {"Hisp/Latino": 1, "Not Hisp/Latino": 0, "Unknown": np.nan},
    "PTRACCAT": {"White": 5, "Black": 4, "Asian": 2, "Am Indian/Alaskan": 1,
                 "Hawaiian/Other PI": 3, "More than one": 0, "Unknown": np.nan},
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
    "PTID":     Var("ID"),
    "COLPROT":  Var("Cohort"),
    "VISCODE":  Var("Visit"),
    "EXAMDATE": Var("Visit"),
    "AGE":      Var("Demographic", unit="years"),
    "PTGENDER": Var("Demographic", rename="GENDER"),
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
}


# ---------------------------------------------------------------------------
# 5. DATASET  —  la "scheda d'identita'" del file, fedele al blocco ADNIMERGE
#    di adni_cleaning1.ipynb (celle 222-224).
# ---------------------------------------------------------------------------
@dataclass
class DatasetConfig:
    file_code: str
    source: str
    id_column: str = "RID"
    date_column: str = "EXAMDATE"
    viscode_reference: Optional[str] = "VISCODE"
    essential_columns: list[str] = field(default_factory=list)   # tieni riga se >=1 valorizzata
    also_required: list[str] = field(default_factory=list)       # 2° filtro (AND): richiedi questa
    recode_columns: list[str] = field(default_factory=list)      # quali colonne passare a RECODE
    decensor_biomarkers: bool = False   # ">1700"/"<200" -> numerico (file CSF)
    recompute_age: bool = False         # AGE_bl + Δtempo -> AGE per visita
    clean_fs_fields: bool = False       # FLDSTRENG/FSVERSION: estrai parte numerica
    compute_atn: bool = False           # rapporti + profilo ATN (solo file CSF)
    atn_method: str = "unknown"


ADNIMERGE = DatasetConfig(
    file_code="ADNIMERGE",
    source="ADNIMERGE_05Mar2026.csv",
    viscode_reference="VISCODE",
    essential_columns=["APOE4", "MMSE", "Ventricles", "Hippocampus", "AGE"],
    also_required=["DX"],
    recode_columns=["PTGENDER", "PTMARRY", "PTETHCAT", "PTRACCAT", "DX"],
    recompute_age=True,
    clean_fs_fields=True,
    # compute_atn resta False: nel notebook l'ATN e' solo per i file CSF, non ADNIMERGE
)


# ---------------------------------------------------------------------------
# 6. Helper derivati
# ---------------------------------------------------------------------------
def rename_map() -> dict[str, str]:
    return {name: v.rename for name, v in CATALOG.items() if v.rename}


def columns_in(parameter: str) -> list[str]:
    return [name for name, v in CATALOG.items() if v.parameter == parameter]
