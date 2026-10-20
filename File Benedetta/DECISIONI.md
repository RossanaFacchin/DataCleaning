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
| D006 | 15/10/2026 | Struttura | Catalogo in JSON, alias qualificati, nuovi campi | Da implementare (precisata da D017, D018) |
| D007 | 15/10/2026 | Dati | Metodo di misura in colonna separata | Da implementare (precisata da D020) |
| D008 | 31/08/2026* | Struttura | Config = decisioni, pipeline = logica; niente round-trip su CSV | Già applicata |
| D009 | 31/08/2026* | Struttura | Rename per primo, CATALOG indicizzato per nome standard | Già applicata |
| D010 | 31/08/2026* | Dati | RECODE in etichette stringa standard, non numeri | Già applicata |
| D011 | 31/08/2026* | Dati | Soglia del report e soglia di cancellazione separate | Già applicata |
| D012 | 31/08/2026* | Dati | Volumi normalizzati rinominati `<vol>%ICV` | Già applicata |
| D013 | 31/08/2026* | Dati | Scarto righe senza volumi spostato dopo il merge | Già applicata |
| D014 | 19/10/2026 | Struttura | Registro decisioni in `DECISIONI.md`, aggiornato da Claude | Implementata |
| D015 | 19/10/2026 | Struttura | Log di esecuzione automatico per ogni file | Implementata (20/10/2026) |
| D016 | 19/10/2026 | Dati | Drop dichiarato prima del rename, niente priorità tra alias | Da implementare |
| D017 | 19/10/2026 | Struttura | Sintassi e precedenza degli alias `DATASET:FILE.colonna` | Da implementare |
| D018 | 19/10/2026 | Struttura | Schema di `catalog.json`: estratte, derivate, levels, template | Da implementare |
| D019 | 20/10/2026 | Dati | AGE: alias + derivata, il misurato vince, controlli e log | Da implementare |
| D020 | 19/10/2026 | Dati | Colonna metodo per categoria `<CAT>_METHOD` | Da implementare |
| D021 | 19/10/2026 | Struttura | Armonizzazione fuori perimetro: ora solo pulizia | Rinviata |
| D022 | 19/10/2026 | Dati | Nessun livello di riferimento per le dummy (per ora) | Già applicata |
| D023 | 31/08/2026* | Dati | Scarto riga se manca anche una sola colonna obbligatoria (ID, data) | Già applicata |
| D024 | 31/08/2026* | Dati | Report `profile()` con soggetti e visite, anche dopo cleaning 2 | Già applicata |
| D025 | 31/08/2026* | Dati | Collasso delle visite outer, nessuna riga persa nel merge | Già applicata |

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
- **Area:** Struttura · **Stato:** Da implementare
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
- **Precisata da:** D020 (colonna per categoria, non per variabile).

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
- **Area:** Dati · **Stato:** Da implementare
- **Problema:** rinominare su un nome già occupato (es. VISCODE2 → VISCODE quando VISCODE esiste).
- **Decisione:** nuovo campo `DatasetConfig.drop_before_rename` (nomi grezzi): le colonne che
  darebbero fastidio si eliminano prima del rename, in modo dichiarato e registrato nel log.
  Se resta comunque una collisione, il rename è saltato con **warning** e voce nel log.
- **Alternative scartate:** priorità tra alias (vince il primo presente); spostare la colonna
  esistente su un altro nome.

### D017 · Sintassi e precedenza degli alias
- **Area:** Struttura · **Stato:** Da implementare
- **Decisione:** alias nella forma `DATASET:FILE.colonna`, dove `FILE` = `file_code` del
  `DatasetConfig` oppure `*` (tutti i file del dataset). Precedenza, vince il più specifico:
  1. `ADNI:ADNIMERGE.PTGENDER` → 2. `ADNI:*.PTGENDER` → 3. `*:*.PTGENDER` (o il nome nudo).
  Stesso alias allo stesso livello per due concetti → errore all'import; a livelli diversi
  vince il più specifico, con un messaggio informativo.
- **Conseguenza:** `CATEGORY_RENAME` e `DatasetConfig.rename` vengono migrati in alias
  qualificati e poi rimossi (unica fonte di verità).

### D018 · Schema di `catalog.json`
- **Area:** Struttura · **Stato:** Da implementare
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
- **Area:** Dati · **Stato:** Da implementare · **Supera:** D004
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
- **Area:** Dati · **Stato:** Da implementare (solo parte di pulizia)
- **Problema:** il documento proponeva una colonna metodo per ogni variabile; nella pratica il
  metodo dipende dal tipo di prelievo o di acquisizione, non dal singolo biomarcatore.
- **Decisione:** una colonna per categoria con nome uniforme `<CAT>_METHOD` (`CSF_METHOD`,
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
