# Registro delle decisioni

Traccia storica delle decisioni **chiuse** sulla pulizia dei dati e sulla struttura del
codice. Le questioni ancora aperte stanno in `notes_CP.md`; quando una si chiude, si
registra qui e in `notes_CP.md` si lascia il rimando all'ID.

**Come si usa**
- Una voce per decisione, con ID progressivo `D0NN` che non si riusa né si rinumera.
- Una decisione non si cancella: se cambia, si aggiunge una voce nuova e la vecchia passa a
  stato *Superata da D0NN*.
- Nel codice si cita l'ID nel commento (es. `# [D021]`); nel catalogo nel campo `log_ref`.
- **Area**: *Dati* (come si pulisce/trasforma) oppure *Struttura* (come è organizzato il codice).
- **Stato**: *Già applicata* · *Da implementare* · *Implementata* · *Rinviata* · *Superata da …*
- L'impatto si scrive con conteggi aggregati (righe, soggetti, colonne), mai con dati a livello
  di partecipante.
- Aggiornato da Claude a fine sessione quando si prende una decisione, e rivisto da Chiara.

---

## Indice

| ID | Data | Area | Decisione in breve | Stato |
|---|---|---|---|---|
| D001 | 31/08/2026* | Dati | Rinomina secondo convenzione interna con alias multipli | Già applicata |
| D002 | 31/08/2026* | Dati | PTGENDER / SEX / Gender → GENDER | Già applicata |
| D003 | 31/08/2026* | Dati | ABETA / TAU / PTAU di ADNIMERGE → `*_CSF`, considerati Elecsys | Già applicata, da verificare |
| D004 | 12/10/2026 | Dati | AGE: età al baseline o alla visita? | Superata da D019 |
| D005 | 31/08/2026* | Dati | Test cognitivi: solo punteggi totali | Già applicata |
| D006 | 15/10/2026 | Struttura | Catalogo in JSON, alias qualificati, nuovi campi | Implementata (20/10/2026) |
| D007 | 15/10/2026 | Dati | Metodo di misura in colonna separata | Da implementare (precisata da D020) |
| D008 | 31/08/2026* | Struttura | Config = decisioni, pipeline = logica; niente round-trip su CSV | Già applicata |
| D009 | 31/08/2026* | Struttura | Rename per primo, CATALOG indicizzato per nome standard | Già applicata |
| D010 | 31/08/2026* | Dati | RECODE in etichette stringa standard, non numeri | Già applicata |
| D011 | 31/08/2026* | Dati | Soglia del report e soglia di cancellazione separate | Già applicata |
| D012 | 31/08/2026* | Dati | Volumi normalizzati rinominati `<vol>%ICV` | Già applicata |
| D013 | 31/08/2026* | Dati | Scarto righe senza volumi spostato dopo il merge | Già applicata |
| D014 | 19/10/2026 | Struttura | Registro decisioni in `DECISIONI.md`, aggiornato da Claude | Implementata |
| D015 | 19/10/2026 | Struttura | Log di esecuzione automatico per ogni file | Implementata (20/10/2026) |
| D016 | 19/10/2026 | Dati | Drop dichiarato prima del rename (`drop_columns`), niente priorità tra alias | Implementata (20/10/2026) |
| D017 | 19/10/2026 | Struttura | Sintassi e precedenza degli alias `DATASET:FILE.colonna` | Implementata (20/10/2026) |
| D018 | 19/10/2026 | Struttura | Schema di `catalog.json`: estratte, derivate, levels, template | Implementata (20/10/2026) |
| D019 | 20/10/2026 | Dati | AGE: alias + derivata, il misurato vince, controlli e log | Implementata (20/10/2026) |
| D020 | 19/10/2026 | Dati | Colonna metodo per categoria: resta `METHOD_<CAT>` per riga, proposta `<CAT>_METHOD` in standby | Rinviata |
| D021 | 19/10/2026 | Struttura | Armonizzazione fuori perimetro: ora solo pulizia | Rinviata |
| D022 | 19/10/2026 | Dati | Nessun livello di riferimento per le dummy (per ora) | Già applicata |
| D023 | 31/08/2026* | Dati | Scarto riga se manca anche una sola colonna obbligatoria (ID, data) | Già applicata |
| D024 | 31/08/2026* | Dati | Report `profile()` con soggetti e visite, anche dopo cleaning 2 | Già applicata |
| D025 | 31/08/2026* | Dati | Collasso delle visite outer, nessuna riga persa nel merge | Già applicata |
| D026 | 20/10/2026 | Dati | Dummy create dopo il merge, non in cleaning 2 | Implementata |
| D027 | 20/10/2026 | Dati | Codici numerici di mancante dichiarati per file | Implementata |
| D028 | 20/10/2026 | Dati | Scarto delle righe per valore (screen fail `VISCODE == "f"`) | Implementata |
| D029 | 20/10/2026 | Dati | Date note solo come mese/anno: giorno imputato al 15 | Implementata |
| D030 | 20/10/2026 | Dati | Età calcolata anche da data di nascita, arrotondata a 1 decimale | Implementata |
| D031 | 20/10/2026 | Dati | PTDEMOG e i suoi codici portati dal branch della collega | Implementata |
| D032 | 20/10/2026 | Struttura | Campo `scope` nel catalogo (ciclo di vita delle variabili) | Implementata in parte (20/10/2026) |
| D033 | 20/10/2026 | Dati | Codici standard: solo verificati (MMSE, MoCA su LOINC) | Implementata in parte |
| D034 | 20/10/2026 | Dati | Effetti collaterali del catalogo: EXAMDATE_bl esce, update_stamp diventa data | Implementata |
| D035 | 26/10/2026 | Dati | ICV resta in mm3 quando si normalizzano i volumi | Implementata |
| D036 | 26/10/2026 | Struttura | Evoluzioni nel catalogo: dummy e %ICV come voci figlie generate | Implementata |
| D037 | 26/10/2026 | Struttura | Separatore delle dummy: `/` (es. `GENDER/male`) | Implementata |
| D038 | 26/10/2026 | Struttura | `dtype` eliminato: è una data chi ha `date_precision` (`day`/`month`); modelli del catalogo separati | Implementata |
| D039 | 26/10/2026 | Dati | `date_precision: year`: date note solo come anno, imputate al 1° luglio | Implementata |
| D040 | 26/10/2026 | Struttura | Campo `worsening` nel catalogo: direzione di peggioramento (`increase`/`decrease`) | Implementata |
| D041 | — | Struttura | *Citata nel codice (rapporti in `config.RATIOS`, `derived` solo descrittivo) ma voce mai scritta: da completare* | — |
| D042 | 29/10/2026 | Struttura | Storico dei log: runlog e mergelog in `logs/` con data e ora nel nome | Implementata |
| D043 | 29/10/2026 | Struttura | `evolution` solo per `dummy`/`pct_icv`: rapporti e APOE4 si dichiarano con `derived` sulla figlia | Implementata |
| D044 | 29/10/2026 | Struttura | `load_columns`: lista bianca di colonne grezze subito dopo il load; avvisi su colonne fuori catalogo e filtri di riga | Implementata (ADNIMERGE, PTDEMOG) |
| D045 | 29/10/2026 | Struttura | `row_filters` (gruppi "almeno uno") sostituisce i tre campi dei filtri di riga; `dedup_columns` separata | Implementata |

