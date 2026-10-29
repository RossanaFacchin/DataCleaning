# CLAUDE.md — Linee guida del progetto DataCleaning

File guida per chi lavora (persone e Claude) nella cartella `DataCleaning`.
È un documento **vivo**: va aggiornato quando cambia la struttura o una regola.
Lingua del progetto: **italiano** (commenti, docstring, note, messaggi a schermo).

---

## 1. Contesto

Riscrittura della pulizia dati del progetto **ADNI** (Alzheimer's Disease
Neuroimaging Initiative). Il codice originale era una serie di notebook
(`adni_cleaning1/2/3.ipynb`, `automated_merge.py`) basati su un oggetto opaco
`dataCleaner`, su un Excel di supporto (`ADNI_variables_statistics.xlsx`) letto e
riscritto a ogni giro, e sul datalake.

Obiettivo: una pipeline **locale** (CSV in ingresso/uscita, niente datalake),
**config-driven**, leggibile e riproducibile, che porti ogni file ADNI grezzo a un
dataset pulito con nomi standard, e poi unisca (merge) i file per categoria.

Possibile estensione futura: inclusione di altri dataset di ADNI, ma anche poi dataset di altre banche dati.

---

## 2. Struttura della cartella

| Percorso | Cos'è | Stato |
|---|---|---|
| `File Benedetta/` | **Versione di riferimento attuale** del framework (config + pipeline) | Si lavora qui |
| `File Benedetta/config.py` | Decisioni: POLICY, RECODE, `DatasetConfig` dei file, merge; carica e valida il catalogo | Si modifica |
| `File Benedetta/catalog.json` | **Catalogo delle variabili**: definizione, unità, alias `DATASET:FILE.colonna`, derivate, levels, scope, codici standard | Dato, unica fonte di verità sulle variabili |
| `File Benedetta/pipeline.py` | Logica di pulizia, merge, armonizzazione, report | Si modifica solo per *nuove operazioni* |
| `File Benedetta/export_catalog.py` | Vista tabellare del catalogo e dizionario dati dei file puliti (solo consultazione) | Strumento |
| `File Benedetta/cutoffs.json` | Soglie ATN (trasformano i dati → cleaning) | Dato |
| `File Benedetta/ranges.json` | Range `[min, max, direzione]` per colonna, sezioni `normalization`/`volume`/`cofattori` (metadati → merge) | Dato |
| `File Benedetta/generate_config_stubs.py` | Genera bozze di `DatasetConfig` osservando i file | Strumento |
| `File Benedetta/config_datasets_draft.py` | Output del generatore: bozze con TODO | Generato, da rivedere |
| `File Benedetta/count_bridges.py` | Conta i campioni-ponte tra metodi (per l'armonizzazione) | Strumento |
| `File Benedetta/README_config.md` | Guida al codice attuale (config, catalogo, pipeline, log) | Aggiornato al 20/10/2026 |
| `File Benedetta/NOTE_PER_ROSSANA.md` | Errori tipici e checklist | Riferimento |
| `File Benedetta/notes_CP.md` | Note di Chiara: domande, proposte, cose da fare | **Backlog di lavoro** (questioni aperte) |
| `File Benedetta/DECISIONI.md` | Registro storico delle decisioni chiuse (dati e struttura del codice) | Aggiornato a fine sessione |
| root: `config.py`, `pipeline.py`, `README_config.md` | Versione precedente (solo cleaning 1 ADNIMERGE) | Storica |
| root: `*_settings.json` | Vecchi JSON di range, ora accorpati in `ranges.json` | Storici |
| root: `README.md`, `TestCleaning`, notebook, PDF | EDA iniziale e documentazione del vecchio processo | Riferimento |

I CSV (dati grezzi e output) **non vanno in git** (`.gitignore`): sono dati clinici.

---

## 3. Il principio fondamentale: config = decisioni, pipeline = logica

Davanti a qualsiasi cosa chiedersi: **«è una decisione/un dato, o è un calcolo?»**

- **Decisione o dato** (nome standard di una variabile, soglia, lista di colonne,
  mappa di ricodifica, metodo/assay di un file, file di input/output) →
  `config.py`, o un file JSON letto dal config se è un dato tabulare.
- **Calcolo** (quanti mancanti, min/max, dedup, dummy, normalizzazione) →
  `pipeline.py`, e il risultato **non si scrive mai a mano** da nessuna parte.

Corollari:
- Aggiungere un file nuovo = **nuova `DatasetConfig`**, non nuova funzione
  (salvo vera eccezione isolata).
- Le statistiche (tipo, range, validi/mancanti, keep/drop) le rigenera `profile()`
  in un CSV di report: l'output non è mai anche input.
- I JSON di dati clinici restano file: non si incollano come dict nel `.py` e non
  si ricopiano i valori nella pipeline "per comodità".

---

## 4. Regole di scrittura del codice

### 4.1 Contratto del modulo `pipeline.py`
- **Nessun I/O all'import.** `from pipeline import run_cleaning1` non deve leggere
  né scrivere nulla. Niente codice eseguibile fuori da funzioni o dal `__main__`.
- **Funzioni pure `df -> df`** (o `df -> (df, info)` quando serve un log):
  prendono un DataFrame e ne restituiscono uno nuovo (`df.copy()`), senza stato globale.
- **Composizione in memoria.** Gli stadi si passano DataFrame, non CSV riletti da
  disco. Si scrive su disco solo alla fine di ogni stadio (`save_dataset`, `__main__`).
- **Un nome = un contratto.** Mai ridefinire una funzione con lo stesso nome e un
  tipo di ritorno diverso. Si riusa la stessa funzione (es. `drop_if_all_none`).
- **Orchestratori** (`run_cleaning1`, `run_cleaning2`, `run_all`) leggono il config
  e chiamano le funzioni in ordine; i conteggi (righe rimosse ecc.) li calcolano loro.
  `run_cleaning1` e `run_cleaning2` restituiscono `(df, log)`: ogni passo si registra con
  `df = _log_step(log, "nome_passo", df, funzione(df), **dettagli)`. Un passo nuovo
  va sempre registrato così; i passi non eseguibili sui dati vanno in `_log_skip`.

### 4.2 Config
- `source` è **sempre il file grezzo** e non si sovrascrive; gli output sono campi
  separati (`output_cleaned1`, `output_cleaned2`, `report_file`).
- Le liste di colonne nel `DatasetConfig` usano **nomi standard** (il rename gira
  per primo, vedi §5).
- **Ogni soglia ha un solo significato.** `MISSING_KEEP_THRESHOLD` etichetta il
  report (consultiva); `SPARSE_KEEP_THRESHOLD` cancella colonne (distruttiva).
- Colonne generate (dummy, `VISIT_MONTH`, `AGE_bl`, volumi `%ICV`, costanti di
  metodo) si tengono **in automatico**: non si elencano a mano.

### 4.3 Robustezza e trasparenza
- Fallire **in modo esplicito**: se manca un file o un dato necessario, errore
  chiaro (es. `cutoffs.json` mancante con `compute_atn=True`), mai dati muti.
- Segnalare a schermo/log le incoerenze (es. "colonne richieste ma assenti")
  invece di correggerle in silenzio.
- Niente `assert` che non possono fallire.
- «Gira» non vuol dire «giusto»: dopo ogni modifica controllare shape, n. soggetti,
  colonne aggiunte/perse e il report `profile()`.

### 4.4 Stile
- Commenti e docstring in italiano, densità simile al codice esistente.
- Docstring che dicono *cosa* fa, *perché*, e a quale funzione del vecchio
  notebook corrisponde (es. "ex `remove_sub_1visit`").
- Le scelte nate da una discussione si annotano nel codice con l'ID della decisione
  in `DECISIONI.md` (es. `# [D019]`). I vecchi riferimenti `[nota Chiara #n]` restano
  validi: sono mappati sugli ID in `DECISIONI.md`.
- Dipendenze minime: `pandas`, `numpy`, `matplotlib` (vedi `requirements.txt`).

### 4.5 Semplicità
- Il codice deve restare **semplice, lineare e comprensibile** a una prima lettura.
- **Prediligere le funzioni esistenti**: se una funzione fa già la cosa (es.
  `recompute_age`, ex `add_calculated_age`), la si estende con il minimo indispensabile
  invece di sostituirla con un meccanismo nuovo.
- Soluzioni dirette prima di quelle generiche: niente motori, registri di funzioni,
  dispatcher o livelli di astrazione "per il futuro" se oggi servono per uno o due casi.
- Non generare elementi che poi non servono: campi di log, dizionari di dettaglio,
  opzioni, template o colonne che nessuno legge o usa.
- Se una decisione sembra richiedere codice complesso, **fermarsi e proporre a Chiara**
  una versione semplice e una completa, con il costo di ciascuna, prima di scriverlo.

---

## 5. Le fasi della pipeline (stato attuale)

**Cleaning 1** — `run_cleaning1(cfg)`, singolo file:
`load` → `load_columns` (lista bianca grezza, D044) → `drop_columns` (grezze, D016) → `replace_unknown` (codici del file, D027) →
**`rename_variables` (per primo)** → `decensor` (opz.) → `drop_rows_by_value` (es. screen
fail, D028) → `drop_if_all_none` per ogni gruppo di `row_filters` (D045) → `parse_dates` (date_column + variabili con `date_precision` nel catalogo;
giorno 15 solo per `date_precision: month`, D029) → `dedup_visits` + `add_visit_month` →
`derive_variables` (variabili `derived` del catalogo: AGE da PTDOB o da AGE_bl a 1
decimale, rapporti; il misurato vince, D019/D030) → `recode` (in **etichette stringa
standard**, per sorgente) → `clean_fs_fields` (opz.) → `add_constant_columns`
(metodo/assay) → `add_atn_profile` (opz.) → `drop_scope_columns` (variabili con
`scope: cleaning`, es. PTDOB, D032)

**Cleaning 2/3** — `run_cleaning2(df, cfg)`, singolo file, in memoria:
`drop_sparse_columns` → `remove_single_visit_subjects` → `make_dummies` (spento: le dummy
si fanno dopo il merge, D026) → `normalize_volumes_icv` (rinomina in `<vol>%ICV`) →
`keep_only_columns`

**Attenzione alle date.** Nessuna data va "normalizzata" in blocco: l'imputazione del
giorno vale solo per le variabili con `date_precision: month` nel catalogo e solo per i valori
`MM/YYYY`. Ogni modifica che tocca date o età va verificata riga per riga contro il grezzo.

**Armonizzazione + merge per categoria** — `merge_category` / `run_harmonization`:
impila i file puliti di una categoria (long), armonizza le misure multi-metodo su un
metodo di riferimento calibrando sui campioni-ponte (Deming / Passing-Bablok),
collassa le visite entro `buffer_days`, salva `<CATEGORIA>_consolidated.csv` e
l'artefatto `harmonization_fit_<categoria>.json`.

**Report** — `profile()` dopo cleaning 1 e dopo cleaning 2.

**Log di esecuzione** — in `File Benedetta/logs/`, con data e ora nel nome (storico, D042): `<FILE>_runlog_<AAAAMMGG-HHMM>.json` per ogni file (passi di cleaning 1 e 2: righe
e colonne prima/dopo, mappa di rename, valori non ricodificati, passi saltati, data e
commit git) e `<CATEGORIA>_mergelog_<AAAAMMGG-HHMM>.json` per il merge. Contengono o potranno contenere
RID: sono in `.gitignore` e non vanno condivisi. Il *perché* delle scelte sta invece in
`DECISIONI.md`.

**Entry point** — `python pipeline.py` (da dentro `File Benedetta/`) esegue `run_all()`
su tutti i `config.DATASETS`, saltando con avviso i file il cui `source` non c'è.
Sulla macchina di Chiara Python è quello di Anaconda: `~/anaconda3/python.exe`
(il comando `python` di Windows non è configurato).

---

## 6. Elementi chiave di `config.py` e `catalog.json`

- **`catalog.json`** (D006, D017, D018): unica fonte di verità sulle variabili. Chiave =
  nome standard; campi `domain`, `definition`, `unit` (UCUM), `worsening` (direzione di peggioramento, D040), `role`, `scope`
  (`cleaning`/`merge`/`output`), `date_precision` (presente = data: `day`/`month`/`year`), `aliases`, `derived`, `levels`,
  `method_col`, codici standard, `note`, `log_ref`. Letto e validato da `config.catalog()`
  (errore esplicito se qualcosa non torna). **Mai** rimettere variabili, alias o rename nel
  `.py`; mai inserire codici standard non verificati su una fonte ufficiale (D033).
- **Alias e precedenza del rename** (D017): `DATASET:FILE.colonna`, con `FILE` = `file_code`
  o `*`; il nome nudo vale `*:*`. Vince il più specifico: file preciso > `ADNI:*` > `*:*`.
  Stesso alias allo stesso livello per due variabili = errore. Per rinominare una colonna di
  un file nuovo si aggiunge un alias al catalogo, non un campo nel `DatasetConfig`.
- **Derivate** (D019): `derived` = modi di calcolo in ordine di preferenza
  (`{"from": [...], "by": "..."}`); `by` è una funzione di `pipeline.DERIVATIONS`
  (`age_from_dob`, `age_from_baseline`, `ratio`) o un passo dedicato. Il valore misurato
  (alias) vince sempre; per AGE c'è un controllo di coerenza ±0,5 anni.
- **Evoluzioni** (D036): la madre dichiara `evolution: ["dummy"]` (servono `levels`) o
  `["pct_icv"]` (volumi in mm3); le figlie `<VAR>_<livello>` e `<VOL>%ICV` sono **generate**
  dal caricamento (`generated = true`, ereditano domain/role/scope) e non si scrivono nel JSON,
  salvo per dare loro definizione o codici propri. Dummy: dopo il merge, reversibili
  (`undummy`); %ICV: sostituisce il volume in mm3; ICV resta in mm3 (D035).
- **POLICY**: segnaposto dei mancanti, prefissi censurati, soglie, giorno imputato
  (`DOB_IMPUTED_DAY`), decimali dell'età, tolleranze delle derivate. I mancanti sono su due
  livelli (D027): `MISSING_STRINGS` valgono sempre; i **codici numerici** (−4, −1, 9999) si
  dichiarano per file in `DatasetConfig.missing_codes`, perché in alcune colonne sono valori
  veri (es. RAVLT in ADNIMERGE). Mai aggiungere un codice numerico globale senza controllare
  le distribuzioni.
- **`RECODE`** per sorgente: `{"*": {...}, "<file_code>": {...}}`, la mappa del file vince;
  le etichette d'arrivo sono i `levels` del catalogo (`config.encode`/`decode` per i numeri).
  `RECODE_MULTI` gestisce i valori multipli (RACE `1|5` → mixed).
- **`DatasetConfig`**: scheda d'identità di ogni file (dataset, chiavi, categoria, filtri,
  codici di mancante, flag delle operazioni, output).
