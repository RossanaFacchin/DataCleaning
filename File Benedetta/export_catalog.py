"""
export_catalog.py  —  viste di CONSULTAZIONE del catalogo (catalog.json). [D006, D018]

Non modifica niente: legge catalog.json (tramite config, quindi gia' validato) e scrive
file generati, da NON modificare a mano (la fonte di verita' resta catalog.json).

USO (dalla cartella File Benedetta):
    python export_catalog.py
        -> catalog_table.csv: una riga per variabile, tutti i campi (vista tabellare).
           In piu' stampa i controlli: alias rivendicati da piu' variabili a livelli
           diversi (lecito, vince il piu' specifico) e modi di calcolo sconosciuti.
    python export_catalog.py ADNIMERGE_cleaned_02.csv [altri file puliti ...]
        -> <file>_dizionario.csv: per ogni colonna del file pulito, la voce del catalogo
           a cui si riferisce, anche per le colonne generate da regole:
             dummy  <VAR>_<livello>  -> VAR (con il livello)
             volumi <vol>%ICV        -> vol
           e l'elenco delle colonne che NON si riescono a ricondurre al catalogo.

I file generati contengono solo metadati e nomi di colonna, nessun dato dei partecipanti;
sono comunque CSV, quindi esclusi da git (.gitignore) come tutti gli output.
"""
from __future__ import annotations
import sys
from dataclasses import fields
from pathlib import Path

import pandas as pd

import config

# 'by' accettati nel campo derived: funzioni del motore delle derivate + passi dedicati
KNOWN_STEPS = {"add_visit_month", "add_atn_profile", "add_constant_columns"}


def catalog_table() -> pd.DataFrame:
    rows = []
    for name, v in config.catalog().items():
        row = {"variabile": name}
        for f in fields(config.Var):
            val = getattr(v, f.name)
            if f.name in ("aliases", "log_ref"):
                val = ", ".join(val)
            elif f.name == "derived":
                val = " | ".join(f"{r['by']}({', '.join(r['from'])})" for r in val)
            elif f.name == "levels" and val:
                val = ", ".join(f"{k}={c}" for k, c in sorted(val.items(), key=lambda x: x[1]))
            row[f.name] = val
        rows.append(row)
    return pd.DataFrame(rows)


def checks() -> list[str]:
    """Controlli per l'occhio umano (il loader ha gia' bloccato gli errori veri)."""
    import pipeline                                   # import senza I/O
    known = set(pipeline.DERIVATIONS) | KNOWN_STEPS
    out = []
    for col, items in config.alias_overrides():
        out.append(f"[alias su piu' livelli] {col}: " + "; ".join(f"{a} -> {s}" for a, s in items))
    cat = config.catalog()
    for name, v in cat.items():
        for r in v.derived:
            if r["by"] not in known:
                out.append(f"[derived] {name}: modo di calcolo '{r['by']}' sconosciuto")
            for inp in r["from"]:
                if inp not in cat:
                    out.append(f"[derived] {name}: input '{inp}' non e' nel catalogo")
        if v.method_col and v.method_col not in cat:
            out.append(f"[method_col] {name}: '{v.method_col}' non e' nel catalogo")
    return out


def resolve_column(col: str):
    """Riconduce una colonna di un file pulito al catalogo: (variabile, collegamento, livello)."""
    cat = config.catalog()
    if col in cat:
        return col, "diretta", None
    if col.endswith("%ICV") and col[:-4] in cat:
        return col[:-4], "volume %ICV", None
    for name, v in cat.items():                       # dummy: <VAR>_<livello>
        if v.levels and col.startswith(name + "_") and col[len(name) + 1:] in v.levels:
            return name, "dummy", col[len(name) + 1:]
    return None, "NON NEL CATALOGO", None


def data_dictionary(csv_path: Path) -> tuple[pd.DataFrame, list[str]]:
    columns = pd.read_csv(csv_path, nrows=0).columns       # solo l'intestazione
    cat = config.catalog()
    rows, orphans = [], []
    for col in columns:
        name, link, level = resolve_column(col)
        v = cat.get(name)
        if v is None:
            orphans.append(col)
        rows.append({
            "colonna": col, "variabile_catalogo": name, "collegamento": link, "livello": level,
            "domain": v.domain if v else None, "definition": v.definition if v else None,
            "unit": ("%" if link == "volume %ICV" else v.unit) if v else None,
            "role": v.role if v else None, "scope": v.scope if v else None,
            "method_col": v.method_col if v else None, "vocab_code": v.vocab_code if v else None,
        })
    return pd.DataFrame(rows), orphans


def main(argv):
    if not argv:
        table = catalog_table()
        table.to_csv("catalog_table.csv", index=False)
        print(f"scritto catalog_table.csv ({len(table)} variabili)")
        for line in checks():
            print(" ", line)
        return
    for p in map(Path, argv):
        dd, orphans = data_dictionary(p)
        out = p.with_name(p.stem + "_dizionario.csv")
        dd.to_csv(out, index=False)
        print(f"scritto {out.name}: {len(dd)} colonne, {len(orphans)} non riconducibili al catalogo")
        if orphans:
            print("   ", orphans)


if __name__ == "__main__":
    main(sys.argv[1:])
