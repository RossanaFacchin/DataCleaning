# Pulizia dei dati ADNI — guida al codice

Questa cartella contiene la riscrittura della pulizia dei file ADNI, che prima era fatta con i
notebook `adni_cleaning1/2/3.ipynb`, l'oggetto `dataCleaner` e il file Excel
`ADNI_variables_statistics.xlsx`. Tutto gira in locale: CSV in ingresso, CSV in uscita, niente
datalake.

Aggiornata al 20/10/2026. Il *perché* di ogni scelta è in [`DECISIONI.md`](DECISIONI.md)
(citata qui con gli ID `D0NN`); le questioni ancora aperte sono in [`notes_CP.md`](notes_CP.md).

---

## 1. L'idea in una frase

Il lavoro è diviso tra **decisioni/dati** e **logica**:

| File | Contiene | Si modifica per… |
|---|---|---|
| `catalog.json` | **Cosa sono le variabili**: nome standard, definizione, unità, da quali colonne grezze arrivano, come si calcolano, codifiche | aggiungere o descrivere una variabile, rinominare una colonna di un file |
| `config.py` | **Come si pulisce ogni file**: una `DatasetConfig` per file, soglie (`POLICY`), ricodifiche (`RECODE`) | aggiungere un file o cambiare una regola di pulizia |
| `pipeline.py` | **Le operazioni**, scritte una volta sola | solo se serve un'operazione che non esiste |

Regola pratica: davanti a qualsiasi cosa chiediti *«è una decisione o un dato, oppure un
calcolo?»*. Un nome standard, una soglia o una lista di colonne è una decisione e va in
`config.py`/`catalog.json`. Un conteggio, un minimo o una dummy è un calcolo: lo fa la
pipeline, e non si scrive a mano da nessuna parte.

---

## 2. I file della cartella

