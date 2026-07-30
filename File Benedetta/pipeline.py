"""
pipeline.py  —  ADNI cleaning 1 riscritto per ADNIMERGE.

E' la riscrittura del blocco ADNIMERGE di adni_cleaning1.ipynb (celle 222-229):
stessa sequenza di operazioni, ma ogni vecchia chiamata opaca dataCleaner.<x>()
e' diventata una funzione esplicita, e i valori che prima erano scritti a mano
dentro le celle arrivano da config.py.

    NOTEBOOK (dataCleaner.*)              QUI (funzione)
    -----------------------------------   ---------------------------------
    client.download_file(...)             load()               [datalake -> CSV]
    replace_unknown_values                replace_unknown()
    drop_if_all_none  x2                  drop_if_all_none()   [essential + also_required]
    to_date_format                        parse_dates()
    find_exam_code                        dedup_visits() + add_visit_month()
    add_calculated_age                    recompute_age()
    binarization_gender / categorize_*    recode()             [mappe in config.RECODE]
    FLDSTRENG/FSVERSION .str.extract      clean_fs_fields()
    new_variable_names (legge l'Excel)    rename_variables()   [mappa in config.CATALOG]
    (solo file CSF) get_ATN_profile       add_atn_profile()    [ADNIMERGE non lo usa]
    InfoSupportFile / save_df(support)    profile()            [report, si rigenera]
    client.upload_dataframe(...)          to_csv()             [datalake -> locale]

Uso:
    python3 pipeline.py                 # esegue e salva output + report
    from pipeline import run_cleaning1, profile
    df = run_cleaning1()
"""
from __future__ import annotations
import re
import numpy as np
import pandas as pd

import config
from config import DatasetConfig, ADNIMERGE

# Aggiunta Rossana
ADNIMERGE.source = "ADNIMERGE_cleaned_01.csv"
OUTPUT_FILE = "ADNIMERGE_cleaned_02.csv"

# --- funzioni atomiche: ognuna prende un DataFrame e ne restituisce uno nuovo -
def load(cfg):
    return pd.read_csv(cfg.source, low_memory=False)


#sostituisce i valori "sentinella" — cioè codici usati per rappresentare dati mancanti in modo mascherato (non un vero NaN, ma un valore convenzionale come -4, "Unknown", "N/A", 999, ecc.) — con veri valori mancanti (NaN), che pandas può gestire correttamente.
def replace_unknown(df):
    return df.replace(config.UNKNOWN_SENTINELS, np.nan)


#"ripulire" colonne numeriche che contengono simboli di censura
def decensor(df, cols):
    df = df.copy()
    for c in cols:
        if c in df.columns:
            s = df[c].astype(str).str.replace(r"^[<>]", "", regex=True)
            df[c] = pd.to_numeric(s, errors="coerce")
    return df


#elimina le righe dove tutte le colonne indicate sono vuote contemporaneamente
def drop_if_all_none(df, cols):
    present = [c for c in cols if c in df.columns]
    return df.dropna(subset=present, how="all") if present else df


#converte una o più colonne in formato data vera e propria (datetime), invece di lasciarle come semplice testo.
def parse_dates(df, cols):
    df = df.copy()
    for c in cols:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce")
    return df


#elimina le visite duplicate (stesso paziente, stessa data) tenendo però la riga più completa tra i duplicati, invece di sceglierla a caso.
def dedup_visits(df, id_col, date_col, essential):
    present = [c for c in essential if c in df.columns]
    df = df.copy()
    df["_completeness"] = df[present].notna().sum(axis=1) if present else 0
    return (df.sort_values([id_col, date_col, "_completeness"])
              .drop_duplicates(subset=[id_col, date_col], keep="last")
              .drop(columns="_completeness"))


#calcola, per ogni visita, a quanti mesi di distanza è avvenuta rispetto alla prima visita di quel paziente (il cosiddetto "baseline").
def add_visit_month(df, id_col, date_col):
    df = df.copy().sort_values([id_col, date_col])
    baseline = df.groupby(id_col)[date_col].transform("min")
    df["VISIT_MONTH"] = ((df[date_col] - baseline).dt.days / 30.44).round().astype("Int64")
    return df


