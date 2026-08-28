"""
pipeline.py  —  ADNI cleaning 1 + 2 riscritto per ADNIMERGE.

E' la riscrittura dei blocchi ADNIMERGE dei notebook adni_cleaning*.ipynb:
stessa sequenza di operazioni, ma ogni vecchia chiamata opaca dataCleaner.<x>()
e' diventata una funzione esplicita, e i valori che prima erano scritti a mano
dentro le celle arrivano da config.py.

    NOTEBOOK (dataCleaner.*)              QUI (funzione)
    -----------------------------------   ---------------------------------
    -- cleaning 1 --
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
    -- cleaning 2 / 3 --
    remove_param_few_subjects             drop_sparse_columns()
    remove_sub_1visit                     remove_single_visit_subjects()
    classes_to_dummies                    make_dummies()
    drop_if_all_none (volumi)             drop_if_all_none()   [riuso: volume_row_keys]
    transform_volumes_as_ICV_percent      normalize_volumes_icv()
    filtro colonne finali                 keep_only_columns()
    -- report --
    InfoSupportFile / save_df(support)    profile()            [report, si rigenera]
    client.upload_dataframe(...)          to_csv()             [datalake -> locale]

Contratto del modulo:
    * NESSUN codice esegue I/O al momento dell'import: si puo' fare
        from pipeline import run_cleaning1, run_cleaning2, profile
      senza leggere o scrivere nulla.
    * Ogni funzione prende un DataFrame e ne restituisce uno nuovo (niente
      stato globale, niente rilettura da disco tra un passo e l'altro).
    * L'unico punto che tocca il disco e' il blocco __main__ (e save_dataset).

Uso:
    python3 pipeline.py                 # esegue cleaning1 -> cleaning2 e salva output + report
    from pipeline import run_cleaning1, run_cleaning2
    df1 = run_cleaning1()
    df2, log = run_cleaning2(df1)
"""
from __future__ import annotations
import numpy as np
import pandas as pd

import config
from config import DatasetConfig, ADNIMERGE, PTDEMOG


# ===========================================================================
# CLEANING 1  —  funzioni atomiche: ognuna prende un DataFrame e ne restituisce
#               uno nuovo. Nessun effetto collaterale.
# ===========================================================================
def load(cfg):
    """Legge il file grezzo (ex download dal datalake)."""
    return pd.read_csv(cfg.source, low_memory=False)


def replace_unknown(df):
    """Sostituisce i sentinella di missing (-4, 'Unknown', 9999...) con NaN veri."""
    return df.replace(config.UNKNOWN_SENTINELS, np.nan)


def decensor(df, cols):
    """Toglie i simboli di censura (">1700", "<200") e converte a numerico (file CSF)."""
    df = df.copy()
    for c in cols:
        if c in df.columns:
            s = df[c].astype(str).str.replace(r"^[<>]", "", regex=True)
            df[c] = pd.to_numeric(s, errors="coerce")
    return df


def drop_if_all_none(df, cols):
    """Scarta le righe in cui TUTTE le colonne indicate sono NaN. Restituisce un DataFrame.

    Nota: unica definizione, usata sia in cleaning 1 (colonne essenziali / DX) sia in
    cleaning 2 (chiavi volume). Il conteggio delle righe rimosse lo fa l'orchestratore
    confrontando len(df) prima/dopo: cosi' la funzione mantiene un contratto solo
    (df -> df) e non va ridefinita con firme diverse.
    """
    present = [c for c in cols if c in df.columns]
    return df.dropna(subset=present, how="all") if present else df


def parse_dates(df, cols): # cols: da aggiungere la variabili PTDOP, updatestamp controlare in che formato è, senza creare problemi
    """Converte le colonne indicate in datetime vero."""
    df = df.copy()
    for c in cols:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce")
    return df


def dedup_visits(df, id_col, date_col, essential):
    """Elimina le visite duplicate (stesso paziente, stessa data) tenendo la riga piu' completa."""
    present = [c for c in essential if c in df.columns]
    df = df.copy()
    df["_completeness"] = df[present].notna().sum(axis=1) if present else 0
    return (df.sort_values([id_col, date_col, "_completeness"])
              .drop_duplicates(subset=[id_col, date_col], keep="last")
              .drop(columns="_completeness"))