\* Data indicativa: decisioni prese prima, già presenti nel codice a quella data (dopo la quale
il codice non è cambiato in modo significativo).

**Corrispondenza con i riferimenti già presenti nel codice**

| Nel codice | ID |
|---|---|
| `[nota Chiara #1]` | D023 |
| `[nota Chiara #3]` | D010 |
| `[nota Chiara #4]` | D009 |
| `[nota Chiara #5]` | D024 |
| `[note Chiara #7/#10]` | D025 |
| `[nota Chiara #9]` | D013 |
| `[nota Chiara #11]` | D012 |

---

## Decisioni dal documento metodologico (12 e 15/10/2026)

### D001 · Rinomina secondo convenzione interna
- **Area:** Dati · **Stato:** Già applicata
- **Problema:** nomi diversi tra file per la stessa variabile (ADNIMERGE, PTDEMOG).
- **Decisione:** ogni variabile ha un nome interno del progetto; i nomi di origine sono alias.
- **Fonte:** scelta dell'analista.
- **Impatto:** da completare con il run log (D015).

### D002 · Unificazione di GENDER
- **Area:** Dati · **Stato:** Già applicata
- **Problema:** tre nomi di origine (PTGENDER, SEX, Gender) per lo stesso dato.
- **Decisione:** un'unica variabile `GENDER`.
- **Da verificare:** la codifica di PTGENDER in PTDEMOG e in ADNIMERGE può differire (Q4 del
  documento metodologico); se differisce si gestisce in RECODE per sorgente (D018).

### D003 · Biomarcatori CSF di ADNIMERGE
- **Area:** Dati · **Stato:** Già applicata, provenienza da verificare
- **Problema:** in ADNIMERGE il metodo di ABETA, TAU, PTAU non è esplicitato.
- **Decisione:** rinominati `AB42_CSF`, `TTAU_CSF`, `PT181_CSF` e considerati Elecsys
  (UPENNBIOMK9).
- **Fonte:** ADNI Biomarker Core; forum ADNI.
- **Da verificare:** i valori ADNI1 coincidono con UPENNBIOMK9? (Q3, solo conteggi aggregati).

### D004 · AGE: baseline o visita
- **Area:** Dati · **Stato:** Superata da D019
- **Problema:** in ADNIMERGE `AGE` è l'età al baseline, non alla visita.
- **Risoluzione:** vedi D019.

### D005 · Test cognitivi: solo punteggi totali
- **Area:** Dati · **Stato:** Già applicata
- **Decisione:** si usano solo i totali o globali (MMSE totale, CDR-SB, ADAS-Cog 13), non gli item.
  Versioni diverse della stessa scala (ADAS-Cog 11 e 13) sono variabili distinte.
- **Rinviato:** la conversione tra scale (es. MoCA → MMSE) richiede altre analisi.

### D006 · Catalogo in JSON con alias qualificati
- **Area:** Struttura · **Stato:** Implementata il 20/10/2026
- **Problema:** catalogo nel codice, alias ambigui tra file, mancano definizioni e codici standard.
- **Decisione:** `catalog.json` come unica fonte di verità, alias `DATASET:FILE.colonna`, nuovi
  campi (definizione, codici standard, `standard_match`, `method_col`, note, `log_ref`).
  Vista tabellare generata, mai modificata a mano.
- **Precisata da:** D017 (alias), D018 (schema).

### D007 · Metodo di misura in colonna separata
- **Area:** Dati · **Stato:** Da implementare
- **Problema:** valori di saggi diversi non sono intercambiabili.
- **Decisione:** il metodo va in una colonna accanto al valore, non nel nome della variabile;
  cut-off indicizzati per (variabile, metodo), già supportato da `config.cutoff(var, method)`.
- **Fonte:** Willemse et al. 2018 (non intercambiabilità Elecsys / Innotest).
- **Precisata da:** D020 (colonna per categoria, non per variabile; ridenominazione in standby).

---

## Decisioni già presenti nel codice (registrate a posteriori)

### D008 · Config = decisioni, pipeline = logica
- **Area:** Struttura · **Stato:** Già applicata
- **Decisione:** liste di colonne, soglie e mappe stanno in `config.py` (o in JSON letti dal
  config); i calcoli in `pipeline.py`. Gli stadi si passano DataFrame in memoria; nessun I/O
  all'import. Sostituisce l'Excel di supporto letto e riscritto a ogni giro.
- **Riferimenti:** `README_config.md`, `NOTE_PER_ROSSANA.md`.

### D009 · Rename per primo, CATALOG per nome standard
- **Area:** Struttura · **Stato:** Già applicata · **Rif. codice:** `[nota Chiara #4]`
- **Decisione:** il rename avviene subito dopo `replace_unknown`, così tutti i passi successivi
  lavorano su nomi standard. La chiave del CATALOG è il nome standard; gli alias i nomi grezzi.

### D010 · RECODE in etichette stringa
- **Area:** Dati · **Stato:** Già applicata · **Rif. codice:** `[nota Chiara #3]`
- **Decisione:** le categoriche si ricodificano in etichette standard leggibili (es. `male`,
  `CN`), non in numeri, così le dummy escono leggibili (`GENDER_male`).
- **Nota:** il codice numerico associato viene conservato nei `levels` del catalogo (D018).