#ricalcola l'età del paziente visita per visita, partendo dall'età al basale (prima visita) e sommando il tempo trascorso — invece di usare un'unica età fissa (quella al baseline) ripetuta erroneamente su tutte le visite successive.
def recompute_age(df, date_col="EXAMDATE", bl_date_col="EXAMDATE_bl", age_col="AGE"):
    if age_col not in df.columns or bl_date_col not in df.columns:
        return df
    df = df.copy().rename(columns={age_col: age_col + "_bl"})
    delta_y = (pd.to_datetime(df[date_col], errors="coerce")
               - pd.to_datetime(df[bl_date_col], errors="coerce")).dt.days / 365.25
    df[age_col] = df[age_col + "_bl"] + delta_y
    return df


#sostituisce i valori di determinate colonne con nuovi valori equivalenti, seguendo una mappatura predefinita salvata altrove (in un file/modulo config).
def recode(df, cols):
    df = df.copy()
    for c in cols:
        if c in df.columns and c in config.RECODE:
            df[c] = df[c].map(config.RECODE[c])
    return df


#ripulisce due colonne specifiche legate ai dati di risonanza magnetica processati con FreeSurfer (software comune in neuroimaging per l'analisi di risonanze cerebrali): FLDSTRENG (intensità del campo magnetico dello scanner MRI) e FSVERSION (versione del software FreeSurfer usata).
def clean_fs_fields(df):
    df = df.copy()
    if "FLDSTRENG" in df.columns:
        df["FLDSTRENG"] = df["FLDSTRENG"].astype(str).str.extract(r"([0-9.]+)", expand=False) + "T"
    if "FSVERSION" in df.columns:
        df["FSVERSION"] = df["FSVERSION"].astype(str).str.extract(r"([0-9.]+)", expand=False)
    return df


#rinomina le colonne del DataFrame usando una mappa di corrispondenze (vecchio nome → nuovo nome) definita centralmente in config.py.
def rename_variables(df):
    return df.rename(columns=config.rename_map())


#crea nuove colonne calcolando dei rapporti (ratio) tra biomarcatori del liquido cerebrospinale (CSF, Cerebrospinal Fluid) — misure molto usate negli studi sull'Alzheimer come ADNI.
def add_ratios(df):
    df = df.copy()
    for name, (num, den) in {"TTAU_AB42_CSF": ("TTAU_CSF", "AB42_CSF"),
                             "PT181_AB42_CSF": ("PT181_CSF", "AB42_CSF")}.items():
        if num in df.columns and den in df.columns:
            df[name] = df[num] / df[den]
    return df


#calcola il profilo ATN del paziente — un framework clinico standard usato negli studi sull'Alzheimer per classificare i pazienti in base alla presenza di tre tipi di biomarcatori: Amiloide, Tau, Neurodegenerazione.
def add_atn_profile(df, method):
    df = df.copy()
    axes = {"A": ("AB42_CSF", "below"), "T": ("PT181_CSF", "above"), "N": ("TTAU_CSF", "above")}
    flags = {}
    for axis, (var, direction) in axes.items():
        thr = config.cutoff(var, method)
        if var in df.columns and thr is not None:
            pos = df[var] < thr if direction == "below" else df[var] > thr
            flags[axis] = np.where(df[var].isna(), np.nan, pos.astype(float))
    if not flags:
        raise RuntimeError(f"compute_atn=True ma nessun asse calcolabile (metodo '{method}').")
    for axis, name in [("A", "Apositive"), ("T", "Tpositive"), ("N", "Npositive")]:
        if axis in flags:
            df[name] = flags[axis]
    df["ATN_PROFILE"] = df.apply(
        lambda r: "".join(f"{a}{'+' if r.get(n) == 1 else '-'}"
                          for a, n in [("A", "Apositive"), ("T", "Tpositive"), ("N", "Npositive")]
                          if n in df.columns and not pd.isna(r.get(n))) or np.nan, axis=1)
    return df


# --- orchestratore: l'ex "adni_cleaning1" per un file, leggibile in un colpo --
#è l'orchestratore principale della pipeline di data cleaning: chiama in sequenza tutte le funzioni che abbiamo analizzato finora, componendole in un unico flusso completo e configurabile.
def run_cleaning1(cfg: DatasetConfig = ADNIMERGE) -> pd.DataFrame:
    df = load(cfg)                                                # download -> CSV
    df = replace_unknown(df)                                      # replace_unknown_values
    if cfg.decensor_biomarkers:
        df = decensor(df, config.columns_in("Biomarker"))
    df = drop_if_all_none(df, cfg.essential_columns)             # 1° drop: colonne importanti
    df = drop_if_all_none(df, cfg.also_required)                 # 2° drop: DX obbligatoria
    df = parse_dates(df, [cfg.date_column])                      # to_date_format
    df = dedup_visits(df, cfg.id_column, cfg.date_column, cfg.essential_columns)
    df = add_visit_month(df, cfg.id_column, cfg.date_column)     # find_exam_code -> VISIT_MONTH
    if cfg.recompute_age:
        df = recompute_age(df, cfg.date_column)                  # add_calculated_age
    df = recode(df, cfg.recode_columns)                          # categorize_*
    if cfg.clean_fs_fields:
        df = clean_fs_fields(df)                                 # FLDSTRENG/FSVERSION
    df = rename_variables(df)                                     # new_variable_names
    if cfg.compute_atn:                                          # solo file CSF
        df = add_ratios(df)
        df = add_atn_profile(df, cfg.atn_method)
    return df


