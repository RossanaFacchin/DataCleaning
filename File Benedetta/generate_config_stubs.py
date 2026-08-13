"""
generate_config_stubs.py  —  genera BOZZE di DatasetConfig leggendo i file, ALLA CIECA.

PRINCIPIO
    Lo script NON assume di sapere cosa trovera'. Non indovina la categoria dal nome,
    non da' per scontato EXAMDATE o RID, non fa rename "a somiglianza". OSSERVA i dati
    (campiona qualche riga), RIPORTA cosa vede, e lascia ogni scelta incerta come TODO
    esplicito. L'unica cosa automatica e' il rename su MATCH ESATTO col CATALOG (verita'
    che hai messo tu negli aliases), non una deduzione.

    Per ogni file scrive un blocco DatasetConfig con:
      - profilo per colonna (tipo dai valori, n. distinti, censure >/<);
      - candidati ID / DATA / VISITA rilevati DAI DATI (proposti, non imposti);
      - rename automatico SOLO per colonne gia' nel CATALOG;
      - tutto il resto (categoria, metodo/assay, essential, keep) come TODO.

    USO:
        python3 generate_config_stubs.py [CARTELLA]     # default: cartella corrente
    Output: config_datasets_draft.py + un report di quante decisioni restano per file.
"""
from __future__ import annotations
import sys
import re
import warnings
from pathlib import Path
import pandas as pd

import config   # solo per config.RENAME (grezzo->standard da CATALOG.aliases): match ESATTO

SAMPLE_ROWS = 500
# output della pipeline / file di test: non sono grezzi in ingresso
EXCLUDE = ("_cleaned_0", "_report", "_consolidated", "_merged", "_fake", "_draft")
DATE_SUFFIX = re.compile(r"[_-]?\d{1,2}[A-Za-z]{3}\d{4}$|[_-]?\d{2}_\d{2}_\d{2}$|[_-]?\d{4}-\d{2}-\d{2}$")

# Colonne amministrative/QC note di ADNI: NON sono misure. Lista ESPLICITA e rivedibile
# (non un'euristica nascosta): se vuoi tenerne una, toglila da qui.
IGNORE_EXACT = {
    "PHASE", "SITEID", "STATUS", "IMAGEUID", "LONIUID", "DD_CRF_VERSION_LABEL",
    "LANGUAGE_CODE", "HAS_QC_ERROR", "VID", "GUSPECID", "DER", "RUN", "SEQ", "RECNO",
    "USERDATE", "RUNDATE", "DRAWTIME", "DRAW_TIME", "Comments", "COMMENT", "Primary",
    "Additive", "VERSION", "FLDNAME", "CRFNAME", "update_stamp", "EXAMDATE_bl",
}
IGNORE_PAT = re.compile(r"QC$|^QC|_QC|_?VERSION$", re.I)          # flag di qualita'/versione
ST_PAT = re.compile(r"^ST\d+[A-Z]{0,2}$", re.I)                   # codici FreeSurfer ADNI (volumi)


def is_admin(c: str) -> bool:
    return c in IGNORE_EXACT or bool(IGNORE_PAT.search(c))


def read_sample(path: Path) -> pd.DataFrame:
    """Legge un campione di righe, con fallback robusti. Non esplode su file strani."""
    for enc in ("utf-8", "latin-1"):
        try:
            return pd.read_csv(path, nrows=SAMPLE_ROWS, dtype=str, keep_default_na=True,
                               encoding=enc, engine="python", on_bad_lines="skip")
        except UnicodeDecodeError:
            continue
        except Exception:
            break
    return pd.read_csv(path, nrows=0)          # ultima spiaggia: solo header


def profile_col(s: pd.Series) -> dict:
    """Profila una colonna DAI VALORI (non dal nome): tipo, distinti, censure."""
    s = s.dropna().astype(str).str.strip()
    n = len(s)
    if n == 0:
        return {"kind": "vuota", "distinct": 0, "censored": False}
    censored = bool(s.str.match(r"^[<>]").any())
    stripped = s.str.replace(r"^[<>]\s*", "", regex=True)
    frac_num = pd.to_numeric(stripped, errors="coerce").notna().mean()
    frac_date = 0.0
    if frac_num < 0.9:                          # non provare a "datare" numeri puri
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            frac_date = pd.to_datetime(s, errors="coerce", dayfirst=False).notna().mean()
    kind = "num" if frac_num >= 0.9 else ("date" if frac_date >= 0.9 else "cat/str")
    return {"kind": kind, "distinct": int(s.nunique()), "censored": censored}