### D011 · Due soglie distinte per i mancanti
- **Area:** Dati · **Stato:** Già applicata
- **Decisione:** `MISSING_KEEP_THRESHOLD` (0,65) etichetta soltanto il report;
  `SPARSE_KEEP_THRESHOLD` (0,65) cancella davvero le colonne. Stesso valore, significati diversi.

### D012 · Nome dei volumi normalizzati
- **Area:** Dati · **Stato:** Già applicata · **Rif. codice:** `[nota Chiara #11]`
- **Decisione:** i volumi divisi per ICV prendono il nome `<vol>%ICV` e sostituiscono l'originale
  in mm3, per non confondere le due unità.

### D013 · Scarto righe senza volumi dopo il merge
- **Area:** Dati · **Stato:** Già applicata · **Rif. codice:** `[nota Chiara #9]`
- **Decisione:** non si scartano righe per volumi mancanti nel singolo file (si perderebbero
  altri dati); dopo il merge si scarta solo la riga senza alcun segnale (`drop_rows_no_signal`).

### D023 · Colonne obbligatorie (any-none)
- **Area:** Dati · **Stato:** Già applicata · **Rif. codice:** `[nota Chiara #1]`
- **Decisione:** `required_all_present` scarta la riga se manca anche **una sola** delle colonne
  indicate (es. ID o data). È diverso da `essential_columns`, che scarta solo se mancano **tutte**.

### D024 · Report esteso
- **Area:** Dati · **Stato:** Già applicata · **Rif. codice:** `[nota Chiara #5]`
- **Decisione:** `profile()` riporta, per ogni variabile, anche il numero di soggetti con quel
  valore e la media di visite valorizzate per soggetto; si genera dopo cleaning 1 e dopo cleaning 2.

### D025 · Collasso delle visite outer
- **Area:** Dati · **Stato:** Già applicata · **Rif. codice:** `[note Chiara #7/#10]`
- **Decisione:** nel merge per categoria le righe dello stesso soggetto entro `buffer_days` sono la
  stessa visita e si fondono (primo valore non nullo); nessuna riga viene persa. Il log separa
  match esatti e match entro buffer, con la distanza media.
- **Nota:** la strategia di merge è ancora in revisione (`notes_CP.md` §D.9).

---

## Decisioni della sessione 16–20/10/2026

### D014 · Registro decisioni
- **Area:** Struttura · **Stato:** Implementata
- **Decisione:** questo file. Le decisioni chiuse vanno qui, le questioni aperte in `notes_CP.md`.
  A fine sessione Claude aggiunge le voci nuove e le mostra a Chiara (regola in `CLAUDE.md` §8).
- **Alternative scartate:** registro in JSON (meno leggibile; lo scopo è la lettura umana).

### D015 · Log di esecuzione automatico
- **Area:** Struttura · **Stato:** Implementata il 20/10/2026
- **Problema:** oggi `run_cleaning1` non registra quante righe toglie ciascun filtro, il log di
  `run_cleaning2` viene scartato da `run_all`, e collisioni o valori non ricodificati finiscono
  solo a schermo o in silenzio.
- **Decisione:** `run_cleaning1` restituisce `(df, log)` come `run_cleaning2`; ogni passo registra
  righe prima/dopo, colonne aggiunte/rimosse e dettagli; `run_all` salva `<FILE>_runlog.json`
  (con data e commit git). I log contengono RID: restano locali, esclusi da git.