# --- report: rigenera cio' che prima era l'Excel _statistics (output, non input)
#genera un report riepilogativo (profilazione) di tutte le colonne del dataset, riga per colonna, includendo anche un'analisi per coorte di studio — molto utile come passaggio finale dopo la pipeline di cleaning, per avere una visione d'insieme della qualità dei dati.
def profile(df, cohort_col="COLPROT") -> pd.DataFrame:
    rows, n = [], len(df)
    cohorts = df[cohort_col].dropna().unique().tolist() if cohort_col in df else []
    for col in df.columns:
        s = df[col]
        n_valid = int(s.notna().sum())
        is_num = pd.api.types.is_numeric_dtype(s)
        rows.append({
            "variable": col,
            "type": s.dtype.name,
            "range": f"{s.min()}, {s.max()}" if is_num and n_valid else "",
            "valid_values": n_valid,
            "missing_values": n - n_valid,
            "missing_pop": ", ".join(c for c in cohorts
                                     if df.loc[df[cohort_col] == c, col].notna().sum() == 0),
            "del": "keep" if n and n_valid / n >= config.MISSING_KEEP_THRESHOLD else "drop",
        })
    return pd.DataFrame(rows)


#il blocco di esecuzione principale dello script: il codice che viene effettivamente eseguito quando lanci il file .py direttamente (non quando viene importato come modulo in un altro script).
if __name__ == "__main__":
    df = run_cleaning1()
    print(f"cleaning1 ADNIMERGE: {df.shape[0]} righe x {df.shape[1]} colonne")
    df.to_csv("ADNIMERGE_cleaned_01.csv", index=False)           # ex upload level='cleaned_01'
    profile(df).to_csv("ADNIMERGE_report.csv", index=False)      # ex support file statistics
    print("scritti: ADNIMERGE_cleaned_01.csv, ADNIMERGE_report.csv")

#ROSSANA
### Funzione da richiamare per salvare le modifiche su ADNIMERGE_cleaned_02.csv
def save_dataset(df, path):
   df.to_csv(path, index=False)
   print(f"Salvato: {path}  (shape: {df.shape})")

### Rimozione colonne con troppi valori non validi per l'analizi
# Funzione di pulizia colonne. Calcola, per ogni colonna, la percentuale di valori validi e scarta quelle sotto la soglia definita in config.MISSING_KEEP_THRESHOLD.
def remove_param_few_subjects(df, threshold=config.MISSING_KEEP_THRESHOLD):
    df = df.copy()
    valid_ratio = df.notna().mean()
    dropped = valid_ratio[valid_ratio < threshold].index.tolist()
    df = df.drop(columns=dropped)
    return df, dropped

##Esecuzione dello step. Legge il file originale, applica la pulizia, stampa quali colonne sono state scartate e la variazione di shape, poi salva il risultato con save_dataset().
df_raw = pd.read_csv(ADNIMERGE.source)

df_cleaned, dropped_columns = remove_param_few_subjects(df_raw)
 
print(f"[STEP 1] Colonne scartate ({len(dropped_columns)}): {dropped_columns}")
print(f"[STEP 1] Shape: {df_raw.shape} -> {df_cleaned.shape}")
 
save_dataset(df_cleaned, OUTPUT_FILE)  

###Conversione in dummy delle colonne 'GENDER', 'MARRY', 'ETHNICITY', 'RACE', 'DX'
## Configurazione dello step. Definisce input/output (il file appena prodotto dallo STEP 1) e l'elenco delle variabili categoriche da convertire.
DUMMY_INPUT = OUTPUT_FILE             # <-- usa direttamente l'output dello step 1
DUMMY_OUTPUT = "ADNIMERGE_cleaned_02.csv"

REF_LIST = ['GENDER', 'MARRY', 'ETHNICITY', 'RACE', 'DX']

