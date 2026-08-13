"""
count_bridges.py  —  quanti campioni-ponte ho, per misura?

Un "ponte" e' uno stesso soggetto-visita (RID + EXAMDATE entro buffer_days)
misurato da DUE metodi diversi. Senza ponti una misura NON e' armonizzabile
per calibrazione (Deming/Passing-Bablok): manca il substrato empirico.

Questo script NON trasforma nulla. Pulisce i file di una categoria con la tua
pipeline, li impila in long, e per ogni misura con >=2 metodi conta i ponti
verso il metodo di riferimento (config.HARMONIZE[category]) - la stessa cosa che
fa harmonize() prima di decidere se convertire o marcare 'no_bridge'.

Uso:
    python3 count_bridges.py                 # categoria 'plasma' (default)
    python3 count_bridges.py csf             # altra categoria
"""
from __future__ import annotations
import sys
from pathlib import Path
import pandas as pd

import config
import pipeline


def clean_category(category: str) -> dict:
    """Pulisce (cleaning1+2) tutti i DatasetConfig della categoria di cui esiste il source."""
    cleaned = {}
    for code, cfg in config.DATASETS.items():
        if cfg.category != category:
            continue
        if not Path(cfg.source).exists():
            print(f"[skip] {code}: '{cfg.source}' non trovato")
            continue
        cleaned[code] = pipeline.run_cleaning(cfg)   # cleaning1 -> cleaning2 in memoria
        print(f"[ok]   {code}: {cleaned[code].shape}")
    return cleaned


def count_bridges(category: str = "plasma", hcfg=None,
                  id_col: str = "RID", date_col: str = "EXAMDATE") -> pd.DataFrame:
    hcfg = hcfg or config.HARMONIZE[category]
    cleaned = clean_category(category)
    if len(cleaned) < 2:
        print("\nMeno di due file puliti: niente da appaiare.")
        return pd.DataFrame()

    df = pipeline.stack_category(cleaned)
    mcol = hcfg.method_column
    if mcol not in df.columns:
        raise RuntimeError(f"colonna metodo '{mcol}' assente nei file puliti")

    skip = {id_col, date_col, mcol, "VISCODE", "VISIT_MONTH", "update_stamp"}
    measurands = hcfg.measurands or [c for c in df.columns
                                     if c not in skip and pd.api.types.is_numeric_dtype(df[c])]

    rows = []
    for M in measurands:
        methods = [m for m in df[mcol].dropna().unique()
                   if df.loc[df[mcol] == m, M].notna().any()]
        if len(methods) < 2:
            rows.append({"misura": M, "metodi": ",".join(map(str, methods)) or "-",
                         "stato": "metodo_singolo", "coppia": "-", "n_ponti": "-",
                         "armonizzabile": "passa invariata"})
            continue
        ref = hcfg.reference_overrides.get(M, hcfg.reference)
        if ref not in methods:                       # rif assente -> il piu' coperto (come harmonize)
            ref = max(methods, key=lambda m: df.loc[df[mcol] == m, M].notna().sum())
        ref_rows = df[(df[mcol] == ref) & df[M].notna()][[id_col, date_col, M]]
        for K in [m for m in methods if m != ref]:
            k_rows = df[(df[mcol] == K) & df[M].notna()][[id_col, date_col, M]]
            aligned = pipeline._match_within_buffer(k_rows, ref_rows,
                                                    [id_col, date_col], hcfg.buffer_days)
            n = int(aligned[M].notna().sum())
            verdict = ("OK" if n >= hcfg.min_bridge
                       else "ponte debole" if n >= 5
                       else "NON armonizzabile (no_bridge)")
            rows.append({"misura": M, "metodi": ",".join(map(str, methods)),
                         "stato": "multi_metodo", "coppia": f"{K}->{ref}",
                         "n_ponti": n, "armonizzabile": verdict})
    out = pd.DataFrame(rows)
    return out


if __name__ == "__main__":
    category = sys.argv[1] if len(sys.argv) > 1 else "plasma"
    hcfg = config.HARMONIZE[category]
    print(f"=== Campioni-ponte per categoria '{category}' ===")
    print(f"    riferimento = {hcfg.reference} | buffer = {hcfg.buffer_days} gg | "
          f"soglia ponte robusto (min_bridge) = {hcfg.min_bridge}\n")
    table = count_bridges(category, hcfg)
    if not table.empty:
        print("\n" + table.to_string(index=False))
        out = f"bridges_{category}.csv"
        table.to_csv(out, index=False)
        print(f"\nsalvato: {out}")