- **Distinto da:** questo registro (perché si fa) vs run log (cosa è successo in un'esecuzione).
- **Implementazione:** helper `_log_step` / `_log_skip` in `pipeline.py`; `plan_rename` e
  `unmapped_values` forniscono al log la mappa di rename e i valori non ricodificati, senza
  cambiare il contratto di `rename_variables` e `recode`. `run_cleaning` restituisce
  `(df, {"cleaning1", "cleaning2"})`. Nuovo campo `DatasetConfig.runlog_file`. Anche la stampa
  «colonne richieste ma assenti» di `keep_only_columns`, prima persa, ora compare a schermo.
- **Impatto misurato (ADNIMERGE):** output identico a prima (11.458 × 118 dopo cleaning 1,
  11.458 × 41 dopo cleaning 2). Dal log: il filtro su `DX` toglie 4.963 righe
  (16.421 → 11.458); soggetti 2.430 → 2.409; 197 valori-sentinella convertiti in NaN; nessun
  valore non ricodificato; `drop_sparse_columns` toglie 46 colonne, tra cui MOCA e FLDSTRENG,
  richieste in `keep_columns`.
- **Corretto di passaggio:** `count_bridges.py` usava il risultato di `run_cleaning` come
  DataFrame, ma la funzione restituiva già una tupla.

### D016 · Drop dichiarato prima del rename
- **Area:** Dati · **Stato:** Implementata il 20/10/2026
- **Problema:** rinominare su un nome già occupato (es. VISCODE2 → VISCODE quando VISCODE esiste).
- **Decisione:** nuovo campo `DatasetConfig.drop_columns` (nomi grezzi; nome scelto dalla
  collega nel branch Assignment_analysis_fr): le colonne che darebbero fastidio si eliminano
  subito dopo il caricamento, prima del rename, in modo dichiarato e registrato nel log.
  Se resta comunque una collisione, il rename è saltato con **warning** e voce nel log.
- **Nota:** Chiara valuta di usare `drop_columns` anche in altri momenti (notes_CP B.2).
- **Alternative scartate:** priorità tra alias (vince il primo presente); spostare la colonna
  esistente su un altro nome.

### D017 · Sintassi e precedenza degli alias
- **Area:** Struttura · **Stato:** Implementata il 20/10/2026
- **Decisione:** alias nella forma `DATASET:FILE.colonna`, dove `FILE` = `file_code` del
  `DatasetConfig` oppure `*` (tutti i file del dataset). Precedenza, vince il più specifico:
  1. `ADNI:ADNIMERGE.PTGENDER` → 2. `ADNI:*.PTGENDER` → 3. `*:*.PTGENDER` (o il nome nudo).
  Stesso alias allo stesso livello per due concetti → errore all'import; a livelli diversi
  vince il più specifico, con un messaggio informativo.
- **Conseguenza:** `CATEGORY_RENAME` e `DatasetConfig.rename` vengono migrati in alias
  qualificati e poi rimossi (unica fonte di verità).

### D018 · Schema di `catalog.json`
- **Area:** Struttura · **Stato:** Implementata il 20/10/2026
- **Decisione:**
  - chiave = nome standard; campi `domain`, `definition`, `unit` (UCUM), `role`, `aliases`,
    `derived` (`{"from": [...], "by": "<funzione>"}`), `levels`, `method_col`,
    `omop_concept_id`, `vocab_code`, `admapper_ref`, `standard_match`, `note`, `log_ref`;
  - una voce ha `aliases`, `derived` o entrambi (vedi D019); nessuno dei due → errore;
  - `levels` = etichetta standard → codice **intero**, con la convenzione attuale del notebook
    (es. GENDER female=0, male=1; DX CN=0, MCI=1, Dementia=2; RACE White=5 … More than one=0).
    Le varianti dei singoli file restano in `RECODE`, indicizzato per sorgente;
  - famiglie generate da regole (dummy `<VAR>_<livello>`, `<vol>%ICV`) senza una voce per colonna;
  - template per variabile estratta e calcolata sotto la chiave `_templates`, ignorata dal loader;
  - codici standard inseriti solo dopo verifica su Athena / LOINC / AD-Mapper;
  - export tabellare e dizionario dati dei file puliti in uno script separato
    (`export_catalog.py`), solo per consultazione.

### D019 · AGE: alias + derivata
- **Area:** Dati · **Stato:** Implementata il 20/10/2026 · **Supera:** D004
- **Decisione:**
  - `ADNI:ADNIMERGE.AGE` è alias di `AGE_bl` (età al baseline); `AGE` (età alla visita) ha sia
    alias, per i file che la riportano già, sia `derived` (da `AGE_bl`, `EXAMDATE`, `EXAMDATE_bl`);
  - **il valore misurato vince**: se `AGE` arriva dal file non si ricalcola; si calcola solo se
    manca e gli input ci sono. Il log registra la provenienza;
  - il flag `DatasetConfig.recompute_age` viene rimosso;
  - controllo di coerenza: se `AGE` viene dal file e gli input ci sono, si confronta con il
    valore calcolato; differenze oltre **±0,5 anni** (`POLICY.DERIVED_CHECK_TOLERANCE`) → warning
    e log;
  - log di non calcolabilità: a livello di file (colonne di input assenti) e di soggetto
    (righe con input mancanti, con elenco dei RID solo nel run log locale).
- **Attenzione:** se un file riporta l'età in anni interi troncati, differenze fino a 1 anno sono
  normali; si valuterà dal primo log.

### D020 · Colonna metodo per categoria
- **Area:** Dati · **Stato:** Rinviata (20/10/2026)
- **Aggiornamento 20/10/2026:** la proposta qui sotto è in standby. Per ora resta lo stato
  attuale: colonne `METHOD_CSF`, `METHOD_PLASMA`, …, intese come **informazione di riga**
  sul metodo con cui sono misurate certe variabili. Non sono colonne costanti: dopo l'unione di
  più file possono contenere valori diversi riga per riga (che oggi, nel singolo file, vengano
  riempite con `constant_columns` è solo il modo di popolarle). `FSVERSION` non si modifica.
  Si riprende insieme alla revisione del merge.
- **Problema:** il documento proponeva una colonna metodo per ogni variabile; nella pratica il
  metodo dipende dal tipo di prelievo o di acquisizione, non dal singolo biomarcatore.
- **Proposta (in standby):** una colonna per categoria con nome uniforme `<CAT>_METHOD` (`CSF_METHOD`,
  `PLASMA_METHOD`, `PET_METHOD`, `MRI_METHOD`), che sostituisce `METHOD_CSF` / `METHOD_PLASMA`.
  Valore costante per file, oppure derivato da una colonna se il file mescola più metodi
  (es. `MRI_METHOD = "FreeSurfer_<FSVERSION>"` in ADNIMERGE). Formato `<strumento>_<versione>`.
  `FLDSTRENG` resta separato (acquisizione, non elaborazione). Nel catalogo `method_col` del
  biomarcatore punta alla colonna della sua categoria.
- **Rinviato:** come trattare metodi diversi nella stessa riga dopo il merge (revisione del
  merge, `notes_CP.md` §D.9).

### D021 · Armonizzazione fuori perimetro
- **Area:** Struttura · **Stato:** Rinviata
- **Decisione:** per ora si lavora solo sulla pulizia. Strategie di armonizzazione (conversione,
  z-score, dicotomizzazione con cut-off per saggio) e campioni-ponte si affrontano più avanti.

### D022 · Nessun livello di riferimento per le dummy
- **Area:** Dati · **Stato:** Già applicata (`make_dummies` tiene tutte le classi)
- **Decisione:** non si definisce per ora un `reference_level`: le dummy si generano per tutte le
  classi. Serve solo se un modello di regressione lo richiede (dummy trap); in quel caso si
  aggiunge il campo al catalogo con una nuova decisione.

---

## Decisioni della sessione 20/10/2026 (passo 3)

### D026 · Dummy dopo il merge
- **Area:** Dati · **Stato:** Implementata
- **Problema:** con le dummy create prima del merge, controllare che due file diano lo stesso valore
  per lo stesso soggetto e la stessa visita è difficile (bisogna verificare un solo 1 su più colonne).
- **Decisione:** prima del merge le categoriche restano una colonna sola, in stringa leggibile.
  Le dummy si creano dopo il merge, dalle stringhe (nomi leggibili, es. `GENDER_male`).
  `make_dummies=False` in ADNIMERGE e PTDEMOG; la funzione resta per lo stadio post-merge.
  Le categoriche sono state aggiunte a `keep_columns` di ADNIMERGE.
- **Da valutare allo stadio post-merge:** one-hot per le nominali (RACE, MARRY), una colonna 0/1 per
  GENDER, eventualmente codice ordinale per DX (CN < MCI < Dementia).
- **Impatto misurato (ADNIMERGE):** cleaning 2 da 41 a 29 colonne (−17 dummy, +5 categoriche).

### D027 · Codici di mancante per file
- **Area:** Dati · **Stato:** Implementata
- **Problema:** −4 (e −1) erano trattati come "mancante" in tutte le colonne di tutti i file. In
  ADNIMERGE però compaiono solo in RAVLT_learning e RAVLT_forgetting (e `_bl`), dove sono differenze
  di punteggio vere: la distribuzione è continua (−5: 6, −4: 10, −3: 19, −2: 51, −1: 201). In
  PTDEMOG invece sono codici (es. −4 in PTGENDER, che vale solo 1/2).
- **Decisione:** `MISSING_STRINGS` (testi) valgono sempre; i codici numerici si dichiarano per file in
  `DatasetConfig.missing_codes` (`None` → `DEFAULT_MISSING_CODES`, il comportamento di prima).
  ADNIMERGE: nessuno. PTDEMOG: −4, −1, 9999 (−1 compare solo in PTEDUCAT e PTADBEG).
- **Alternative scartate:** −1 globale (proposto nel branch della collega): avrebbe cancellato circa
  750 valori RAVLT validi in ADNIMERGE.
- **Fonte:** analisi delle distribuzioni sui dati; il significato ufficiale dei codici va verificato
  sul dizionario dati ADNI.
- **Impatto misurato (ADNIMERGE):** recuperati 26 valori RAVLT in cleaning 1 (29 nel file grezzo; 3
  cadono in righe scartate dal filtro su DX). Nessun valore perso.

### D028 · Scarto delle righe per valore (screen fail)
- **Area:** Dati · **Stato:** Implementata
- **Decisione:** `DatasetConfig.drop_rows` = `{colonna standard: [valori]}`, applicato dopo il rename.
  PTDEMOG: `{"VISCODE": ["f"]}` (screen fail). Idea della collega, riscritta perché la sua versione
  andava in errore (campo `viscode_column` inesistente, confronto con una lista).
- **Impatto misurato (PTDEMOG):** −564 righe, −564 soggetti (gli screen fail hanno solo quella riga).

### D029 · Date note solo come mese/anno
- **Area:** Dati · **Stato:** Implementata
- **Problema:** PTDOB è `MM/YYYY`; pandas mette il giorno 1, quindi l'età risulta sempre sovrastimata
  (in media di circa mezzo mese).
- **Decisione:** `POLICY.DOB_IMPUTED_DAY = 15`, applicato **solo** alle colonne in
  `DatasetConfig.month_precision_dates` e **solo** ai valori scritti come `MM/YYYY`: le date complete,
  anche nella stessa colonna, e tutte le altre colonne data restano intatte. Errore massimo ±15 giorni,
  centrato. `extra_date_columns` (della collega) aggiunge le date da convertire oltre a `date_column`.
- **Verifica:** EXAMDATE di ADNIMERGE identica a prima; in PTDEMOG EXAMDATE e update_stamp identiche
  al grezzo riga per riga; PTDOB = mese/anno grezzo con giorno 15 in tutte le 5.396 righe.

### D030 · Età da data di nascita, arrotondata
- **Area:** Dati · **Stato:** Implementata (parte di D019)
- **Decisione:** `recompute_age` ha due modi di calcolo: dalla data di nascita (file senza AGE ma con
  PTDOB, caso PTDEMOG, dalla collega) oppure da `AGE_bl` + tempo trascorso (caso ADNIMERGE). Il valore
  **finale** si arrotonda a `POLICY.AGE_ROUND_DECIMALS = 1` (notes_CP B.4). Il log registra il modo.
- **Impatto misurato:** ADNIMERGE, AGE cambia solo per l'arrotondamento (differenza massima 0,05 anni);
  7 righe senza età, come prima. PTDEMOG, età da 50,4 a 104,3 anni (mediana 73,1); 1 riga senza età
  perché manca la data della visita.
- **Resta per D019:** controllo di coerenza ±0,5 anni, log dei soggetti non calcolabili, rimozione
  del flag `recompute_age`.

### D031 · PTDEMOG dal branch della collega
- **Area:** Dati · **Stato:** Implementata
- **Decisione:** configurazione PTDEMOG portata da `Assignment_analysis_fr` e adattata al rename
  anticipato: `drop_columns=["VISCODE"]`, rename per file VISCODE2→VISCODE, VISDATE→EXAMDATE,
  PHASE→COLPROT; essential con nomi standard; PTDOB esclusa dall'output finale (serve solo all'età ed
  è un quasi-identificativo). Mappature RECODE della collega portate **tali e quali**, tradotte in
  etichette testuali; valori multipli di RACE (`1|5`) → mixed (`RECODE_MULTI`, secondo il suo commento).