##Funzione di conversione in dummy. Individua tra ref_list le colonne presenti nel dataframe e le trasforma in variabili binarie con pd.get_dummies.
def classes_to_dummies(df, ref_list):
    df = df.copy()
    to_dummy_list = [c for c in ref_list if c in df.columns]
    if to_dummy_list:
        df = pd.get_dummies(df, columns=to_dummy_list, dtype=int)
    return df, to_dummy_list

##Funzione di conteggio dummy. Conta quante colonne dummy sono state create in totale e quante per ciascuna variabile originale.
def count_dummy_columns(original_df, final_df, converted_columns):
    new_dummy_columns = [c for c in final_df.columns if c not in original_df.columns]
    per_column_count = {
        col: len([c for c in new_dummy_columns if c.startswith(col + "_")])
        for col in converted_columns
    }
    return len(new_dummy_columns), per_column_count

#Controllo di sicurezza pre-esecuzione. Legge il file d'ingresso e verifica che abbia già il numero di colonne atteso dallo STEP 1 (72), bloccando l'esecuzione con un messaggio chiaro se non è così.
df_step2 = pd.read_csv(DUMMY_INPUT)

assert df_step2.shape[1] == df_cleaned.shape[1], (
    f"[STEP 2] Attenzione: '{DUMMY_INPUT}' ha {df_step2.shape[1]} colonne, "
    f"attese {df_cleaned.shape[1]}. Rieseguire lo STEP 1 prima di procedere."
)

##Esecuzione e salvataggio. Applica la conversione in dummy e salva il risultato con save_dataset().
final_df, converted_columns = classes_to_dummies(df_step2, ref_list=REF_LIST)

save_dataset(final_df, DUMMY_OUTPUT)

###Rimozione righe in cui tutte le colonne chiave sono vuote
KEY_COLUMNS = ['Ventricles', 'Hippocampus', 'WholeBrain', 'ICV']

##Funzione di filtro sulle righe
def drop_if_all_none(df, key_columns):
    df = df.copy()
    cols_present = [c for c in key_columns if c in df.columns]
    mask_all_none = df[cols_present].isna().all(axis=1)
    dropped_rows = int(mask_all_none.sum())
    df = df[~mask_all_none]
    return df, dropped_rows

##Caricamento e applicazione del filtro
df_step3 = pd.read_csv(OUTPUT_FILE)
df_final, dropped_rows = drop_if_all_none(df_step3, KEY_COLUMNS)

save_dataset(df_final, OUTPUT_FILE)

###Riallineamento types delle colonne
##Funzione di riallineamento che controllo ogni colonna
def realign_column_types(df):
    """Ispeziona ogni colonna e la riallinea al tipo corretto (int, float o testo)."""
    df = df.copy()
    type_report = {}

    for col in df.columns:
        original_dtype = str(df[col].dtype)

        # Prova la conversione numerica; se fallisce, la colonna resta testo
        converted = pd.to_numeric(df[col], errors='coerce')
        is_fully_numeric = converted.notna().sum() == df[col].notna().sum()

        if is_fully_numeric:
            if (converted.dropna() % 1 == 0).all():
                df[col] = converted.astype('Int64')   # int nullable, gestisce i NaN
                new_dtype = 'Int64'
            else:
                df[col] = converted.astype('float64')
                new_dtype = 'float64'
        else:
            df[col] = df[col].astype(str).where(df[col].notna(), np.nan)
            new_dtype = 'str'

        if original_dtype != new_dtype:
            type_report[col] = (original_dtype, new_dtype)

    return df, type_report

final_df = pd.read_csv(OUTPUT_FILE)
final_df, type_report = realign_column_types(final_df)

save_dataset(final_df, OUTPUT_FILE)

### Visualizzaszione degli Outliers + conteggio per ogni colonna analizzata
COLUMNS = [
    'APOE4', 'CDRSB', 'ADAS11', 'ADAS13', 'ADASQ4', 'MMSE', 'RAVLT_immediate',
    'RAVLT_learning', 'RAVLT_forgetting', 'RAVLT_perc_forgetting', 'LDELTOTAL',
    'TRABSCOR', 'FAQ', 'FSVERSION', 'IMAGEUID', 'Ventricles', 'Hippocampus',
    'WholeBrain', 'Entorhinal', 'Fusiform', 'MidTemp', 'ICV', 'mPACCdigit',
    'mPACCtrailsB', 'EXAMDATE_bl', 'CDRSB_bl', 'ADAS11_bl', 'ADAS13_bl',
    'ADASQ4_bl', 'MMSE_bl', 'RAVLT_immediate_bl', 'RAVLT_learning_bl',
    'RAVLT_forgetting_bl', 'RAVLT_perc_forgetting_bl', 'LDELTOTAL_BL',
    'TRABSCOR_bl', 'FAQ_bl', 'mPACCdigit_bl', 'mPACCtrailsB_bl', 'FLDSTRENG_bl',
    'FSVERSION_bl', 'IMAGEUID_bl', 'Ventricles_bl', 'Hippocampus_bl',
    'WholeBrain_bl', 'Entorhinal_bl', 'Fusiform_bl', 'MidTemp_bl', 'ICV_bl',
    'FDG_bl'
]