- **`MergeConfig` / `CATEGORY_MERGE`** e **`HarmonizeConfig` / `HARMONIZE`**: regole
  di merge e armonizzazione per categoria (decisioni, non codice).
- **Armonizzazione = una riga**: il metodo/assay è il file stesso, si assegna con
  `constant_columns={"METHOD_<CAT>": "..."}`. Mai mescolare a mano misure di assay
  diversi: non sono numericamente intercambiabili.
- `cutoffs.json` = cleaning (guida un calcolo); `ranges.json` = merge (descrive
  metadati). Non confonderli.

---

## 7. Checklist prima di consegnare una modifica

- [ ] Nessuna riga eseguibile fuori da funzioni o dal `__main__`.
- [ ] `source` = file grezzo; output come campi del config.
- [ ] Passi collegati in memoria, nessun CSV riletto tra un passo e l'altro.
- [ ] Nessuna funzione ridefinita con contratto diverso.
- [ ] Liste di colonne, soglie, mappe → config; calcoli → pipeline.
- [ ] Colonne derivate tenute in automatico, non elencate a mano.
- [ ] Ogni soglia ha un solo significato.
- [ ] File nuovo → nuova `DatasetConfig` + alias in `catalog.json`, non nuova funzione.
- [ ] `export_catalog.py` sul file pulito: nessuna colonna fuori dal catalogo (o spiegata).
- [ ] Dati JSON letti dal config, non copiati nel `.py`.
- [ ] Eseguito e verificati shape / soggetti / colonne / report.