def add_visit_month(df, id_col, date_col):
    """VISIT_MONTH = mesi trascorsi dalla prima visita (baseline) del paziente."""
    df = df.copy().sort_values([id_col, date_col])
    baseline = df.groupby(id_col)[date_col].transform("min")
    df["VISIT_MONTH"] = ((df[date_col] - baseline).dt.days / 30.44).round().astype("Int64")
    return df


def recompute_age(df, date_col="EXAMDATE", bl_date_col="EXAMDATE_bl", age_col="AGE"): # aggiungere un calcolo diverso per PTDEMOG(usare l'if)
    """AGE (fissa al baseline) -> AGE_bl; nuova AGE = AGE_bl + tempo trascorso per visita."""
    # def recompute_age(df, date_col="EXAMDATE", bl_date_col="EXAMDATE_bl", age_col="AGE",
    #                dob_col="PTDOP", visit_date_col="VISDATE"):
    # """AGE (fissa al baseline) -> AGE_bl; nuova AGE = AGE_bl + tempo trascorso per visita.

    # Se il dataset ha dob_col e visit_date_col (caso PTDEMOG), AGE si calcola
    # direttamente come (VISDATE - PTDOP) in anni, invece che per accumulo dal baseline.
    # """
    # df = df.copy()

    # if dob_col in df.columns and visit_date_col in df.columns:
    #     dob = pd.to_datetime(df[dob_col], format="%m/%Y", errors="coerce")
    #     visit = pd.to_datetime(df[visit_date_col], errors="coerce")
    #     df[age_col] = (visit - dob).dt.days / 365.25
    #     return df
    if age_col not in df.columns or bl_date_col not in df.columns:
        return df
    df = df.copy().rename(columns={age_col: age_col + "_bl"})
    delta_y = (pd.to_datetime(df[date_col], errors="coerce")
               - pd.to_datetime(df[bl_date_col], errors="coerce")).dt.days / 365.25
    df[age_col] = df[age_col + "_bl"] + delta_y
    return df


def recode(df, cols):
    """Stringa categorica -> codice numerico, secondo le mappe in config.RECODE."""
    df = df.copy()
    for c in cols:
        if c in df.columns and c in config.RECODE:
            df[c] = df[c].map(config.RECODE[c])
    return df


def clean_fs_fields(df):
    """Estrae la parte numerica di FLDSTRENG ('1.5T'/'3T') e FSVERSION."""
    df = df.copy()
    if "FLDSTRENG" in df.columns:
        df["FLDSTRENG"] = df["FLDSTRENG"].astype(str).str.extract(r"([0-9.]+)", expand=False) + "T"
    if "FSVERSION" in df.columns:
        df["FSVERSION"] = df["FSVERSION"].astype(str).str.extract(r"([0-9.]+)", expand=False)
    return df


def rename_variables(df, cfg):
    """Rinomina nei nomi standard: CATALOG globale + override per-file (cfg.rename)."""
    return df.rename(columns=cfg.effective_rename())


def add_constant_columns(df, mapping):
    """Stampa colonne-costante (es. il metodo/assay del file). ARMONIZZAZIONE."""
    if not mapping:
        return df
    df = df.copy()
    for col, value in mapping.items():
        df[col] = value
    return df


def add_derived_ratios(df, ratios):
    """Rapporti generici {nome: (num, den)} in nomi standard (es. AB42/AB40)."""
    if not ratios:
        return df
    df = df.copy()
    for name, (num, den) in ratios.items():
        if num in df.columns and den in df.columns:
            df[name] = pd.to_numeric(df[num], errors="coerce") / pd.to_numeric(df[den], errors="coerce")
    return df