| File | Cos'è |
|---|---|
| `catalog.json` | Catalogo delle variabili: unica fonte di verità (§4) |
| `config.py` | Configurazione dei file, `POLICY`, `RECODE`; carica e valida il catalogo (§5) |
| `pipeline.py` | Pulizia (cleaning 1 e 2), merge e armonizzazione (in standby), report, log (§6) |
| `export_catalog.py` | Vista tabellare del catalogo e dizionario dati dei file puliti (§8) |
| `generate_config_stubs.py` | Genera bozze di `DatasetConfig` osservando i CSV grezzi (§8) |
| `count_bridges.py` | Conta i campioni-ponte tra metodi (serve all'armonizzazione) |
| `cutoffs.json` | Soglie del profilo ATN: guidano un calcolo, quindi servono alla pulizia |
| `ranges.json` | Range `[min, max, direzione]` per colonna: metadati per il merge |
| `DECISIONI.md` / `notes_CP.md` | Registro delle decisioni prese / questioni aperte |

I CSV, sia grezzi sia di output, e i log di esecuzione non vanno in git (`.gitignore`).

---

## 3. Come si esegue

Dalla cartella `File Benedetta/`:

```bash
python pipeline.py
```

Il comando pulisce tutti i file registrati in `config.DATASETS` il cui CSV grezzo è presente
nella cartella; gli altri vengono saltati con un avviso. Per ogni file scrive:

| Output | Contenuto |
|---|---|
| `<FILE>_cleaned_01.csv` | dopo cleaning 1 |
| `<FILE>_cleaned_02.csv` | dopo cleaning 2 |
| `<FILE>_report.csv`, `<FILE>_report_02.csv` | statistiche di qualità per colonna (`profile()`) |
| `<FILE>_runlog.json` | log di esecuzione passo per passo (§7) |

Esempio di riferimento, ADNIMERGE: **11.458 righe e 2.409 soggetti** dopo cleaning 1.

Da Python, senza scrivere nulla su disco:

```python
import config, pipeline
df1, log1 = pipeline.run_cleaning1(config.ADNIMERGE)
df2, log2 = pipeline.run_cleaning2(df1, config.ADNIMERGE)
```

Importare `pipeline` non legge né scrive nulla: il disco si tocca solo in `run_all` e nel
`__main__`.

---

## 4. Il catalogo: `catalog.json`

Sostituisce le righe del vecchio Excel. È un file JSON perché contiene dati, non logica, come
`cutoffs.json` e `ranges.json`. Lo legge e lo **valida** `config.catalog()`: se c'è un errore,
il programma si ferma con un messaggio chiaro invece di produrre un rename sbagliato in
silenzio.

### 4.1 Una voce

La chiave è il **nome standard** della variabile:

```json
"AB42_CSF": {
  "domain": "Biomarker",
  "definition": "Beta-amiloide 1-42 nel liquor.",
  "unit": "pg/mL",
  "role": "predittore",
  "scope": "output",
  "dtype": null,
  "date_precision": null,
  "aliases": ["ADNI:*.ABETA", "ADNI:EUROIMMUN.BETA_AMYLOID_1_42"],
  "derived": null,
  "levels": null,
  "method_col": "METHOD_CSF",
  "omop_concept_id": null,
  "vocab_code": null,
  "admapper_ref": null,
  "standard_match": "none",
  "note": "Chiave = chiave di cutoffs.json.",
  "log_ref": ["D003"]
}
```

| Campo | Significato |
|---|---|
| `domain` | gruppo: ID, Visit, Demographic, Cognitive, Imaging, Biomarker, History, QC, Metadata… |
| `definition` | cosa misura, quando, come; deve bastare a chi non apre il codice |
| `unit` | unità in notazione UCUM (`a` = anni, `mm3`, `pg/mL`, `{score}`) |
| `role` | predittore, normalizzazione, metodo, qualita, metadato, identificativo… |
| `scope` | fin dove vive la variabile: `cleaning` (tolta a fine cleaning 1), `merge` (fino al merge), `output` (D032) |
| `dtype` / `date_precision` | `date` = da convertire in data; `month` = nota solo come mese/anno (D029) |
| `aliases` | colonne grezze da cui arriva (§4.2) |
| `derived` | come si calcola (§4.3) |
| `levels` | solo per le categoriche: etichetta → codice intero (§4.4) |
| `method_col` | colonna che dice con quale metodo è misurata la riga |
| `omop_concept_id`, `vocab_code`, `admapper_ref`, `standard_match` | codici standard: **solo se verificati** su una fonte ufficiale (D033) |
| `note`, `log_ref` | note libere; ID delle decisioni collegate |

In cima al file, sotto `_templates`, ci sono due modelli da copiare: **variabile estratta** da
un file e **variabile calcolata**. Le chiavi che iniziano con `_` sono ignorate.

### 4.2 Alias e rename

Un alias dice "questa colonna grezza è questa variabile standard". Formato
`DATASET:FILE.colonna`, dove `FILE` è il `file_code` della `DatasetConfig` oppure `*`:

| Alias | Vale per |
|---|---|
| `ADNI:ADNIMERGE.AGE` | solo la colonna AGE del file ADNIMERGE |
| `ADNI:*.PTGENDER` | la colonna PTGENDER in tutti i file ADNI |
| `*:*.SEX` oppure `SEX` | la colonna SEX in qualsiasi dataset |

Se più alias rivendicano la stessa colonna **vince il più specifico**: file preciso, poi
`ADNI:*`, poi `*:*`. Per esempio `TAU` vale `TTAU_PL` nei file plasma (alias per file) e
`TTAU_CSF` altrove (alias `ADNI:*`). Lo stesso alias allo stesso livello per due variabili è
un errore (D017).

Quando due colonne finirebbero sullo stesso nome (es. VISCODE e VISCODE2 → VISCODE), quella di
troppo si toglie prima del rename con `drop_columns` nella `DatasetConfig` (D016). Una
collisione non risolta dà un warning e viene registrata nel log.

### 4.3 Variabili derivate

`derived` è una lista di modi di calcolo, in ordine di preferenza:

```json
"AGE": {
  "aliases": ["ADNI:ADNI_DIAN_COMPARISON.VISITAGE"],
  "derived": [
    {"from": ["PTDOB", "EXAMDATE"], "by": "age_from_dob"},
    {"from": ["AGE_bl", "EXAMDATE", "EXAMDATE_bl"], "by": "age_from_baseline"}
  ]
}
```

Regole (D019):

- **Il dato misurato vince.** Se il file ha già la variabile tramite un alias, non si
  ricalcola. Se gli input ci sono, si calcola comunque per **confronto**: per AGE, le righe
  con differenza oltre ±0,5 anni finiscono nel log con un warning.
- **Si calcola quando manca**, con il primo modo che ha tutti gli input. Le righe rimaste senza
  valore vengono registrate nel log, per soggetto, con l'input mancante.
- `by` è una funzione di `pipeline.DERIVATIONS` (`age_from_dob`, `age_from_baseline`,
  `ratio`) oppure il nome di un passo dedicato (`add_visit_month`, `add_atn_profile`,
  `add_constant_columns`).

Il caso dell'età:
- in ADNIMERGE la colonna AGE è l'età **al baseline** → alias di `AGE_bl`; `AGE` alla visita si
  calcola come `AGE_bl` + tempo trascorso;
- in PTDEMOG AGE non c'è → si calcola da `PTDOB`;
- il risultato è arrotondato a 1 decimale (D030).

### 4.4 Categoriche: `levels` e `RECODE`

- `levels` (catalogo) è il **vocabolario standard**, valido ovunque, con il suo codice
  numerico: GENDER `{"female": 0, "male": 1}`, DX `{"CN": 0, "MCI": 1, "Dementia": 2}`… Per
  passare da etichetta a numero e viceversa: `config.encode(serie, "GENDER")` /
  `config.decode(...)`.
- `RECODE` (`config.py`) dice **come ogni file scrive** quei valori: `"Male"` in ADNIMERGE,
  `1` in PTDEMOG. È indicizzato per sorgente, `{"*": {...}, "PTDEMOG": {...}}`, e la mappa del
  file vince su quella generica.

Le categoriche restano **una colonna in stringa** fino al merge. Le dummy si creano dopo
(D026): una colonna per ogni livello del catalogo, così tutti i file hanno le stesse dummy.

---

## 5. La configurazione di un file: `DatasetConfig`

Esempio commentato (PTDEMOG):

```python
PTDEMOG = DatasetConfig(
    file_code="PTDEMOG",                    # = FILE negli alias del catalogo
    source="PTDEMOG_21Apr2026.csv",         # SEMPRE il file grezzo
    category="cofactor",                    # gruppo per il merge
    drop_columns=["VISCODE"],               # grezze tolte subito: si usa VISCODE2 (D016)
    drop_rows={"VISCODE": ["f"]},           # righe scartate per valore: screen fail (D028)
    missing_codes=[-4, "-4", -1, "-1", 9999, 9999.0],   # codici di "mancante" del file (D027)
    essential_columns=["GENDER", "MARRY", "ETHNICITY", "RACE"],  # tieni la riga se >=1 c'e'
    also_required=["PTDOB"],                # ...e in piu' questa deve esserci
    recode_columns=["GENDER", "MARRY", "ETHNICITY", "RACE"],
    make_dummies=False,                     # dummy dopo il merge (D026)
    keep_columns=[...],                     # colonne da tenere in cleaning 2 (nomi standard)
)
```

Tutte le liste usano i **nomi standard**, perché il rename avviene subito dopo il caricamento.
Fanno eccezione `drop_columns`, che agisce prima del rename e quindi usa i nomi grezzi, e
`missing_codes`, che contiene valori e non nomi.

**Codici di mancante (D027).** I testi come "Unknown" o "NA" diventano NaN sempre. I codici
numerici (−4, −1, 9999) solo dove sono dichiarati, perché in alcune colonne sono valori veri:
in ADNIMERGE, −4 e −1 in RAVLT_learning/forgetting sono differenze di punteggio reali
(ADNIMERGE ha `missing_codes=[]`). Se un file non dichiara nulla vale il default di prima
(−4, 9999).

**Colonne di metodo.** `constant_columns={"METHOD_CSF": "elecsys"}` riempie la colonna metodo
della riga con il saggio del file. È un'informazione di riga: dopo il merge può avere valori
diversi da una riga all'altra (D020, in standby).

---

## 6. Cosa fa la pipeline, passo per passo

**Cleaning 1** — `run_cleaning1(cfg)`, un file:

| Passo | Cosa fa | Ex notebook |
|---|---|---|
| `load` | legge il CSV grezzo | download dal datalake |
| `drop_columns` | toglie le colonne grezze indesiderate | — |
| `replace_unknown` | segnaposto di mancante → NaN (testi sempre, codici per file) | `replace_unknown_values` |
| `rename_variables` | nomi grezzi → nomi standard con gli alias del catalogo | `new_variable_names` |
| `decensor` | `">1700"` → 1700 (biomarcatori, se attivo) | — |
| `drop_rows_by_value` | scarta righe per valore (es. screen fail) | — |
| `drop_required` / `drop_if_all_none` | scarta righe senza ID/data o senza misure essenziali | `drop_if_all_none` ×2 |
| `parse_dates` | converte in data `date_column` e le variabili `dtype: date`; per le date mese/anno mette il giorno 15, **solo** ai valori MM/YYYY (D029) | `to_date_format` |
| `dedup_visits` + `add_visit_month` | una riga per soggetto e data; `VISIT_MONTH` | `find_exam_code` |
| `derive_variables` | calcola le derivate del catalogo (AGE, rapporti) | `add_calculated_age` |
| `recode` | categorie → etichette standard | `categorize_*` |
| `clean_fs_fields` | normalizza FLDSTRENG / FSVERSION (se attivo) | — |
| `add_constant_columns` | colonne metodo | — |
| `add_atn_profile` | profilo ATN da `cutoffs.json` (se `compute_atn`) | `get_ATN_profile` |
| `drop_scope_columns` | toglie le variabili con `scope: cleaning` (es. PTDOB, EXAMDATE_bl) | — |

**Cleaning 2/3** — `run_cleaning2(df, cfg)`:

| Passo | Cosa fa |
|---|---|
| `drop_sparse_columns` | toglie le colonne con meno del 65% di valori validi (se attivo) |
| `remove_single_visit_subjects` | toglie i soggetti con una sola visita (se attivo) |
| `make_dummies` | dummy delle categoriche (oggi spento: si fa dopo il merge) |
| `normalize_volumes_icv` | volumi in % di ICV, rinominati `<vol>%ICV` (se attivo) |
| `keep_only_columns` | tiene `keep_columns` più, in automatico, le derivate del catalogo, le dummy, i %ICV e le colonne metodo |

**Merge e armonizzazione** (`merge_category`, `run_harmonization`) esistono ma sono **in
standby**: la strategia di merge è ancora da decidere (`notes_CP.md` §D.9).

---

## 7. Log e report

| Cosa | Dove | Risponde a |
|---|---|---|
| Run log | `<FILE>_runlog.json` | *cosa è successo* in questa esecuzione: per ogni passo righe e colonne prima/dopo, mappa di rename, codici convertiti per colonna, valori non ricodificati, derivate calcolate o non calcolabili, controlli di coerenza; data e commit git |
| Report | `<FILE>_report*.csv` | com'è fatto il dataset: tipo, range, validi/mancanti, soggetti, coorti scoperte |
| Registro decisioni | `DECISIONI.md` | *perché* si fa così |

I run log possono contenere RID (per esempio i soggetti per cui l'età non è calcolabile):
restano in locale e non si condividono.

---

## 8. Strumenti

- **`python export_catalog.py`** → `catalog_table.csv`, il catalogo in forma di tabella da
  consultare (non modificarlo: la fonte è il JSON), più alcuni controlli stampati a video.
- **`python export_catalog.py ADNIMERGE_cleaned_02.csv`** → `ADNIMERGE_cleaned_02_dizionario.csv`:
  per ogni colonna del file pulito, la voce del catalogo (anche per dummy e `%ICV`) e l'elenco
  delle colonne non riconducibili al catalogo.
- **`python generate_config_stubs.py [cartella]`** → `config_datasets_draft.py`: bozze di
  `DatasetConfig` per i CSV della cartella, con i rename già noti dal catalogo e la lista delle
  colonne da decidere.

---

## 9. Ricette

**Aggiungere una variabile.** Si copia `_templates.variabile_estratta` in `catalog.json`,
con chiave = nome standard e alias verso la colonna grezza. Se è categorica servono anche
`levels` e la mappa in `RECODE`.

**Rinominare una colonna di un file nuovo.** Si aggiunge l'alias
`"ADNI:<file_code>.<colonna>"` alla voce standard del catalogo. Non si tocca né la
`DatasetConfig` né la pipeline.

**Aggiungere una variabile calcolata.** Si copia `_templates.variabile_calcolata`. Se il modo
di calcolo non esiste ancora, si aggiunge una funzione in `pipeline.DERIVATIONS`: è l'unico
caso in cui si tocca la pipeline.

**Aggiungere un file.**
1. `generate_config_stubs.py` per avere la bozza.
2. Una `DatasetConfig` in `config.py`, registrata in `DATASETS`.
3. Gli alias nel catalogo.
4. Si esegue la pipeline e si controllano il run log e `export_catalog.py` sul file pulito.

---

## 10. Dal vecchio mondo al nuovo

| Prima | Ora |
|---|---|
| Excel `ADNI_variables_statistics.xlsx`, letto e riscritto a ogni giro | `catalog.json` (input) + `profile()` (output che si rigenera) |
| `parameter`, `variable_code`, `Unit`, `metadati_*` | `domain`, chiave del catalogo + `aliases`, `unit`, `role` |
| `rename` per file e `CATEGORY_RENAME` in `config.py` | alias qualificati nel catalogo (migrati il 20/10/2026, D017) |
| `categorize_*` con numeri dentro le funzioni | `RECODE` per sorgente → etichette; `levels` → numeri |
| `add_calculated_age`, `recompute_age=True`, `derived_ratios` | variabili `derived` del catalogo, calcolate quando servono |
| checkpoint "apri l'Excel e controlla" | run log + report + `export_catalog.py` |

---

## 11. Da verificare

- Le **definizioni** del catalogo sono in bozza.
- Due rename ereditati dal generatore di bozze sono dubbi: CDR `CDGLOBAL → CDRSB` e APOERES
  `GENOTYPE → APOE4` (`notes_CP.md` D.14).
- **Codici standard**: verificati solo MMSE (LOINC 72106-8) e MoCA (LOINC 72172-0) (D033).
- Le mappature di `RECODE` per PTDEMOG (`notes_CP.md` D.13).