def detect_candidates(cols, prof):
    """Candidati DAI DATI + indizio dal nome, MAI imposti."""
    date_c = [c for c in cols if prof[c]["kind"] == "date"]
    id_c = [c for c in cols if re.search(r"(^|_)(RID|PTID|ID|SUBJECT)$", c, re.I)]
    visit_c = [c for c in cols if "VISCODE" in c.upper()]
    return date_c, id_c, visit_c


def varname(code: str) -> str:
    v = re.sub(r"\W", "_", code).upper().strip("_")
    return v if (v[:1].isalpha() or v[:1] == "_") else "F_" + v


def stub_for(path: Path, reverse: dict):
    df = read_sample(path)
    cols = list(df.columns)
    prof = {c: profile_col(df[c]) for c in cols} if len(df) else {c: {"kind": "?", "distinct": 0, "censored": False} for c in cols}
    code = DATE_SUFFIX.sub("", re.sub(r"\.csv$", "", path.name, flags=re.I)).strip("_")
    var = varname(code)

    date_c, id_c, visit_c = detect_candidates(cols, prof)
    # rename automatico: SOLO match esatto col CATALOG (nessuna euristica)
    auto_rename = {c: reverse[c] for c in cols if c in reverse and reverse[c] != c}
    key_like = set(id_c) | set(visit_c) | set(date_c)
    # separa: amministrative/QC (ignora), codici ST FreeSurfer (dizionario), misure vere
    admin = [c for c in cols if c not in reverse and c not in key_like and is_admin(c)]
    st_cols = [c for c in cols if c not in reverse and c not in key_like and ST_PAT.match(c)]
    unknown = [c for c in cols if c not in reverse and c not in key_like
               and not is_admin(c) and not ST_PAT.match(c)]
    name_hint = [cat for cat, ks in {  # SOLO indizio, in commento
        "plasma": ["plasma", "nfl", "c2n", "precivity", "adx", "blennow"],
        "csf": ["csf", "upennbiomk", "elecsys", "fujirebio", "euroimmun", "mesoscale"],
        "pet": ["av45", "av1451", "fbb", "fbp", "suvr", "amyloid", "berkeley", "pet"],
        "volumes": ["ucsffsx", "ucsffsl", "ucsdvol", "roi", "fsx", "fsl"],
        "scale": ["mmse", "adas", "cdr", "moca", "faq", "ravlt"],
        "cofactor": ["ptdemog", "apoe", "dxsum", "demog"],
    }.items() if any(k in path.name.lower() for k in ks)]

    L = []
    L.append(f"# {'='*72}")
    L.append(f"# {var}")
    L.append(f"#   source: {path.name}   |   righe campionate: {len(df)}   |   colonne: {len(cols)}")
    if name_hint:
        L.append(f"#   INDIZIO categoria dal nome (NON deciso): {name_hint}")
    if admin:
        L.append(f"#   ignorate {len(admin)} colonne amministrative/QC (vedi IGNORE_* nello script)")
    if st_cols:
        L.append(f"#   {len(st_cols)} colonne FreeSurfer ST* -> servono il DIZIONARIO ADNI ST->regione")
        L.append(f"#     (es. {st_cols[:5]} ...): non elencate qui, si mappano col dizionario")
    L.append(f"#   profilo colonne di interesse (nome | tipo | distinti | note):")
    for c in cols:
        if c in admin or c in st_cols:
            continue                                    # gia' riassunte sopra
        p = prof[c]
        note = []
        if c in auto_rename: note.append(f"-> {auto_rename[c]} (CATALOG)")
        if c in id_c: note.append("cand. ID")
        if c in date_c: note.append("cand. DATA")
        if c in visit_c: note.append("cand. VISITA")
        if p["censored"]: note.append("censure >/<")
        if c in unknown: note.append("DA DECIDERE")
        L.append(f"#     {c:<24} | {p['kind']:<7} | {p['distinct']:>5} | {', '.join(note)}")
    L.append(f"# {'-'*72}")
    L.append(f"{var} = DatasetConfig(")
    L.append(f'    file_code="{code}",                          # <-- VERIFICA')
    L.append(f'    source="{path.name}",')
    L.append(f"    category=None,                              # <-- DECIDI" +
             (f"  (indizio: {name_hint})" if name_hint else ""))
    # id_column: convenzione ESPLICITA -> se c'e' RID usalo (standard ADNI), elencando alt
    if "RID" in id_c:
        alt_id = [c for c in id_c if c != "RID"]
        L.append(f'    id_column="RID",                            # standard ADNI (alt: {alt_id or "nessuna"}) VERIFICA')
    elif len(id_c) == 1:
        L.append(f'    id_column="{id_c[0]}",                      # rilevato, VERIFICA')
    else:
        L.append(f"    # id_column=?  candidati: {id_c or 'NESSUNO'}  <-- DECIDI")
    # date_column: ordine di preferenza ESPLICITO tra i candidati rilevati dai valori
    DATE_PREF = ["EXAMDATE", "SCANDATE", "DRAW_DATE", "DRAWDATE", "USERDATE", "PROCESSDATE"]
    chosen_date = next((d for d in DATE_PREF if d in date_c), None)
    if chosen_date:
        alt = [c for c in date_c if c != chosen_date]
        L.append(f'    date_column="{chosen_date}",{" "*(18-len(chosen_date))}# preferenza ADNI (alt: {alt or "nessuna"}) VERIFICA')
    elif len(date_c) == 1:
        L.append(f'    date_column="{date_c[0]}",                  # rilevato dai valori, VERIFICA')
    else:
        L.append(f"    # date_column=?  candidati (dai valori): {date_c or 'NESSUNO'}  <-- DECIDI")
    if len(visit_c) == 1:
        L.append(f'    viscode_reference="{visit_c[0]}",')
    if auto_rename:
        L.append(f"    rename={{                                    # SOLO match esatto col CATALOG")
        for r, s in auto_rename.items():
            L.append(f"        {r!r}: {s!r},")
        L.append(f"    }},")
    if unknown:
        L.append(f"    # {len(unknown)} colonne DA DECIDERE (rename/keep/scarta, o -> CATALOG.aliases):")
        L.append(f"    #   {unknown}")
    if st_cols:
        L.append(f"    # + {len(st_cols)} colonne ST* FreeSurfer da mappare col dizionario ADNI")
    L.append(f'    # constant_columns={{"METHOD_<CAT>": "<assay>"}},   # se biomarcatore: METTI il metodo')
    L.append(f"    # essential_columns=[...],  # keep_columns=[...]   # <-- scegli (nomi STANDARD)")
    L.append(f")")
    L.append("")
    _date_pref = ["EXAMDATE", "SCANDATE", "DRAW_DATE", "DRAWDATE", "USERDATE", "PROCESSDATE"]
    date_ok = any(d in date_c for d in _date_pref) or len(date_c) == 1
    id_ok = ("RID" in id_c) or len(id_c) == 1
    return var, "\n".join(L), {"unknown": len(unknown), "date": len(date_c),
                               "id_ok": id_ok, "admin": len(admin), "st": len(st_cols),
                               "date_ok": date_ok}