- **Da verificare:** tutte le mappature sul dizionario dati (notes_CP D.13).
- **Impatto misurato:** 6.149 → 5.396 righe dopo cleaning 1; 17 colonne dopo cleaning 2; nessun valore
  non ricodificato.

### D032 · Campo `scope` nel catalogo
- **Area:** Struttura · **Stato:** Implementata in parte il 20/10/2026
- **Decisione:** ogni voce del catalogo dichiara fin dove vive la variabile: `cleaning` (tolta a fine
  pulizia, es. PTDOB), `merge` (tenuta fino al merge, es. update_stamp, HAS_QC_ERROR), `output`
  (arriva al dataset finale). Anche le variabili ausiliarie entrano nel catalogo: servono come input
  delle derivate e vanno documentate. Riduce le liste `keep_columns` scritte a mano.

---

## Decisioni della sessione 20/10/2026 (passi 4, 5, 6)

### Note di implementazione per D006, D017, D018, D019, D032
- **D006/D018:** il catalogo è `catalog.json` (65 voci, 159 alias), letto e validato da
  `config.catalog()` alla prima richiesta, non all'import. Il loader blocca: campi sconosciuti,
  `scope` non valido, voce senza `aliases` né `derived`, alias malformato, stesso alias per due
  variabili. Template sotto `_templates`. Vista tabellare e dizionario dati dei file puliti con
  `export_catalog.py`. `RECODE` è indicizzato per sorgente (`"*"` + file); `levels` danno la
  corrispondenza etichetta ↔ codice intero (`config.encode` / `config.decode`); `make_dummies`
  crea una colonna per ogni livello. Le definizioni sono **in bozza**, da rivedere.
- **D017:** i 23 `rename` per file e `CATEGORY_RENAME` sono stati migrati in alias qualificati e
  rimossi. Verifica: la mappa di rename effettiva è identica a prima per 32 configurazioni su 33;
  l'unica differenza voluta è ADNIMERGE `AGE → AGE_bl`. Gli alias della categoria pet (nessun file
  pet configurato) sono a livello `ADNI:*`. Dalla migrazione sono emersi due rename del generatore
  clinicamente dubbi, portati tali e quali e da verificare: CDR `CDGLOBAL → CDRSB` (il CDR globale
  0-3 non è il Sum of Boxes 0-18) e APOERES `GENOTYPE → APOE4` (genotipo vs numero di alleli e4).
