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
             dummy  <VAR>/<livello>  -> VAR (con il livello)
             volumi <vol>%ICV        -> vol
           e l'elenco delle colonne che NON si riescono a ricondurre al catalogo.

I file generati contengono solo metadati e nomi di colonna, nessun dato dei partecipanti;
sono comunque CSV, quindi esclusi da git (.gitignore) come tutti gli output.
"""
from __future__ import annotations
import json
import sys
from dataclasses import fields
from pathlib import Path

import pandas as pd

import config

# 'by' accettati nel campo derived (solo descrittivo [D041]): passi della pipeline che calcolano
KNOWN_STEPS = {"recompute_age", "add_derived_ratios", "add_visit_month", "add_atn_profile",
               "add_constant_columns"} | set(config.EVOLUTIONS)


def template_rows() -> list[dict]:
    """Le righe dei template (chiavi '_template_*' di catalog.json): per ogni chiave la sua
    spiegazione. Vanno in testa alla tabella, cosi' chi la apre legge subito cosa significa ogni
    colonna. Il loader le ignora (chiavi '_'): qui si leggono dal JSON grezzo."""
    raw = json.loads((Path(config.__file__).parent / config.CATALOG_FILE).read_text(encoding="utf-8"))
    rows = []
    for label, block in raw.items():
        if not (label.startswith("_template") and isinstance(block, dict)):
            continue
        row = {"variabile": label}
        for key, val in block.items():
            row[key] = ", ".join(map(str, val)) if isinstance(val, list) else val
        rows.append(row)
    return rows


def catalog_table() -> pd.DataFrame:
    rows = template_rows()
    for name, v in config.catalog().items():
        row = {"variabile": name, "_istruzioni": ""}
        for f in fields(config.Var):
            val = getattr(v, f.name)
            if f.name in ("aliases", "log_ref", "evolution"):
                val = ", ".join(val)
            elif f.name == "derived":
                val = " | ".join(f"{r['by']}({', '.join(r['from'])})" for r in val)
            elif f.name == "levels" and val:
                val = ", ".join(f"{k}={c}" for k, c in sorted(val.items(), key=lambda x: x[1]))
            row[f.name] = val
        rows.append(row)
    columns = ["variabile", "_istruzioni"] + [f.name for f in fields(config.Var)]
    return pd.DataFrame(rows).reindex(columns=columns)


def checks() -> list[str]:
    """Controlli per l'occhio umano (il loader ha gia' bloccato gli errori veri)."""
    out = []
    for col, items in config.alias_overrides():
        out.append(f"[alias su piu' livelli] {col}: " + "; ".join(f"{a} -> {s}" for a, s in items))
    cat = config.catalog()
    for name, v in cat.items():
        for r in v.derived:
            if r["by"] not in KNOWN_STEPS:
                out.append(f"[derived] {name}: modo di calcolo '{r['by']}' sconosciuto")
            for inp in r["from"]:
                if inp not in cat:
                    out.append(f"[derived] {name}: input '{inp}' non e' nel catalogo")
        if v.method_col and v.method_col not in cat:
            out.append(f"[method_col] {name}: '{v.method_col}' non e' nel catalogo")
    return out + worsening_checks()


def worsening_checks() -> list[str]:
    """[D040] Confronta 'worsening' del catalogo con la direzione di ranges.json (sezioni
    normalization e volume), che resta anche li'. Segnala le discordanze e le variabili che
    hanno la direzione da una parte sola."""
    conv = {"increasing": "increase", "inverse": "decrease"}
    ranges = {}
    for section in ("normalization", "volume"):
        for col, v in config.load_settings(section).items():
            dirs = {v[2]} if isinstance(v, list) else {x[2] for x in v.values()}
            ranges[col] = conv.get(dirs.pop()) if len(dirs) == 1 else f"misto {sorted(dirs)}"
    cat = config.catalog()
    out, not_in_catalog = [], []
    for name in sorted(set(ranges) | {n for n, v in cat.items() if v.worsening}):
        w, r = (cat[name].worsening if name in cat else None), ranges.get(name)
        if name not in cat:
            not_in_catalog.append(name)
        elif r and w != r:
            out.append(f"[worsening] {name}: catalogo {w!r}, ranges.json {r!r}")
        elif not r:
            out.append(f"[worsening] {name}: nel catalogo ({w}) ma non in ranges.json")
    if not_in_catalog:
        out.append(f"[worsening] {len(not_in_catalog)} colonne di ranges.json non sono nel catalogo: "
                   + ", ".join(not_in_catalog))
    return out


def resolve_column(col: str):
    """Riconduce una colonna di un file pulito al catalogo: (variabile, collegamento, livello).
    Dummy e %ICV sono voci del catalogo (figlie generate dalle evoluzioni [D036]); le regole sui
    nomi restano solo come ripiego per colonne generate senza evoluzione dichiarata."""
    cat = config.catalog()
    if col in cat:
        parent = config.parent_of(col)
        if parent:
            d = cat[col].derived[0]
            return col, f"evoluzione {d['by']} di {parent}", d.get("level")
        return col, "diretta", None
    if col.endswith("%ICV") and col[:-4] in cat:
        return col[:-4], "volume %ICV", None
    sep = config.DUMMY_SEP
    for name, v in cat.items():                       # dummy: <VAR>/<livello>
        if v.levels and col.startswith(name + sep) and col[len(name) + len(sep):] in v.levels:
            return name, "dummy", col[len(name) + len(sep):]
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
            "worsening": v.worsening if v else None,
            "variabile_madre": config.parent_of(name) if v else None,
            "role": v.role if v else None, "scope": v.scope if v else None,
            "method_col": v.method_col if v else None, "vocab_code": v.vocab_code if v else None,
        })
    return pd.DataFrame(rows), orphans


def main(argv):
    if not argv:
        table = catalog_table()
        table.to_csv("catalog_table.csv", index=False)
        n_tpl = int(table["variabile"].str.startswith("_").sum())
        print(f"scritto catalog_table.csv ({n_tpl} righe di template con la spiegazione delle "
              f"colonne + {len(table) - n_tpl} variabili)")
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