---

## 8. Come lavorare con Claude su questo progetto

- Prima di proporre codice, verificare se la cosa è **decisione** (config) o
  **calcolo** (pipeline), e dirlo.
- Le scelte cliniche/metodologiche (soglie, mapping, metodo di riferimento,
  strategia di merge, quali colonne tenere) sono **decisioni di Chiara**: proporre
  opzioni motivate, non deciderle in silenzio.
- Per ogni modifica indicare: cosa cambia, perché, quale funzione del vecchio
  notebook coinvolge, e l'effetto atteso su righe/colonne.
- Tenere il codice **fedele al comportamento del notebook originale** salvo
  modifica esplicitamente decisa (e annotata).
- Le questioni aperte stanno in `File Benedetta/notes_CP.md`: consultarle quando si
  tocca una parte collegata, e aggiornarle quando una questione si chiude.
- **Registro decisioni (`File Benedetta/DECISIONI.md`).** A fine sessione, se è stata
  presa una decisione sulla pulizia dei dati o sulla struttura del codice, Claude:
  1. aggiunge una voce con il prossimo ID libero (`D0NN`), data, area (*Dati* /
     *Struttura*), problema, decisione, alternative scartate, impatto e stato;
  2. aggiorna l'indice in cima al file;
  3. se la decisione ne cambia una precedente, non la cancella ma la marca
     *Superata da D0NN*;
  4. se la decisione chiude una questione di `notes_CP.md`, lascia lì il rimando all'ID;
  5. mostra a Chiara le voci aggiunte.
  Prima di proporre qualcosa, controllare in `DECISIONI.md` se è già stato deciso.
  L'impatto si scrive solo con conteggi aggregati, mai con dati di singoli partecipanti.