- **D019:** motore `derive_variables` in `pipeline.py`. AGE ha due modi di calcolo (da PTDOB, da
  AGE_bl); `AB4240_PL` è un rapporto derivato (ex `derived_ratios`). Il misurato vince; controllo
  di coerenza ±0,5 anni per AGE; log per soggetto degli input mancanti. Rimossi i campi
  `recompute_age`, `derived_ratios`, `rename`, `extra_date_columns`, `month_precision_dates`.
  In ADNIMERGE `essential_columns` usa ora `AGE_bl` (stesso filtro di prima).
- **D032:** implementato `scope = cleaning` (colonne tolte a fine cleaning 1: PTDOB, EXAMDATE_bl).
  `scope = merge` (update_stamp, HAS_QC_ERROR) è solo dichiarato: si applicherà con il merge. Le
  liste `keep_columns` restano per ora; le derivate del catalogo sono tenute in automatico.
- **Impatto misurato** (ADNIMERGE, PTDEMOG, plasma ADx/VUMC, plasma Blennow): tutti i valori
  identici a prima del passo 4, stesse righe e stesso ordine delle colonne. Differenze: EXAMDATE_bl
  e PTDOB non sono più in `cleaned_01`; update_stamp è di tipo data (valori identici). Il dizionario
  dati riconduce al catalogo tutte le colonne dei `cleaned_02` di ADNIMERGE, PTDEMOG e ADx/VUMC.

### D033 · Codici standard: solo se verificati
- **Area:** Dati · **Stato:** Implementata in parte
- **Decisione:** un codice entra nel catalogo solo dopo verifica su una fonte ufficiale. Verificati
  il 20/10/2026 sul terminology server HL7 (tx.fhir.org, LOINC 2.82): **MMSE → LOINC 72106-8**
  "Total score [MMSE]" e **MOCA → LOINC 72172-0** "Total score [MoCA]", entrambi attivi,
  `standard_match = exact`. CDRSB: nessun codice LOINC per il Sum of Boxes trovato (72088-8 è la
  scala CDR complessiva, non il SOB) → vuoto. OMOP (Athena) e loinc.org non sono accessibili in modo
  automatico: `omop_concept_id` resta vuoto ovunque.
- **Da fare:** verifica manuale su Athena / loinc.org / AD-Mapper per le altre variabili.

### D034 · Effetti collaterali del catalogo
- **Area:** Dati · **Stato:** Implementata
- **Decisione:** EXAMDATE_bl ha `scope = cleaning` (serve solo a calcolare AGE) ed esce a fine
  cleaning 1; update_stamp ha `dtype = date` e viene convertita in data in tutti i file (utile al
  merge per la scelta del valore più recente). I volumi Entorhinal, Fusiform, MidTemp sono ora nel
  catalogo con unità mm3: se si attiva `normalize_icv`, verranno normalizzati anche loro.

---

## Decisioni del 26/10/2026

### D035 · ICV resta in mm3
- **Area:** Dati · **Stato:** Implementata
- **Problema:** `normalize_volumes_icv` normalizzava anche ICV su se stessa: creava `ICV%ICV`
  (sempre 100, nessuna informazione) ed eliminava la colonna ICV originale.
- **Decisione:** ICV non viene mai normalizzata e resta in mm3, utile come covariata, per altri
  metodi di correzione (es. residui) e per controllare la normalizzazione.
- **Impatto:** nessuno sugli output attuali (`normalize_icv` è spento in tutti i file); quando si
  attiverà, `ICV` resterà nel file pulito e non comparirà `ICV%ICV`.

### D036 · Evoluzioni: dummy e %ICV come voci del catalogo
- **Area:** Struttura · **Stato:** Implementata
- **Problema:** dal catalogo si ricavano i metadati dei file creati (es. elenco dei predittori o
  dei cofattori presenti nel df), ma le dummy e i volumi `%ICV` non avevano una voce: il
  collegamento era solo ricostruito dal nome.
- **Decisione (opzione A):** la variabile madre dichiara il **tipo** di trasformazione nel campo
  `evolution`; le voci figlie le genera il caricamento del catalogo (`generated = true`), con
  dominio, ruolo, scope e `log_ref` ereditati dalla madre, definizione automatica e `derived` che
  punta alla madre. Una voce scritta a mano con lo stesso nome vince su quella generata.
  - `dummy` (GENDER, MARRY, ETHNICITY, RACE, DX): `<VAR>/<livello>` (D037) per ogni livello di `levels`,
    uguali per tutti i file; si creano **dopo il merge** dalle stringhe; sostituiscono la colonna
    madre ma sono **reversibili** (`pipeline.undummy`, che conta e segnala le righe incoerenti:
    nessun 1 o più di un 1). Dove la categoria manca le dummy sono NA, non 0, per poter tornare
    indietro senza perdere l'informazione.
  - `pct_icv` (Ventricles, Hippocampus, WholeBrain, Entorhinal, Fusiform, MidTemp): `<VOL>%ICV`;
    **sostituisce** il volume in mm3, che non si recupera. ICV resta in mm3 (D035).
  - Quali variabili diventano dummy e quali volumi si normalizzano lo dice solo il catalogo:
    rimosso `DatasetConfig.dummy_columns`; `volume_columns()` usa `evolution` invece dell'unità.
  - Funzioni: `config.evolutions(var)` (figlie), `config.parent_of(var)` (madre),
    `config.evolution_vars(tipo)`.
- **Alternative scartate:** una voce scritta a mano per ogni dummy e ogni `%ICV` (più righe,
  ripetizioni); campo `evolution` con la lista dei nomi delle figlie (nomi già determinati da
  una regola, rischio di disallineamento). Da rivedere se in futuro servirà.
- **Impatto:** catalogo da 65 a 88 voci (23 generate); output dei file invariati (dummy e
  normalizzazione sono spente). Chiude la proposta di `notes_CP.md` punto 15.
