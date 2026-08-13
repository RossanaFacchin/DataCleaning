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
from config import DatasetConfig, ADNIMERGE


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


def drop_required(df, cols):
    """[nota Chiara #1] Scarta la riga se MANCA anche UNA sola di queste colonne
    (any-none), es. ID o data. Diverso da drop_if_all_none (che scarta se TUTTE NaN)."""
    present = [c for c in cols if c in df.columns]
    return df.dropna(subset=present, how="any") if present else df


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


def parse_dates(df, cols):
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


def recompute_age(df, date_col="EXAMDATE", bl_date_col="EXAMDATE_bl", age_col="AGE"):
    """AGE (fissa al baseline) -> AGE_bl; nuova AGE = AGE_bl + tempo trascorso per visita."""
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
    """Rinomina nei nomi standard: CATALOG globale + categoria + override per-file.

    A prova di collisione: se un rename porterebbe due colonne allo STESSO nome
    (es. il grezzo ha gia' 'CDRSB' e un'altra colonna verrebbe mappata li'), quel
    rename viene SALTATO (si tiene il grezzo), cosi' non nascono colonne duplicate.
    """
    mapping = cfg.effective_rename()
    taken = set(df.columns)
    safe = {}
    collisions = []
    for raw, std in mapping.items():
        if raw not in df.columns or std == raw:
            continue
        if std in taken:                       # il nome standard e' gia' occupato -> non rinominare
            collisions.append((raw, std))
            continue
        safe[raw] = std
        taken.discard(raw); taken.add(std)
    if collisions:
        print(f"  [rename] {cfg.file_code}: saltati per collisione (tenuto il grezzo): {collisions}")
    return df.rename(columns=safe)


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
    """Orchestratore di cleaning 1: raw -> dataframe pulito (in memoria, niente I/O).

    [nota Chiara #4] RENAME PER PRIMO: subito dopo aver uniformato i missing si
    portano le colonne ai nomi standard, cosi' tutto il resto (drop, recode, decensor,
    dedup, eta') lavora su nomi standard ed e' agganciato al CATALOG.
    """
    df = load(cfg)                                                # download -> CSV
    df = replace_unknown(df)                                      # replace_unknown_values
    df = rename_variables(df, cfg)                               # <-- RENAME FIRST (#4)
    if cfg.decensor_biomarkers:
        df = decensor(df, cfg.decensor_columns or config.columns_in("Biomarker"))
    df = drop_required(df, cfg.required_all_present)             # [#1] scarta se manca ID/data
    df = drop_if_all_none(df, cfg.essential_columns)             # scarta se TUTTE le essenziali NaN
    df = drop_if_all_none(df, cfg.also_required)                 # 2° filtro (es. DX obbligatoria)
    df = parse_dates(df, [cfg.date_column])                      # to_date_format
    has_keys = (cfg.date_column in df.columns) and (cfg.id_column in df.columns)
    if has_keys:
        df = dedup_visits(df, cfg.id_column, cfg.date_column, cfg.essential_columns)
        df = add_visit_month(df, cfg.id_column, cfg.date_column)  # find_exam_code -> VISIT_MONTH
    if cfg.recompute_age and (cfg.date_column in df.columns):
        df = recompute_age(df, cfg.date_column)                  # add_calculated_age (AGE->AGE_bl)
    df = recode(df, cfg.recode_columns)                          # categorie -> etichette standard (#3)
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

    [nota Chiara #3] le categoriche sono gia' ETICHETTE STANDARD (stringhe) dopo
    recode, quindi le dummy escono leggibili (DX_CN, GENDER_male) e i NaN non
    generano colonna. Restituisce (df, colonne_dummy_create).
    """
    df = df.copy()
    present = [c for c in cols if c in df.columns]
    before = set(df.columns)
    if present:
        df = pd.get_dummies(df, columns=present, dtype=int)
    created = [c for c in df.columns if c not in before]
    return df, created


def normalize_volumes_icv(df, icv_column="ICV", vol_columns=None):
    """Normalizza i volumi come percentuale di ICV e li RINOMINA in '<vol>%ICV'.

    [nota Chiara #11] i volumi normalizzati prendono il nome '<vol>%ICV' (es.
    'Hippocampus%ICV'), coerente coi ranges e col vecchio output: cosi' non si
    confonde un volume in mm3 con uno gia' normalizzato. Restituisce (df, mappa_rinomini).
    NB: NON somma sinistro+destro (get_volumes_total) - i volumi ADNIMERGE sono gia' totali.
    """
    df = df.copy()
    if vol_columns is None:
        vol_columns = config.volume_columns(icv_column)
    if icv_column not in df.columns:
        return df, {}
    icv = pd.to_numeric(df[icv_column], errors="coerce")
    renamed = {}
    for c in list(vol_columns) + [icv_column]:
        if c in df.columns:
            new = f"{c}%ICV"
            df[new] = pd.to_numeric(df[c], errors="coerce") / icv * 100.0
            df = df.drop(columns=c)
            renamed[c] = new
    return df, renamed


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

    # [nota Chiara #9] il drop-righe-per-volumi NON si fa piu' qui (rischia di
    # buttare righe con altri dati): si fa dopo il merge, con drop_rows_no_signal().

    renamed_vol = {}
    if cfg.normalize_icv:
        df, renamed_vol = normalize_volumes_icv(df, cfg.icv_column)   # #11: rinomina in <vol>%ICV
        log["icv_rinominati"] = renamed_vol

    if cfg.keep_columns:
        # dummy generate, colonne calcolate, volumi %ICV e le COSTANTI (metodo/assay) si
        # tengono in automatico: NON vanno elencate a mano nel config.
        engineered = [c for c in ("VISIT_MONTH", "AGE_bl") if c in df.columns]
        auto = created + engineered + list(renamed_vol.values()) + list(cfg.constant_columns)
        df, dropped_cols, missing_cols = keep_only_columns(df, cfg.keep_columns, extra=auto)
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


def collapse_visits(df_long, id_col="RID", date_col="EXAMDATE", buffer_days=80, method_column=None):
    """[note Chiara #7/#10] Collassa il long in UNA riga per (soggetto, visita), OUTER:
    NESSUNA riga persa. Righe dello stesso soggetto entro buffer_days = stessa visita ->
    coalescing (primo valore non-nullo). Robusto: se manca la data collassa per SOGGETTO
    (file baseline/genetici tipo APOERES); se manca l'ID non collassa. Restituisce (df, log)."""
    df = df_long.copy()
    has_id = id_col in df.columns
    has_date = date_col in df.columns
    if not has_id:                                  # senza chiave soggetto non si collassa
        return df.reset_index(drop=True), {"righe_in": len(df), "visite_out": len(df),
                                           "note": f"'{id_col}' assente: nessun collasso"}
    if has_date:
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
        df = df.sort_values([id_col, date_col], na_position="last").reset_index(drop=True)
    else:
        df = df.sort_values([id_col]).reset_index(drop=True)   # niente data -> per soggetto
    clusters, dists = [], []
    cur_id = cur_anchor = None; c = -1
    for _, row in df.iterrows():
        rid = row[id_col]
        if not has_date:                            # una riga per soggetto
            if rid != cur_id:
                c += 1; cur_id = rid
        else:
            d = row[date_col]
            if rid != cur_id or pd.isna(d) or cur_anchor is None or (d - cur_anchor).days > buffer_days:
                c += 1; cur_id, cur_anchor = rid, d
            else:
                dists.append((d - cur_anchor).days)
        clusters.append(c)
    df["_cl"] = clusters

    def _coalesce(g):
        out = g.iloc[0].copy()
        for col in g.columns:
            nn = g[col].dropna()
            if len(nn):
                out[col] = nn.iloc[0]
        if method_column and method_column in g.columns:
            ms = list(dict.fromkeys(g[method_column].dropna().tolist()))
            out[method_column] = "+".join(map(str, ms)) if ms else np.nan
        return out

    collapsed = (df.groupby("_cl", sort=False).apply(_coalesce, include_groups=False)
                   .reset_index(drop=True))
    collapsed = collapsed.drop(columns="_cl", errors="ignore")
    dists = np.array(dists)
    log = {"righe_in": len(df), "visite_out": len(collapsed),
           "match_esatti_0gg": int((dists == 0).sum()) if dists.size else 0,
           "match_entro_buffer": int((dists > 0).sum()) if dists.size else 0,
           "distanza_media_gg": round(float(dists[dists > 0].mean()), 1) if (dists > 0).any() else 0.0}
    return collapsed, log


def drop_rows_no_signal(df, signal_columns):
    """[nota Chiara #9] DOPO il merge: scarta la riga solo se manca OGNI segnale
    (nessun valore tra le colonne indicate, es. volumi+PET+CSF). Restituisce (df, n_rimosse)."""
    present = [c for c in signal_columns if c in df.columns]
    if not present:
        return df, 0
    keep = df[present].notna().any(axis=1)
    return df[keep].copy(), int((~keep).sum())


def merge_category(cleaned: dict, category: str, harmonize_first: bool = True):
    """Consolida una categoria: impila i file (long) -> [armonizza] -> collassa in una
    riga per visita (outer). [note Chiara #7] niente piu' suffix_by_method: i metodi si
    portano sulla stessa scala (armonizzazione) e poi si coalescono, restando agganciati
    ai nomi di CATALOG/cutoffs. Restituisce (df_categoria, log)."""
    df_long = stack_category(cleaned)
    log = {}
    if harmonize_first and category in config.HARMONIZE:
        df_long, log["harmonize"] = harmonize(df_long, config.HARMONIZE[category], verbose=False)
    mcfg = config.CATEGORY_MERGE.get(category)
    buffer = mcfg.buffer_days if mcfg else 80
    mcol = mcfg.method_column if mcfg else None
    df_wide, log["collapse"] = collapse_visits(df_long, buffer_days=buffer, method_column=mcol)
    return df_wide, log


# ===========================================================================
# ARMONIZZAZIONE (v0)  —  porta piu' metodi sulla stessa scala, per misura.
#   Substrato: i file puliti IMPILATI (long), non il merge largo. Per ogni misura
#   con >=2 metodi: calibra ogni metodo sul riferimento usando i campioni-ponte
#   (stesso soggetto-visita misurato da 2 metodi) e collassa in una colonna.
#   Le misure con un solo metodo passano invariate. I coefficienti finiscono in
#   un artefatto JSON (auditabile), con la qualita' del ponte (n, r, IC).
# ===========================================================================
def stack_category(cleaned: dict) -> pd.DataFrame:
    """Impila i DataFrame puliti di una categoria in formato long (una riga per metodo)."""
    return pd.concat(list(cleaned.values()), ignore_index=True, sort=False)


def _deming(x, y, delta=1.0):
    """Deming regression y = a + b*x (entrambi con errore). Chiuso, robusto al dilution bias."""
    x = np.asarray(x, float); y = np.asarray(y, float)
    mx, my = x.mean(), y.mean()
    sxx = ((x - mx) ** 2).sum(); syy = ((y - my) ** 2).sum(); sxy = ((x - mx) * (y - my)).sum()
    b = (syy - delta * sxx + np.sqrt((syy - delta * sxx) ** 2 + 4 * delta * sxy ** 2)) / (2 * sxy)
    return my - b * mx, b


def _passing_bablok(x, y):
    """Passing-Bablok y = a + b*x (non parametrico, robusto agli outlier)."""
    x = np.asarray(x, float); y = np.asarray(y, float); n = len(x)
    s = []
    for i in range(n):
        for j in range(i + 1, n):
            dx = x[i] - x[j]
            if dx == 0:
                continue
            sl = (y[i] - y[j]) / dx
            if sl != -1:
                s.append(sl)
    s = np.sort(s); N = len(s); K = int((s < -1).sum())
    b = s[(N + K) // 2] if (N + K) % 2 else 0.5 * (s[(N + K) // 2 - 1] + s[(N + K) // 2])
    a = np.median(y - b * x)
    return a, b


def _fit_converter(x_ref, y_met, strategy):
    """Fitta ref = a + b*metodo (converte il metodo nella scala del riferimento) + diagnostica."""
    fit = _passing_bablok if strategy == "passing_bablok" else _deming
    a, b = fit(y_met, x_ref)                       # nota: ref in funzione del metodo
    r = float(np.corrcoef(x_ref, y_met)[0, 1])
    rng = np.random.default_rng(0); bs = []
    for _ in range(1000):
        idx = rng.integers(0, len(x_ref), len(x_ref))
        try:
            bs.append(fit(np.asarray(y_met)[idx], np.asarray(x_ref)[idx])[1])
        except Exception:
            pass
    ci = [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))] if bs else None
    return {"intercept": float(a), "slope": float(b), "n": len(x_ref), "r": round(r, 3), "slope_ci95": ci}


def harmonize(df_long, hcfg, id_col="RID", date_col="EXAMDATE", verbose=True):
    """Armonizza in formato long. Restituisce (df_armonizzato, fits).

    Per ogni misura con >=2 metodi: converte ogni metodo non-riferimento sulla scala
    del riferimento (calibrazione sui ponti) e collassa in un'unica colonna. Le misure
    a metodo singolo restano invariate. `fits` e' l'artefatto dei coefficienti+diagnostica.
    """
    df = df_long.copy()
    mcol = hcfg.method_column
    if mcol not in df.columns:
        raise RuntimeError(f"colonna metodo '{mcol}' assente: i file puliti la stampano da constant_columns")
    # misure candidate: numeriche, non chiavi/metodo
    skip = {id_col, date_col, mcol, "VISCODE", "VISIT_MONTH", "update_stamp"}
    measurands = hcfg.measurands or [c for c in df.columns
                                     if c not in skip and pd.api.types.is_numeric_dtype(df[c])]
    fits = {}
    for M in measurands:
        methods = [m for m in df[mcol].dropna().unique()
                   if df.loc[df[mcol] == m, M].notna().any()]
        if len(methods) < 2:
            fits[M] = {"status": "single_method", "method": methods[0] if methods else None}
            continue
        ref = hcfg.reference_overrides.get(M, hcfg.reference)
        if ref not in methods:                     # rif assente per questa misura -> prendi il piu' coperto
            ref = max(methods, key=lambda m: df.loc[df[mcol] == m, M].notna().sum())
        fits[M] = {"status": "harmonized", "reference": ref, "converters": {}}
        ref_rows = df[(df[mcol] == ref) & df[M].notna()][[id_col, date_col, M]]
        for K in [m for m in methods if m != ref]:
            k_rows = df[(df[mcol] == K) & df[M].notna()][[id_col, date_col, M]]
            aligned = _match_within_buffer(k_rows, ref_rows, [id_col, date_col], hcfg.buffer_days)
            mask = aligned[M].notna().values
            x_ref = aligned[M].values[mask].astype(float)     # riferimento
            y_met = k_rows[M].values[mask].astype(float)      # metodo K
            if len(x_ref) < 5:
                fits[M]["converters"][K] = {"status": "no_bridge", "n": int(len(x_ref))}
                if verbose:
                    print(f"  [{M}] {K}->{ref}: ponte insufficiente (n={len(x_ref)}) - lasciato invariato")
                continue
            d = _fit_converter(x_ref, y_met, hcfg.strategy)
            d["status"] = "ok" if d["n"] >= hcfg.min_bridge else "weak_bridge"
            fits[M]["converters"][K] = d
            # applica: converte TUTTI i valori del metodo K nella scala del riferimento
            sel = (df[mcol] == K) & df[M].notna()
            df.loc[sel, M] = d["intercept"] + d["slope"] * df.loc[sel, M].astype(float)
            if verbose:
                flag = "" if d["status"] == "ok" else f"  ATTENZIONE ponte debole (n={d['n']}, r={d['r']})"
                print(f"  [{M}] {K}->{ref}: ref = {d['intercept']:.2f} + {d['slope']:.3f}*{K}{flag}")
    return df, fits


def run_harmonization(cleaned: dict, category: str, hcfg=None, artifact="harmonization_fit.json"):
    """Comodita': impila i file puliti di una categoria, armonizza, salva l'artefatto dei fit."""
    import json
    hcfg = hcfg or config.HARMONIZE[category]
    df_long = stack_category(cleaned)
    df_harm, fits = harmonize(df_long, hcfg)
    with open(artifact, "w") as f:
        json.dump(fits, f, indent=2)
    return df_harm, fits


# ===========================================================================
# REPORT  —  rigenera cio' che prima era l'Excel _statistics (output, non input).
# ===========================================================================
def profile(df, cohort_col="COLPROT", id_col="RID") -> pd.DataFrame:
    """Report per colonna: tipo, range, validi/mancanti, coorti scoperte, keep/drop.

    [nota Chiara #5] per ogni variabile aggiunge quanti SOGGETTI hanno quel valore e
    la media di visite valorizzate per soggetto (non solo il conteggio righe). Da girare
    sia dopo cleaning1 sia dopo cleaning2.
    """
    rows, n = [], len(df)
    df = df.loc[:, ~df.columns.duplicated()]      # difensivo: mai iterare su colonne duplicate
    cohorts = df[cohort_col].dropna().unique().tolist() if cohort_col in df else []
    has_id = id_col in df.columns
    for col in df.columns:
        s = df[col]
        n_valid = int(s.notna().sum())
        is_num = pd.api.types.is_numeric_dtype(s)
        n_subj = vis_per_subj = None
        if has_id and n_valid:
            g = df.loc[s.notna()].groupby(id_col)
            n_subj = int(g.ngroups)
            vis_per_subj = round(n_valid / n_subj, 2) if n_subj else None
        rows.append({
            "variable": col,
            "type": s.dtype.name,
            "range": f"{s.min()}, {s.max()}" if is_num and n_valid else "",
            "valid_values": n_valid,
            "missing_values": n - n_valid,
            "n_subjects": n_subj,                 # [#5] soggetti con quel valore
            "visits_per_subject": vis_per_subj,   # [#5] media visite valorizzate/soggetto
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
        # [nota Chiara #5] profile anche dopo cleaning2
        profile(df2, cfg.cohort_column).to_csv(cfg.report_file.replace("_report", "_report_02"), index=False)
        summary["cleaned"].append((code, df2.shape))
        if cfg.category:
            cleaned_by_category.setdefault(cfg.category, {})[code] = df2

    if do_merge:
        import json
        for category, dfs in cleaned_by_category.items():
            if len(dfs) < 1:
                continue
            merged, mlog = merge_category(dfs, category)     # stack -> armonizza -> collassa (outer)
            save_dataset(merged, f"{category.upper()}_consolidated.csv")
            if mlog.get("harmonize"):                        # artefatto dei fit di armonizzazione
                with open(f"harmonization_fit_{category}.json", "w") as f:
                    json.dump(mlog["harmonize"], f, indent=2)
            summary["merged"].append((category, merged.shape, list(dfs)))
            if verbose and mlog.get("collapse"):
                print(f"[{category}] collapse: {mlog['collapse']}")

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