- Quando una regola di questo file cambia, aggiornare questo file.

---

## 9. Questioni aperte / incoerenze note

- `catalog.json` da rivedere: definizioni in bozza, due rename dubbi migrati tali e quali
  (CDR `CDGLOBAL → CDRSB`, APOERES `GENOTYPE → APOE4`), codici standard quasi tutti vuoti
  (`notes_CP.md` D.14, `DECISIONI.md` D017/D033).
- `scope: merge` (update_stamp, HAS_QC_ERROR) è dichiarato ma non ancora applicato: si
  applicherà con il merge (in standby). Le liste `keep_columns` restano da semplificare.
- `NOTE_PER_ROSSANA.md` cita `README_armonizzazione_merge.md`, che non è nel repo.
- Root vs `File Benedetta/`: esistono due versioni di `config.py`/`pipeline.py`.
  Da decidere se archiviare quelle in root.
- Strategia di merge da rivedere (outer join, suffissi di metodo, match con buffer,
  log delle distanze): vedi `notes_CP.md` §D.9.
- Altre proposte in sospeso: vedi `notes_CP.md` §A–D. (Filtri di riga a gruppi: D045; lista bianca
  iniziale `load_columns`: D044, da estendere agli altri 31 file prima di togliere `keep_columns`;
  arrotondamento età: D030; metadati dopo dummy/volumi: dizionario dati di `export_catalog.py`.)