def main(folder: str = "."):
    reverse = getattr(config, "RENAME", {})
    csvs = sorted(p for p in Path(folder).glob("*.csv")
                  if not any(tok in p.name for tok in EXCLUDE))
    if not csvs:
        print(f"nessun CSV grezzo in {Path(folder).resolve()}"); return

    blocks, names, report = [], [], []
    for p in csvs:
        try:
            var, block, info = stub_for(p, reverse)
            blocks.append(block); names.append(var); report.append((p.name, info))
        except Exception as e:
            print(f"[skip] {p.name}: {type(e).__name__}: {e}")

    header = (
        '"""BOZZE auto-generate ALLA CIECA da generate_config_stubs.py - RIEMPI I TODO.\n'
        "Lo script ha solo OSSERVATO i file: categoria, metodo, essential e keep sono\n"
        "scelte tue. Il rename automatico copre solo i match ESATTI col CATALOG.\n"
        '"""\n'
        "from config import DatasetConfig\n\n\n"
    )
    footer = ("\nDATASETS_DRAFT = {d.file_code: d for d in (\n    "
              + ",\n    ".join(names) + ",\n)}\n")
    out = Path(folder) / "config_datasets_draft.py"
    out.write_text(header + "\n".join(blocks) + footer)

    print(f"scritto {out}  ({len(names)} file)\n")
    print(f"{'file':<50} {'vere':>5} {'ST*':>5} {'admin':>6} {'data?':>6} {'ID?':>6}")
    for name, i in report:
        dok = "ok" if i["date_ok"] else "DECIDI"
        idok = "ok" if i["id_ok"] else "DECIDI"
        print(f"{name:<50} {i['unknown']:>5} {i['st']:>5} {i['admin']:>6} {dok:>6} {idok:>6}")
    tot_u = sum(i["unknown"] for _, i in report)
    tot_st = sum(i["st"] for _, i in report)
    tot_a = sum(i["admin"] for _, i in report)
    print(f"\nTOTALE: {tot_u} misure vere DA DECIDERE  |  {tot_st} colonne ST* (-> dizionario ADNI)"
          f"  |  {tot_a} admin/QC ignorate")
    print(f"file con data da decidere: {sum(1 for _,i in report if not i['date_ok'])}"
          f"  |  file con ID da decidere: {sum(1 for _,i in report if not i['id_ok'])}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")