def add_atn_profile(df, cfg):
    """Profilo ATN (Amiloide/Tau/Neurodegenerazione) sulle soglie di cutoffs.json.

    Gli assi (quale marcatore e in che verso per A/T/N) arrivano da cfg.atn_axes
    -> data-driven: lo stesso codice vale per CSF, plasma o PET, cambia solo il
    dizionario di assi nel config. Il metodo/assay e' cfg.atn_method.
    """
    df = df.copy()
    axes = cfg.atn_axes or config.ATN_AXES_CSF
    method = cfg.atn_method
    flags = {}
    for axis, (var, direction) in axes.items():
        thr = config.cutoff(var, method)
        if var in df.columns and thr is not None:
            pos = df[var] < thr if direction == "below" else df[var] > thr
            flags[axis] = np.where(df[var].isna(), np.nan, pos.astype(float))
    if not flags:
        raise RuntimeError(f"compute_atn=True ma nessun asse calcolabile (metodo '{method}').")
    axis_names = [(a, f"{a}positive") for a in axes]
    for axis, name in axis_names:
        if axis in flags:
            df[name] = flags[axis]
    df["ATN_PROFILE"] = df.apply(
        lambda r: "".join(f"{a}{'+' if r.get(n) == 1 else '-'}"
                          for a, n in axis_names
                          if n in df.columns and not pd.isna(r.get(n))) or np.nan, axis=1)
    return df


def run_cleaning1(cfg: DatasetConfig = ADNIMERGE) -> pd.DataFrame:
    """Orchestratore di cleaning 1: raw -> dataframe pulito (in memoria, niente I/O)."""
    df = load(cfg)                                                # download -> CSV
    df = replace_unknown(df)                                      # replace_unknown_values
    if cfg.decensor_biomarkers:
        df = decensor(df, cfg.decensor_columns or config.columns_in("Biomarker"))
    df = drop_if_all_none(df, cfg.essential_columns)             # 1° drop: colonne importanti
    df = drop_if_all_none(df, cfg.also_required)                 # 2° drop: DX obbligatoria
    df = rename_variables(df, cfg)                               # new_variable_names (+ override per-file)
    df = parse_dates(df, [cfg.date_column])                      # to_date_format
    df = dedup_visits(df, cfg.id_column, cfg.date_column, cfg.essential_columns)
    df = add_visit_month(df, cfg.id_column, cfg.date_column)     # find_exam_code -> VISIT_MONTH
    if cfg.recompute_age:
        df = recompute_age(df, cfg.date_column)                  # add_calculated_age
    df = recode(df, cfg.recode_columns)                          # categorize_*
    if cfg.clean_fs_fields:
        df = clean_fs_fields(df)                                 # FLDSTRENG/FSVERSION
    df = add_constant_columns(df, cfg.constant_columns)         # stampa il metodo/assay (armonizzazione)
    df = add_derived_ratios(df, cfg.derived_ratios)             # rapporti generici (es. AB42/AB40)
    if cfg.compute_atn:                                        # file con profilo ATN (CSF/plasma/PET)
        df = add_atn_profile(df, cfg)
    return df


# ===========================================================================
# CLEANING 2 / 3  —  ex notebook adni_cleaning2 / adni_cleaning3 per ADNIMERGE.
#                    Stesso stile: funzioni pure (df -> df) + orchestratore.
# ===========================================================================
def drop_sparse_columns(df, threshold=None):
    """Scarta le colonne con quota di validi sotto la soglia (ex remove_param_few_subjects).

    Usa SPARSE_KEEP_THRESHOLD (azione distruttiva), NON MISSING_KEEP_THRESHOLD
    che serve solo a etichettare il report. Restituisce (df, colonne_scartate).
    """
    threshold = config.SPARSE_KEEP_THRESHOLD if threshold is None else threshold
    valid_ratio = df.notna().mean()
    dropped = valid_ratio[valid_ratio < threshold].index.tolist()
    return df.drop(columns=dropped), dropped