- **Da completare:** molte madri hanno `role` vuoto (MARRY, ETHNICITY, RACE, DX, quasi tutti i
  volumi): le figlie lo ereditano vuoto, quindi l'elenco dei predittori/cofattori è incompleto
  finché i ruoli non sono compilati.

### D037 · Separatore delle dummy "/"
- **Area:** Struttura · **Stato:** Implementata
- **Problema:** con `_` non si distingue dove finisce il nome della variabile e dove inizia il
  livello, perché molti nomi e livelli contengono già `_` (`MARRY_never_married`).
- **Decisione:** le dummy si chiamano `<VAR>/<livello>` (es. `GENDER/male`, `MARRY/never_married`);
  il separatore è `config.DUMMY_SEP`, usato da catalogo, `make_dummies`, `undummy` ed
  `export_catalog.py`. Supera la forma `<VAR>_<livello>` citata in D010, D018, D026.
- **Da sapere:** alcuni strumenti a valle trattano male "/" nei nomi di colonna (R lo converte in
  ".", le formule statsmodels richiedono `Q("GENDER/male")`); cambiarlo costa una riga.
- **Nota sui nomi:** le dummy si creano dai `levels` del catalogo, che coincidono con i valori
  nelle colonne perché `recode` produce esattamente quelle etichette; un livello assente in un
  file produce comunque la sua colonna (tutta 0), così tutti i file hanno le stesse dummy.

### D038 · Solo `date_precision` per le date; modelli del catalogo separati
- **Area:** Struttura · **Stato:** Implementata
- **Problema:** `dtype` aveva un solo valore possibile (`date`) e serviva solo insieme a
  `date_precision`: due campi per un'informazione. I modelli del catalogo erano annidati
  (`_variabile_calcolata` dentro `_templates`), e una parentesi sbagliata rendeva il file illeggibile.
- **Decisione:** `dtype` eliminato. Una variabile è una data se ha `date_precision`: `day` = data
  completa (EXAMDATE, EXAMDATE_bl, update_stamp), `month` = solo mese/anno (PTDOB); assente = non è
  una data. In cima a `catalog.json`, uno accanto all'altro: `_istruzioni` (generali),
  `_template_variabile_estratta`, `_template_variabile_calcolata`. Ogni chiave dei modelli ha la sua
  spiegazione, che comincia con `OBBLIGATORIO.` o `Facoltativo.`; nessun `null`. I modelli sono le
  prime righe di `catalog_table.csv`.
- **Impatto:** stesse 88 voci, stesse 4 variabili data; output della pipeline identici.

### D039 · Date note solo come anno
- **Area:** Dati · **Stato:** Implementata
- **Decisione:** terzo valore di `date_precision`, `year`, per le date note solo come anno (valori
  `YYYY`, anche letti come numero 1940.0). La data è imputata a metà anno, al 1° luglio
  (`POLICY.YEAR_IMPUTED_MONTH_DAY = (7, 1)`): errore centrato, massimo ±6 mesi, stessa logica del
  giorno 15 per `month` (D029). L'imputazione vale solo per i valori scritti `YYYY`; le date complete
  nella stessa colonna non si toccano. Il run log conta i valori imputati per colonna.
- **Confermato:** niente `dtype` (D038). La prova `"dtype": str` su RID non viene tenuta; restano le
  altre modifiche di Chiara a RID (campi vuoti tolti).
- **Da decidere:** PTADBEG, PTCOGBEG, PTADDX sono anni scritti come numeri; oggi restano numeri
  (anno di calendario). Marcarli `year` li trasformerebbe in date.
- **Impatto:** nessuna variabile del catalogo usa ancora `year`; output invariati.

### D040 · Direzione di peggioramento nel catalogo (`worsening`)
- **Area:** Struttura · **Stato:** Implementata
- **Problema:** per scale cliniche, volumi e biomarcatori serve sapere se un aumento o una
  diminuzione indica un peggioramento. L'informazione c'era solo in `ranges.json` (terzo elemento di
  `[min, max, direzione]`: `increasing` / `inverse`), non usata da nessuna funzione e invisibile nel
  catalogo.
- **Decisione:** campo facoltativo `worsening` nel catalogo, valori `increase` (peggiora se aumenta)
  e `decrease` (peggiora se diminuisce), validato da `config.load_catalog`. Compilato copiando
  `ranges.json` tale e quale (`increasing → increase`, `inverse → decrease`) per scale, volumi e
  biomarcatori. Le figlie %ICV lo ereditano dalla madre, le dummy no. La direzione **resta anche in
  `ranges.json`**; `export_catalog.py` controlla che i due coincidano.
- **APOE4:** solo nella descrizione (più alleli e4 = rischio maggiore), perché non è un parametro
  che cambia nel tempo.
- **Alternative scartate:** lasciarla solo in `ranges.json` (fuori dalla fonte unica delle
  variabili, D006); toglierla da `ranges.json` (si tocca `column_ranges` senza necessità per ora).
- **Da verificare:** `WholeBrain` non compilato (in `ranges.json` c'è `Brain` = increasing ma
  `Brain%ICV` = inverse, contraddittori); `ICV` copiato `decrease` ma è una variabile di
  normalizzazione, non un marcatore; `APS2` non è in `ranges.json`. Vedi `notes_CP.md` punto 17.
- **Impatto:** 31 variabili compilate (17 `increase`, 14 `decrease`) più 5 figlie %ICV;
  nessuna discordanza con `ranges.json`; output della pipeline invariati (solo metadati).

### D042 · Storico dei log di esecuzione
- **Area:** Struttura · **Stato:** Implementata
- **Problema:** `<FILE>_runlog.json` e `<CATEGORIA>_mergelog.json` avevano nome fisso e ogni run
  sovrascriveva il precedente: non si potevano confrontare due esecuzioni (es. prima/dopo una
  modifica al catalogo).
- **Decisione:** `run_all` salva i log in `config.LOG_DIR` (`logs/`) con data e ora nel nome
  (`<nome>_AAAAMMGG-HHMM.json`, funzione `_log_path`); tutti i log dello stesso run hanno lo stesso
  timestamp. Cartella in `.gitignore` (contiene RID). Nessuna cancellazione automatica.
  Nello stesso giro i run log registrano anche `visite_per_soggetto` (distribuzione
  `{n_visite: n_soggetti}`, `_visits_per_subject`) a fine cleaning 1 e cleaning 2 (`notes_CP.md` A.3).