#Conta gli outlier di una colonna numerica con il metodo IQR (1.5 * IQR oltre Q1/Q3).
def count_outliers_iqr(series):
    data = series.dropna()
    q1, q3 = data.quantile(0.25), data.quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    n_outliers = int(((data < lower_bound) | (data > upper_bound)).sum())
    return n_outliers

#Calcola gli outlier IQR per l'elenco di colonne fornito, senza generare grafici.
#Le colonne non numeriche o assenti vengono segnalate a parte.
def count_outliers_for_columns(df, columns):
    df = df.copy()
    outlier_counts = {}
    skipped_columns = {}

    for col in columns:
        if col not in df.columns:
            skipped_columns[col] = "assente nel dataset"
            continue
        if not pd.api.types.is_numeric_dtype(df[col]):
            skipped_columns[col] = "non numerica"
            continue
        outlier_counts[col] = count_outliers_iqr(df[col])

    return outlier_counts, skipped_columns

df = pd.read_csv(OUTPUT_FILE, low_memory=False)
outlier_counts, skipped_columns = count_outliers_for_columns(df, COLUMNS)

###Mantiene le colonne presenti in COLONNE_CHIARA(excludendo quelle generate dal codice precedentemente)
#Elenco di riferimento fornito da confrontare con le colonne effettive del dataset
COLONNE_CHIARA = [
    'RID', 'COLPROT', 'VISCODE', 'EXAMDATE', 'AGE', 'PTGENDER', 'PTEDUCAT',
    'PTETHCAT', 'PTRACCAT', 'PTMARRY', 'APOE4', 'CDRSB', 'ADAS11', 'ADAS13',
    'MMSE', 'RAVLT_immediate', 'FAQ', 'MOCA', 'FLDSTRENG', 'FSVERSION',
    'IMAGEUID', 'Ventricles', 'Hippocampus', 'Entorhinal', 'Fusiform',
    'MidTemp', 'ICV', 'DX', 'update_stamp'
]

#Colonne aggiuntive da mantenere comunque (dummy + variabile di visita), anche se non presenti in COLONNE_CHIARA
COLONNE_EXTRA_DA_MANTENERE = [
    'VISIT_MONTH', 'AGE', 'GENDER_0', 'GENDER_1',
    'MARRY_0.0', 'MARRY_1.0', 'MARRY_2.0', 'MARRY_3.0',
    'ETHNICITY_0.0', 'ETHNICITY_1.0',
    'RACE_0.0', 'RACE_1.0', 'RACE_2.0', 'RACE_3.0', 'RACE_4.0', 'RACE_5.0',
    'DX_0', 'DX_1', 'DX_2'
]

#Mantiene solo le colonne presenti in reference_columns (più eventuali colonne extra da conservare comunque), scartando tutte le altre
def keep_only_reference_columns(df, reference_columns, extra_columns=None):
    df = df.copy()
    extra_columns = extra_columns or []

    # Unisce l'elenco di riferimento con le colonne extra, senza duplicati
    columns_to_keep_full = list(dict.fromkeys(reference_columns + extra_columns))

    cols_to_keep = [c for c in columns_to_keep_full if c in df.columns]
    missing_in_dataset = [c for c in columns_to_keep_full if c not in df.columns]
    dropped_columns = [c for c in df.columns if c not in columns_to_keep_full]

    df = df[cols_to_keep]
    return df, dropped_columns, missing_in_dataset

df_step_chiara = pd.read_csv(OUTPUT_FILE, low_memory=False)
df_chiara, dropped_columns, missing_in_dataset = keep_only_reference_columns(
    df_step_chiara, COLONNE_CHIARA, COLONNE_EXTRA_DA_MANTENERE
)

save_dataset(df_chiara, OUTPUT_FILE)