def remove_single_visit_subjects(df, id_col, min_multivisit_subjects=None, force=False):
    """Scarta i soggetti con una sola visita (ex remove_sub_1visit).

    Se i soggetti con >1 visita sono meno di `min_multivisit_subjects`, il file e'
    considerato 'single visit' e NON si scarta nulla (salvo force=True, che riproduce
    l'eccezione dei file anagrafici/genetici PTDEMOG/APOERES). Restituisce (df, info).
    """
    if min_multivisit_subjects is None:
        min_multivisit_subjects = config.MULTIVISIT_MIN_SUBJECTS
    visits_per_subject = df.groupby(id_col)[id_col].transform("size")
    n_multivisit = int((df.groupby(id_col).size() > 1).sum())
    info = {"n_multivisit_subjects": n_multivisit, "applied": False}
    if n_multivisit < min_multivisit_subjects and not force:
        return df, info                       # trattato come single-visit: intatto
    info["applied"] = True
    return df[visits_per_subject > 1].copy(), info


def make_dummies(df, cols):
    """One-hot delle colonne categoriche presenti (ex classes_to_dummies).

    Prima cast a Int64 nullable, cosi' i suffissi sono interi puliti ('DX_0', non 'DX_0.0')
    e i NaN NON generano una colonna dummy. Restituisce (df, colonne_dummy_create).
    """
    df = df.copy()
    present = [c for c in cols if c in df.columns]
    for c in present:
        try:
            df[c] = df[c].astype("Int64")
        except (TypeError, ValueError):
            pass
    before = set(df.columns)
    if present:
        df = pd.get_dummies(df, columns=present, dtype=int)
    created = [c for c in df.columns if c not in before]
    return df, created


def normalize_volumes_icv(df, icv_column="ICV", vol_columns=None):
    """Normalizza i volumi cerebrali come percentuale di ICV (ex transform_volumes_as_ICV_percent).

    NB: NON somma sinistro+destro (get_volumes_total): in ADNIMERGE i volumi sono gia'
    totali a colonna singola. Restituisce un DataFrame.
    """
    df = df.copy()
    if vol_columns is None:
        vol_columns = config.volume_columns(icv_column)
    if icv_column not in df.columns:
        return df
    icv = pd.to_numeric(df[icv_column], errors="coerce")
    for c in vol_columns:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce") / icv * 100.0
    return df


def keep_only_columns(df, keep, extra=None):
    """Tiene solo le colonne in `keep` (+ `extra`) effettivamente presenti.

    Restituisce (df, colonne_scartate, colonne_richieste_ma_assenti).
    """
    extra = extra or []
    wanted = list(dict.fromkeys(list(keep) + list(extra)))     # unione senza duplicati, ordine stabile
    present = [c for c in wanted if c in df.columns]
    missing = [c for c in wanted if c not in df.columns]
    dropped = [c for c in df.columns if c not in wanted]
    return df[present], dropped, missing

# def drop_columns(df, drop):
#     """Rimuove le colonne in `drop`, se presenti.
# 
#     Restituisce (df, colonne_rimosse, colonne_richieste_ma_assenti).
#     """
#     drop = list(dict.fromkeys(drop))                       # niente duplicati, ordine stabile
#     present = [c for c in drop if c in df.columns]
#     missing = [c for c in drop if c not in df.columns]
#     return df.drop(columns=present), present, missing


def run_cleaning2(df: pd.DataFrame, cfg: DatasetConfig = ADNIMERGE):
    """Orchestratore di cleaning 2/3: dataframe cleaned_01 -> cleaned_02 (in memoria).

    Riceve il DataFrame in input (NON rilegge da disco) e restituisce (df, log),
    dove log e' un dizionario di conteggi utile per la stampa nel __main__.
    """
    log = {}
    r0, c0 = df.shape

    if cfg.drop_sparse_columns:
        df, dropped = drop_sparse_columns(df)
        log["colonne_scartate_sparse"] = dropped

    if cfg.remove_single_visit:
        n_before = len(df)
        df, info = remove_single_visit_subjects(
            df, cfg.id_column, force=cfg.keep_even_single_visit)
        log["single_visit"] = {**info, "righe_rimosse": n_before - len(df)}

    created = []
    if cfg.make_dummies:
        df, created = make_dummies(df, cfg.dummy_columns)
        log["dummy_create"] = created

    if cfg.volume_row_keys:
        n_before = len(df)
        df = drop_if_all_none(df, cfg.volume_row_keys)          # riuso della funzione di cleaning 1
        log["righe_rimosse_volumi"] = n_before - len(df)

    if cfg.normalize_icv:
        df = normalize_volumes_icv(df, cfg.icv_column)
        log["icv_normalizzato"] = True

    if cfg.keep_columns:
        # le dummy generate e le colonne calcolate si tengono in automatico:
        # NON vanno elencate a mano nel config.
        engineered = [c for c in ("VISIT_MONTH", "AGE_bl") if c in df.columns]
        df, dropped_cols, missing_cols = keep_only_columns(
            df, cfg.keep_columns, extra=created + engineered)
        log["colonne_scartate_finali"] = dropped_cols
        log["colonne_richieste_assenti"] = missing_cols

    log["shape_iniziale"] = (r0, c0)
    log["shape_finale"] = df.shape
    return df, log


