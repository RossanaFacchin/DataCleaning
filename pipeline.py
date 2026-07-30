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


# --- funzioni atomiche: ognuna prende un DataFrame e ne restituisce uno nuovo -
def load(cfg):
    return pd.read_csv(cfg.source, low_memory=False)


def replace_unknown(df):
    return df.replace(config.UNKNOWN_SENTINELS, np.nan)


def decensor(df, cols):
    df = df.copy()
    for c in cols:
        if c in df.columns:
            s = df[c].astype(str).str.replace(r"^[<>]", "", regex=True)
            df[c] = pd.to_numeric(s, errors="coerce")
    return df


def drop_if_all_none(df, cols):
    present = [c for c in cols if c in df.columns]
    return df.dropna(subset=present, how="all") if present else df


def parse_dates(df, cols):
    df = df.copy()
    for c in cols:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce")
    return df


def dedup_visits(df, id_col, date_col, essential):
    present = [c for c in essential if c in df.columns]
    df = df.copy()
    df["_completeness"] = df[present].notna().sum(axis=1) if present else 0
    return (df.sort_values([id_col, date_col, "_completeness"])
              .drop_duplicates(subset=[id_col, date_col], keep="last")
              .drop(columns="_completeness"))


def add_visit_month(df, id_col, date_col):
    df = df.copy().sort_values([id_col, date_col])
    baseline = df.groupby(id_col)[date_col].transform("min")
    df["VISIT_MONTH"] = ((df[date_col] - baseline).dt.days / 30.44).round().astype("Int64")
    return df


def recompute_age(df, date_col="EXAMDATE", bl_date_col="EXAMDATE_bl", age_col="AGE"):
    if age_col not in df.columns or bl_date_col not in df.columns:
        return df
    df = df.copy().rename(columns={age_col: age_col + "_bl"})
    delta_y = (pd.to_datetime(df[date_col], errors="coerce")
               - pd.to_datetime(df[bl_date_col], errors="coerce")).dt.days / 365.25
    df[age_col] = df[age_col + "_bl"] + delta_y
    return df


def recode(df, cols):
    df = df.copy()
    for c in cols:
        if c in df.columns and c in config.RECODE:
            df[c] = df[c].map(config.RECODE[c])
    return df


def clean_fs_fields(df):
    df = df.copy()
    if "FLDSTRENG" in df.columns:
        df["FLDSTRENG"] = df["FLDSTRENG"].astype(str).str.extract(r"([0-9.]+)", expand=False) + "T"
    if "FSVERSION" in df.columns:
        df["FSVERSION"] = df["FSVERSION"].astype(str).str.extract(r"([0-9.]+)", expand=False)
    return df


def rename_variables(df):
    return df.rename(columns=config.rename_map())


def add_ratios(df):
    df = df.copy()
    for name, (num, den) in {"TTAU_AB42_CSF": ("TTAU_CSF", "AB42_CSF"),
                             "PT181_AB42_CSF": ("PT181_CSF", "AB42_CSF")}.items():
        if num in df.columns and den in df.columns:
            df[name] = df[num] / df[den]
    return df


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


if __name__ == "__main__":
    df = run_cleaning1()
    print(f"cleaning1 ADNIMERGE: {df.shape[0]} righe x {df.shape[1]} colonne")
    df.to_csv("ADNIMERGE_cleaned_01.csv", index=False)           # ex upload level='cleaned_01'
    profile(df).to_csv("ADNIMERGE_report.csv", index=False)      # ex support file statistics
    print("scritti: ADNIMERGE_cleaned_01.csv, ADNIMERGE_report.csv")