- **Alternative scartate:** nome fisso (nessuno storico); rotazione/pulizia automatica (codice in
  più non necessario oggi).
- **Da tenere presente:** i CSV in uscita restano sovrascritti; la cartella è sincronizzata da
  OneDrive come i CSV, quindi le copie di file con RID aumentano.
- **Impatto:** dati in uscita invariati; cambia solo dove e con che nome si salvano i log.

### D043 · `evolution` vs `derived`: rapporti e APOE4
- **Area:** Struttura · **Stato:** Implementata
- **Problema:** nel catalogo alcune madri dichiaravano `evolution: ["ratios"]` (CSF/plasma) o
  `["APOE4"]` (APOE), valori non supportati: il validatore bloccava il run.
- **Decisione:** `evolution` resta riservata alle trasformazioni meccaniche con figlie generate dal
  loader (`dummy`, `pct_icv`, D036). Le variabili calcolate con significato proprio (rapporti,
  APOE4) sono voci vere del catalogo con `derived` sulla figlia; per i rapporti serve anche la riga
  in `config.RATIOS`. Rimossi `ratios`/`APOE4` da `evolution`. Corretto `AB4240_CSF` (`derived`
  puntava ad AB42_PL/AB40_PL invece che ai valori CSF) e aggiunto `AB4240_CSF` a `config.RATIOS`.
  APOE4 si ricava dal genotipo APOE, non il contrario.
- **Alternative scartate:** nuova evoluzione `ratios` (un rapporto ha due madri e una definizione
  propria, non è una trasformazione meccanica).
- **Da decidere (Chiara):** alias di APOE e APOE4 (oggi `APOERES.GENOTYPE` è su APOE4); passo di
  calcolo di APOE4 dal genotipo (oggi `"by": "to be completed"`).
- **Impatto:** il rapporto AB42/AB40 nel liquor viene ora calcolato nei file CSF che hanno AB42 e
  AB40 ma non il rapporto misurato (colonna in più dove prima mancava). Conteggi da verificare al
  primo run con il catalogo valido.

### D044 · Lista bianca iniziale di colonne grezze (`load_columns`)
- **Area:** Struttura · **Stato:** Implementata per ADNIMERGE e PTDEMOG
- **Problema:** ADNIMERGE ha 116 colonne (50 `*_bl`) e la pipeline le trascinava tutte fino a
  `keep_columns` in cleaning 2; la selezione delle colonne era divisa tra `drop_columns` (grezze,
  inizio), `scope` (catalogo) e `keep_columns` (standard, fine). `notes_CP.md` B.2.
- **Decisione:** nuovo campo `DatasetConfig.load_columns` con **nomi grezzi** (si incollano da
  `df.columns`); subito dopo il load si tengono solo quelle (riusa `keep_only_columns`), passo
  registrato nel log. Avvisi: colonne elencate ma assenti dal file; colonne caricate senza voce nel
  catalogo (restano col nome grezzo). Per tutti i file, nuovo avviso se una colonna dei filtri di
  riga (`required_all_present`, `essential_columns`, `also_required`) manca dopo il rename: i filtri
  la ignoravano in silenzio, allargandosi. In ADNIMERGE e PTDEMOG `keep_columns` e `drop_columns`
  sono commentate (non rimosse); le colonne escluse restano scritte come commento.
- **Alternative scartate:** lista nera estesa con `drop_columns` (lunga; le colonne nuove di una
  release passano inosservate); lista bianca dal catalogo (un alias `ADNI:*` caricherebbe la
  variabile da ogni file, senza scelta per file; obbliga a compilare il catalogo prima di lavorare).
- **Eccezione a §4.2:** come `drop_columns` (D016), usa nomi grezzi perché agisce prima del rename.
- **Da decidere (Chiara):** gruppi di ADNIMERGE lasciati commentati (PET, CSF, Ecog, altre scale,
  WholeBrain); rimozione definitiva di `keep_columns`/`drop_columns` dopo aver scritto
  `load_columns` per gli altri 31 file.
- **Impatto:** ADNIMERGE 117 → 31 colonne a fine cleaning 1, PTDEMOG 84 → 17; output di cleaning 2
  **identico** al precedente (stesse righe 11.458 / 5.396, soggetti 2.409 / 4.292, colonne e valori).
  Alias di APOE impostato a `ADNI:*.APOE` (D043): catalogo di nuovo valido.

### D045 · Filtri di riga come lista di gruppi (`row_filters`) e `dedup_columns`
- **Area:** Struttura · **Stato:** Implementata
- **Problema:** tre campi con nomi simili e logiche diverse (`required_all_present` = scarta se ne
  manca una; `essential_columns` e `also_required` = scarta se mancano tutte), facili da confondere.
  `essential_columns` serviva anche a `dedup_visits` per scegliere il duplicato più completo.
  `notes_CP.md` B.3.
- **Decisione:** un solo campo `row_filters`, lista di gruppi: per ogni gruppo la riga si scarta se
  mancano **tutti** i valori (`drop_if_all_none`, un passo di log per gruppo). Un gruppo di una
  colonna equivale a una colonna obbligatoria, quindi copre anche `required_all_present`. Nuovo
  campo `dedup_columns` per la scelta tra visite duplicate, tenuto separato perché è più delicato:
  servono variabili di visita, non del soggetto. Rimossi i tre campi e `drop_required` (non più
  usata). Conversione a comportamento identico: `dedup_columns` = vecchia `essential_columns`.
- **Alternative scartate:** usare la lista di `load_columns` anche per i duplicati (contiene
  variabili del soggetto e amministrative, che non distinguono le righe).
- **Da decidere (Chiara):** in ADNIMERGE il gruppo `APOE4, MMSE, Ventricles, Hippocampus, AGE_bl`
  scarta 0 righe, perché APOE4 e AGE_bl sono costanti del soggetto e presenti su ogni riga; lo
  stesso vale per `dedup_columns`. Proposta: solo misure di visita. Eventuale gruppo temporale
  `["VISCODE", "EXAMDATE"]`.
- **Impatto:** output identico (ADNIMERGE 11.458 righe / 2.409 soggetti; PTDEMOG 5.396 / 4.292).
  Righe rimosse per gruppo: ADNIMERGE RID 0, essenziali 0, DX 4.963; PTDEMOG anagrafiche 18, PTDOB 171.