def run_cleaning(cfg: DatasetConfig):
    """Comodita': cleaning1 + cleaning2 in memoria per un cfg qualsiasi. Restituisce (df, log)."""
    return run_cleaning2(run_cleaning1(cfg), cfg)


# ===========================================================================
# MERGE per categoria (v0)  —  motore generico guidato da config.CATEGORY_MERGE.
#   Fa SOLO il match di visita entro buffer + applica una strategia sui metodi.
#   Le REGOLE di conflitto sono decisioni (Chiara): stanno nel MergeConfig, non qui.
# ===========================================================================
def _match_within_buffer(base, other, keys, buffer_days):
    """Allinea `other` a `base` sulle stesse chiavi, tollerando EXAMDATE entro buffer_days.

    Assunzione: keys = ['RID', <date_col>]. Match esatto su RID, poi la data piu'
    vicina entro il buffer (una riga di other usata al massimo una volta).
    Restituisce other reindicizzato sull'indice di base (NaN dove non c'e' match).
    """
    id_col, date_col = keys[0], keys[1]
    base = base.copy()
    other = other.copy()
    base[date_col] = pd.to_datetime(base[date_col], errors="coerce")
    other[date_col] = pd.to_datetime(other[date_col], errors="coerce")
    used = set()
    rows = []
    for idx, b in base.iterrows():
        cand = other[(other[id_col] == b[id_col]) & (~other.index.isin(used))]
        if len(cand):
            dist = (cand[date_col] - b[date_col]).abs()
            near = dist[dist <= pd.Timedelta(days=buffer_days)]
            if len(near):
                j = near.idxmin()
                used.add(j)
                rows.append(other.loc[j])
                continue
        rows.append(pd.Series(index=other.columns, dtype="object"))
    aligned = pd.DataFrame(rows, index=base.index)
    return aligned


def merge_category(datasets: dict, category: str, mcfg=None):
    """Fonde i file puliti di una categoria in un unico DataFrame, config-driven.

    `datasets`: {file_code: dataframe_pulito}. Usa CATEGORY_MERGE[category] per
    buffer, colonna-metodo e strategia. Ritorna (df_merged, log).

    strategy:
      'suffix_by_method' -> misure omonime da metodi diversi -> colonne separate
                            (<var>_<metodo>): nessuna perdita, nessun pooling indebito.
    """
    mcfg = mcfg or config.CATEGORY_MERGE[category]
    keys = mcfg.join_keys
    items = list(datasets.items())
    base_code, base = items[0]
    base = base.copy()
    log = {"base": base_code, "aggiunti": [], "strategy": mcfg.strategy}

    for code, other in items[1:]:
        aligned = _match_within_buffer(base, other, keys, mcfg.buffer_days)
        # colonne da portare dentro (escludo le chiavi, gia' presenti nel base)
        bring = [c for c in other.columns if c not in keys]
        if mcfg.strategy == "suffix_by_method" and mcfg.method_column:
            m_base = base[mcfg.method_column].dropna().unique()
            m_oth = other[mcfg.method_column].dropna().unique()
            tag_b = str(m_base[0]) if len(m_base) else base_code
            tag_o = str(m_oth[0]) if len(m_oth) else code
            # rinomina le misure in conflitto con suffisso metodo, su entrambi i lati
            common = [c for c in bring if c in base.columns and c != mcfg.method_column]
            base = base.rename(columns={c: f"{c}_{tag_b}" for c in common})
            for c in bring:
                newname = f"{c}_{tag_o}" if c in common else c
                base[newname] = aligned[c].values
        else:
            for c in bring:
                base[c] = aligned[c].values
        log["aggiunti"].append({code: int(aligned[bring[0]].notna().sum()) if bring else 0})
    return base, log


# ===========================================================================
# REPORT  —  rigenera cio' che prima era l'Excel _statistics (output, non input).
# ===========================================================================
def profile(df, cohort_col="COLPROT") -> pd.DataFrame:
    """Report per colonna: tipo, range, validi/mancanti, coorti scoperte, keep/drop (soglia report)."""
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


def save_dataset(df, path):
    """Salvataggio con log (unico punto, insieme al __main__, che tocca il disco)."""
    df.to_csv(path, index=False)
    print(f"  salvato: {path}  (shape: {df.shape})")


# ===========================================================================
# ORCHESTRATORE COMPLETO  —  pulisce TUTTI i file registrati e mergia per categoria.
# ===========================================================================
def run_all(datasets=None, do_merge=True, verbose=True):
    """Pulisce ogni DatasetConfig in `datasets` e mergia le categorie con >=2 file.

    - salta con avviso i file il cui `source` non e' nella cartella (non e' un errore:
      cosi' puoi tenere registrati file che oggi non hai sottomano);
    - mergia solo le categorie che hanno una regola in config.CATEGORY_MERGE.
    Restituisce un riepilogo (dict) di cosa e' stato pulito / saltato / mergiato.
    """
    from pathlib import Path
    datasets = datasets or config.DATASETS
    cleaned_by_category, summary = {}, {"cleaned": [], "skipped": [], "merged": []}

    for code, cfg in datasets.items():
        if not Path(cfg.source).exists():
            summary["skipped"].append((code, f"'{cfg.source}' non trovato"))
            if verbose:
                print(f"[skip] {code}: '{cfg.source}' non trovato nella cartella")
            continue
        df1 = run_cleaning1(cfg)
        save_dataset(df1, cfg.output_cleaned1)
        profile(df1, cfg.cohort_column).to_csv(cfg.report_file, index=False)
        df2, log = run_cleaning2(df1, cfg)
        save_dataset(df2, cfg.output_cleaned2)
        summary["cleaned"].append((code, df2.shape))
        if cfg.category:
            cleaned_by_category.setdefault(cfg.category, {})[code] = df2

    if do_merge:
        for category, dfs in cleaned_by_category.items():
            if category not in config.CATEGORY_MERGE:
                summary["skipped"].append((f"merge:{category}", "nessuna regola in CATEGORY_MERGE"))
                if verbose:
                    print(f"[skip merge] categoria '{category}': manca la regola in CATEGORY_MERGE")
                continue
            if len(dfs) < 2:
                if verbose:
                    print(f"[info] categoria '{category}': un solo file, niente da mergiare")
                continue
            merged, _ = merge_category(dfs, category)
            out = f"{category.upper()}_merged.csv"
            save_dataset(merged, out)
            summary["merged"].append((category, merged.shape, list(dfs)))

    return summary


# ===========================================================================
# ENTRY POINT  —  l'unico posto che esegue I/O. Pulisce tutto e mergia.
# ===========================================================================
if __name__ == "__main__":
    print("=== CLEANING di tutti i file registrati in config.DATASETS ===")
    summary = run_all()
    print("\n=== RIEPILOGO ===")
    for code, shape in summary["cleaned"]:
        print(f"  pulito : {code}  {shape}")
    for cat, shape, files in summary["merged"]:
        print(f"  mergiato: {cat}  {shape}  da {files}")
    for what, why in summary["skipped"]:
        print(f"  saltato : {what}  ({why})")