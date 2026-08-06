# Note sulla riscrittura di `pipeline.py` — cosa correggere e perché

Ciao Rossana,
hai fatto la parte più grossa: riprodurre il comportamento della "base" (il cleaning
completo di Chiara) dentro la pipeline nuova. Qui sotto trovi, in ordine di
importanza, cosa non va e come l'ho sistemato nei file allegati (`config.py`, `pipeline.py`
corretti). 

Il principio unico da tenere a mente è quello del README: **`config.py` = decisioni e
dati; `pipeline.py` = logica, composta in memoria, senza toccare il disco se non
all'ingresso e all'uscita.** Quasi tutti gli errori sotto sono una violazione di questa
riga.

---

## 1. Bug bloccanti: il file Python non gira 

### 1a. Hai mutato `ADNIMERGE.source` — cleaning1 non trova più il suo input

In cima al file avevi aggiunto:

```python
ADNIMERGE.source = "ADNIMERGE_cleaned_01.csv"
```

Così però `run_cleaning1()` (che legge `cfg.source`) non legge più il file **grezzo**:
prova a leggere il proprio **output**, che alla prima esecuzione non esiste ancora.
Eseguendo `python3 pipeline.py` su una cartella pulita si ottiene:

```
FileNotFoundError: [Errno 2] No such file or directory: 'ADNIMERGE_cleaned_01.csv'
```

`source` è una **decisione** e sta nel `config`: per cleaning1 dev'essere sempre il file
raw. Il nome dell'output è un'altra decisione, che ho messo nel `config` come campo
separato (`output_cleaned1`, `output_cleaned2`), senza sovrascrivere l'input.

### 1b. Codice eseguibile a livello di modulo — il semplice `import` fa I/O e crasha

Dal blocco `if __name__ == "__main__":` in giù hai messo statement eseguibili "nudi"
(non dentro funzioni):

```python
df_raw = pd.read_csv(ADNIMERGE.source)
df_cleaned, dropped_columns = remove_param_few_subjects(df_raw)
...
save_dataset(df_cleaned, OUTPUT_FILE)
```

Questi girano **all'import**. Ma il docstring del file promette proprio
`from pipeline import run_cleaning1, profile`: e infatti quell'import da solo crasha,
perché esegue le letture/scritture qui sopra. Un modulo non deve avere effetti
collaterali all'import: chi lo importa vuole le funzioni, non far partire una pipeline.

Correzione: tutto ciò che tocca il disco vive **solo** dentro `run_cleaning2()` (in
memoria) e nel blocco `__main__`. Importare il modulo ora non legge e non scrive niente.

---

## 2. Il pattern read → write → read tra un passo e l'altro

Ogni tuo step salva su CSV e il successivo **rilegge lo stesso CSV**:

```python
save_dataset(df_cleaned, OUTPUT_FILE)
df_step2 = pd.read_csv(DUMMY_INPUT)      # rilegge cio' che ha appena scritto
...
df_step3 = pd.read_csv(OUTPUT_FILE)      # e di nuovo
```

È di nuovo l'anti-pattern dell'Excel: passi di dati che si scambiano informazione
attraverso un file condiviso, sovrascritto in place più volte. Conseguenze: l'ordine
conta, i tipi si perdono a ogni round-trip (è il motivo per cui poi ti serviva
`realign_column_types`), e basta un'esecuzione a metà per lasciare il file in uno stato
incoerente.

Correzione: `run_cleaning1` restituisce un DataFrame, `run_cleaning2` lo **riceve in
memoria** e lo passa di funzione in funzione. Si scrive su disco una volta sola alla
fine di ciascuno stadio. (Effetto collaterale gradito: `realign_column_types` non serve
quasi più, perché senza round-trip su CSV i tipi non si degradano. L'ho reso opzionale
e spento.)

---

## 3. Hai ridefinito `drop_if_all_none` con un contratto diverso

Esiste già la funzione (cleaning1), che restituisce **un DataFrame**:

```python
def drop_if_all_none(df, cols):
    ...
    return df.dropna(subset=present, how="all")
```

Più in basso l'hai ridefinita con lo stesso nome ma restituendo **una tupla**
`(df, dropped_rows)`. In Python vince l'ultima definizione: chi importa il modulo si
ritrova la versione tupla anche dentro `run_cleaning1`, dove `df = drop_if_all_none(...)`
diventa `df = (dataframe, numero)` e tutto il seguito esplode. È un bug latente, che si
manifesta solo da import o cambiando l'ordine: il tipo più insidioso.

Correzione: **una sola** `drop_if_all_none`, riusata sia per le colonne essenziali
(cleaning1) sia per le chiavi-volume (cleaning2). Il conteggio delle righe rimosse lo
calcola l'orchestratore con `len(df)` prima/dopo, così la funzione mantiene un contratto
unico `df -> df`.

---

## 4. Decisioni e dati cablati in `pipeline.py` (vanno nel `config`)

Questo è il punto centrale della tua domanda "cosa spostare nel config". Ecco la mappa di dove le ho spostate:

| Cosa avevi in `pipeline.py` | Cos'è | Dove va ora |
|---|---|---|
| `OUTPUT_FILE = "..._02.csv"` | nome di output (decisione) | `DatasetConfig.output_cleaned2` |
| `REF_LIST = ['GENDER','MARRY',...]` | quali categoriche fare dummy | `DatasetConfig.dummy_columns` |
| `KEY_COLUMNS = ['Ventricles',...]` | chiavi per scartare righe vuote | `DatasetConfig.volume_row_keys` |
| `COLONNE_CHIARA = [...]` | whitelist finale di colonne | `DatasetConfig.keep_columns` |
| `COLONNE_EXTRA_DA_MANTENERE` incl. `MARRY_0.0`, `RACE_5.0`... | nomi dummy scritti a mano | **eliminato**: le dummy le tiene in automatico la pipeline |
| soglia 0.65 riusata per scartare colonne | soglia (dato) | `POLICY.SPARSE_KEEP_THRESHOLD` |
| `COLUMNS = [...]` (lista outlier) | lista per EDA | **fuori**: è roba da script EDA, non da cleaning |

Regola per orientarti: se una cosa è una lista di nomi di colonne o una soglia che *tu
scegli*, è una decisione → `config`. Se è un `for` che *calcola* qualcosa, è logica →
`pipeline`. Davanti a `REF_LIST` o `KEY_COLUMNS` scritte in mezzo al codice, la domanda
"la sto scegliendo io o la sta calcolando il codice?" dà subito la risposta.

Due dettagli su questa tabella:

- **Le dummy scritte a mano (`MARRY_0.0`, `RACE_5.0`…) erano fragili.** Quei suffissi
  con `.0` esistono solo perché la colonna, dopo il recode con `np.nan`, diventa float.
  Basta un cambio di tipo e i nomi non combaciano più. Nella versione nuova
  `make_dummies` fa prima il cast a `Int64`, quindi i suffissi sono interi puliti
  (`MARRY_0`, non `MARRY_0.0`), e la pipeline **tiene automaticamente** tutte le dummy
  generate: non vanno elencate da nessuna parte.

- **`COLONNE_CHIARA` mescolava nomi grezzi e standard.** Contiene `PTGENDER`, `PTEDUCAT`,
  `PTETHCAT`… ma a quel punto della pipeline quelle colonne sono già state rinominate
  (`GENDER`, `EDUCATION`, `ETHNICITY`) e poi trasformate in dummy. Quindi metà della tua
  whitelist non esisteva più al momento del filtro. L'ho riscritta con i **nomi standard
  post-rename**, coerenti con lo stato del dataframe in quel punto.

---

## 5. L'`assert` "di sicurezza" non controlla niente

```python
df_step2 = pd.read_csv(DUMMY_INPUT)        # DUMMY_INPUT e' il file appena salvato
assert df_step2.shape[1] == df_cleaned.shape[1], "..."   # ...contro il df che lo ha scritto
```

Stai rileggendo da disco il file che `df_cleaned` ha appena **scritto** e poi verifichi
che abbia lo stesso numero di colonne di `df_cleaned`. È vero per costruzione: l'assert
passa sempre. Il commento parla di "72 colonne attese", numero che nel codice non
compare. Un controllo che non può fallire dà solo una falsa sensazione di sicurezza.
L'ho rimosso: componendo in memoria non c'è alcun disallineamento da controllare.

---

## 6. Cosa manca (la tua domanda "manca qualcosa?")

Sì, tre cose:

1. **`remove_sub_1visit` non è implementata.** Hai aggiunto al config
   `MULTIVISIT_MIN_SUBJECTS = 10` (giusto: è una soglia, va nel config!) ma poi la logica
   che la usa non c'è: nessuna funzione conta i soggetti con >1 visita né scarta quelli
   con una sola. La costante restava orfana. L'ho implementata
   (`remove_single_visit_subjects`), con l'eccezione per i file anagrafici/genetici
   (PTDEMOG/APOERES) del notebook.

2. **La normalizzazione dei volumi su ICV (cleaning3) non c'è.** Usavi
   `Ventricles/Hippocampus/WholeBrain/ICV` solo per scartare righe vuote, ma il
   `transform_volumes_as_ICV_percent` — volumi come % dell'ICV — mancava del tutto.
   L'ho aggiunto (`normalize_volumes_icv`). Nota: **non** ho aggiunto la somma
   sinistro+destro (`get_volumes_total`), perché in ADNIMERGE i volumi sono già totali a
   colonna singola; serve solo ai file UCSF con emisferi separati.

3. **Il calcolo degli outlier era codice morto.** Calcolavi `outlier_counts` e poi non
   lo usavi da nessuna parte. In più l'analisi outlier è EDA, non cleaning: appartiene
   allo script esplorativo (`README.md`), non alla pipeline che modifica i dati. L'ho
   tolto da qui.

Le prime due le ho **implementate ma lasciate spente** (`remove_single_visit=False`,
`normalize_icv=False`) nel `config`; magari lunedì discutetelo te e Chiara assieme.

---

## 7. Dettagli minori (ma da sapere)

- **Non riusare `MISSING_KEEP_THRESHOLD` per cancellare colonne.** Nel design quella
  soglia serve **solo** al report `profile()` per *etichettare* keep/drop: non cancella
  niente, è consultiva. Tu l'hai usata come soglia di un `drop(columns=...)` vero, cioè
  hai trasformato un'etichetta in un'azione distruttiva. Ho separato le due cose:
  `MISSING_KEEP_THRESHOLD` (report) e `SPARSE_KEEP_THRESHOLD` (azione). Stesso valore
  oggi, 0.65, ma significati diversi — e domani li puoi cambiare in modo indipendente.

- **Tensione MOCA/FLDSTRENG.** Le avevi nella whitelist "da tenere", ma hanno ~45% di
  valori validi, quindi il drop delle colonne sparse (soglia 65%) le elimina prima. La
  pipeline corretta **te lo dice** invece di produrre in silenzio un file senza colonne
  che credevi di aver tenuto — in esecuzione stampa `ATTENZIONE, richieste ma assenti:
  ['MOCA','FLDSTRENG']`. È una decisione tua: alzare la soglia, esentare quelle colonne,
  o accettare di perderle.

- **`categorize_*` → `RECODE` + `recode_columns`.** Bene che tu non abbia reintrodotto le
  vecchie funzioni categoriche; ricorda solo che la mappa va in `config.RECODE` e la
  lista di colonne in `dummy_columns`/`recode_columns`, mai i valori dentro il codice.

---

## In sintesi

Quello che avevi scritto **funziona nella tua testa** come sequenza di celle di
notebook: esegui in ordine, salvi, rileggi. Ma tradotto in un modulo `.py` riporta
dentro tutti i difetti del notebook (stato globale, ordine che conta, I/O all'import,
decisioni sparse nel codice). La riscrittura serviva proprio a togliere quei difetti.

Checklist per il prossimo file che aggiungerai:

- [ ] Nessuna riga eseguibile fuori da una funzione o dal `__main__`.
- [ ] `source` = file grezzo, mai sovrascritto; gli output sono campi del `config`.
- [ ] I passi si passano DataFrame in memoria, non CSV riletti da disco.
- [ ] Nessun nome di funzione ridefinito con un contratto diverso.
- [ ] Liste di colonne e soglie → `config`. `for`/calcoli → `pipeline`.
- [ ] Le dummy e le colonne calcolate si tengono in automatico, non a mano.
- [ ] Ogni soglia ha un solo significato (report ≠ azione distruttiva).

Se qualcosa non ti torna, ne parliamo :)
--> SE VUOI PROVARE: prova a lanciarlo e verificare che la pulizia abbia avuto senso (guarda le shape delle matrici, e se lievita in dimensione, le colonne se sono state aggiunte correctly etc)

## Aggiornamento — cosa è stato aggiunto dopo (armonizzazione, merge, JSON)

Da quando hai scritto la tua versione il framework è cresciuto, sempre con la stessa regola (decisioni nel config, logica nel pipeline). Ti serve conoscere queste cose perché toccano i file che aggiungerai.

Aggiungere un file = solo config, anche per plasma/CSF/PET. Sono stati aggiunti al DatasetConfig alcuni campi generici (category, rename per-file, constant_columns, derived_ratios, atn_axes) e poche funzioni scritte una volta. Da lì un file nuovo si descrive senza toccare la logica. Il dettaglio operativo, con un esempio CSF completo, è nella sezione §9 del README (README_armonizzazione_merge.md) — leggila prima di aggiungere un file di una categoria nuova.

L'armonizzazione è una riga, non una funzione. Il metodo/assay con cui è misurato un biomarcatore non è una colonna del file: è il file stesso. Quindi lo si assegna come costante (constant_columns={"METHOD_CSF": "elecsys"}), e due file che misurano la stessa cosa con strumenti diversi si portano allo stesso nome standard via rename. Diventano la stessa variabile ma restano distinguibili dal metodo. Non mescolare mai a mano misure di assay diversi: non sono numericamente intercambiabili.

I quattro JSON di supporto: dove vanno. Questo è il punto su cui è facile sbagliare, quindi tienilo a mente. Ci sono due categorie, e fanno lavori diversi:

- cutoffs.json — soglie del profilo ATN. Trasforma i dati (calcola ATN_PROFILE), quindi è roba di cleaning. Lo legge config.cutoff(); serve solo ai file con compute_atn=True. Se manca e un file lo richiede, il codice si ferma con un errore chiaro (non produce dati muti).
- ranges.json — range di validità [min, max, direzione] per colonna, in tre sezioni (normalization, volume, cofattori). Non trasforma niente: serve ad arricchire i metadati nello stadio di merge (è ciò che nel vecchio automated_merge.py facevano i filter_*). Lo legge config.load_settings(sezione) / config.column_ranges(...).

Due cose da non fare con questi JSON, che sono la versione "dati" dello stesso errore di prima (dato mischiato a logica):

Non incollarli come dict dentro config.py. Sono dati tabulari clinici (la traduzione del vecchio Excel di supporto): restano file, letti dal config. Metterli nel .py rimette l'Excel dentro il codice.
Non ricopiare i range dentro il pipeline "per comodità": si leggono da ranges.json con column_ranges, in un posto solo.

I tre file separati di prima (normalization_settings.json, volume_values_settings.json, cofattori_values_settings.json) sono stati accorpati in un unico ranges.json a tre sezioni: stessi valori, un file solo. cutoffs.json resta separato apposta — fa un lavoro diverso (una soglia che guida un calcolo, non un range che descrive).

--> Aggiunte alla checklist:

 File nuovo → nuovo DatasetConfig (+ rename per-file), mai una funzione nuova, salvo vera eccezione isolata.
 I JSON di dati restano file letti dal config; nel .py non ci finiscono valori clinici a mano.
 cutoffs.json = cleaning (trasforma); ranges.json = merge (metadati). Non confonderli.


### EXTRA per Chiara: nuovo dataset OASIS (altra banca dati che era di interesse, diversa origine)

Valuta di capire come integrare nuovi dati da source diversa (OASIS era su Kaggle, a saperlo...)

https://www.kaggle.com/code/hyunseokc/detecting-early-alzheimer-s/input

### Appunti Chiara
#### 1. def drop_if_all_none(df, cols): 
(riga 79 di pipeline) nelle note sopra indica che sostituisce la chiamata di 1 funzione chiamata sia per essential che per richieste. --> [essential + also_required]
Da capire bene se unisce due liste o le tratta diversamente. Infatti io potrei dire che se manca tipo l'ID mi deve cancellare la riga, e se non c'è nessun valore tra 5 colonne allora eliminare. se vengono unite ID e lista delle 5 variabili non si ha lo stesso effetto... Se vengono chiamati in momenti separati si ottiene il risultato corretto.

#### 2. def recompute_age(df, date_col="EXAMDATE", bl_date_col="EXAMDATE_bl", age_col="AGE"):
riga 122 --> viene rinominata AGE in AGE_bl ma se rinominiamo/standardizziamo prima i dati allora possiamo mettere dirrettamente come label AGE_bl. Non so se ha già senso inserire anche le altre cose che sappiamo possono esseci o lasciamo così per ora e aggiornimo metodi per il calcolo dell'età man mano che troviamo i file.

#### 3. def recode(df, cols):
riga 130 --> valutare di mappare non numericamente ma con stringhe standard poi utili per dummies per non ritrasformarle in numeri.

#### 4. CATALOG r def rename
sia in config che in pipeline
Problema attuale

CATALOG è indicizzato per nome grezzo (PTGENDER, NF_LIGHT...), non per concetto. Se la stessa variabile concettuale (es. "genere") appare con nomi diversi tra file (PTGENDER, SEX, Gender...), oggi l'unico modo per gestirlo è:

aggiungere ogni sinonimo come voce separata in CATALOG (duplica parameter/unit/role più volte), oppure
aggiungerlo nel self.rename del singolo DatasetConfig (ma allora quel sinonimo non eredita gli attributi di CATALOG — solo il nome standard).
In entrambi i casi il nome standard ("GENDER") resta una stringa scritta a mano in più punti → rischio di typo silenziosi.

Strategia proposta: invertire la chiave di CATALOG

Indicizzare CATALOG per nome standard invece che per nome grezzo, e aggiungere alla Var una lista di sinonimi noti:


CATALOG = {
    "GENDER": Var(parameter="Demographic", aliases=["PTGENDER", "SEX", "Gender"]),
    "AGE":    Var(parameter="Demographic", unit="years", aliases=["AGE"]),
    ...
}
Da qui si genera automaticamente la mappa inversa (grezzo → standard) usata per il rename:


def rename_map():
    return {alias: std for std, v in CATALOG.items() for alias in v.aliases}
Vantaggi:

Un solo punto dove aggiungere un nuovo sinonimo quando lo si scopre in un nuovo file (basta appendere alla lista aliases), senza toccare parameter/unit/role.
Il nome standard è scritto una sola volta (come chiave del dizionario) → niente più rischio di typo sparsi tra file diversi.
Si può validare a "import time" che nessun alias sia condiviso per errore da due variabili standard diverse (basta un controllo che segnali duplicati in fase di costruzione della reverse map).
Cosa resta invariato: self.rename per-file continua a esistere per i casi eccezionali già visti (stesso nome grezzo che significa cose diverse a seconda del file, o override intenzionali) — resta il meccanismo di "ultima parola" che vince sui conflitti, ma sarebbe usato solo per le vere eccezioni, non per i sinonimi comuni ormai gestiti da aliases.

Trade-off da considerare: richiede di riscrivere CATALOG esistente (migrazione una tantum) e serve decidere cosa succede se due file usano lo stesso alias con significati diversi — da gestire con un controllo esplicito invece che lasciarlo implicito come oggi.

Sarebbe da sopostare prima di tutto il renamen e quindi fare le funzioni che hanno bisogno di info da CATALOG dopo il rename.

#### 5. def profile(df, cohort_col="COLPROT") -> pd.DataFrame:
riga 440 --> valutare e discutere quali altre info possono essere utili, tipo numero di visite per sogg con quel valore vero, ...
Aggiungere il calcolo di profile anche dopo clenaing2

#### 6. verbose - parametro ORCHESTRATORE
cosa significa? cos ainidca (riga 470)

#### 7. def merge_category(datasets: dict, category: str, mcfg=None):
riga 398 --> capire meglio la logica quindi integrare con regole altre categorie

Dubbio sul fatto che visite combacianti con metodi differenti vengano unite in una sola riga modificando il nome della variabile con il metodo. Da valutre e capire meglio perchè non tenere le cose separate.

#### 8. cleaned_by_category
riga 495 --> capire come funziona

#### 9. if cfg.volume_row_keys: --->  drop_if_all_none
if da riga 336 a 339 --> non sono sicura sia utile rimuovere la riga se ci sono i volumi nella tabella ma mancano in quella riga. perche potremmo cancallare altri valori utili. dopo il merge concellavamo una riga se non aveva nessun valore tra volumi PET e CSF

Anche keep columns da capire se necessaria... da investigare meglio --> in pipeline, da spostare in gonfig? o mettere lista default e dire ok si ci sono colonne in questa lista tenere solo quelle

Da studiare meglio il meccanismo di accoppiamento delle stesse visite. Attenzione se è necessario prima di agire nel match by bufferdate di fare ordine per ID e DATA in entrambi i df. potrebbe non essere necessario ma non so...il rischio potrebbe essere che una riga ha la setssa data di un altra (match esatto) ma è anche dentro il tempo buffer di 80gg della visita precedente. cosa succede se non trova metches? cancella tutto? non impila? Considerare anche VISCODE? trattamento visite equindistanti da una della base, ordine non cronologico dei dataset, ... mettere in log le distanza tra i match direi di dividere tra esatti e con buffer (buffer medio)

Problema le righe che indicano altre visite o soggetti vengono perse, e non attaccate in fondo. e no rientrano nei log-. --> usare outer join al posto che allign

Problema suffisso nel merge, se una variabile è solo in un metodo e non viene specificato nel nome della variabile in quanto non presente nell'altro file si perde il metodo di questa variabile ed ad un secondo merge per categoria non si saprebbe come operare. aggiungendo il 3 file non viene aggiunto il suffisso perchè non esiste più il nome base, in quanto già suffissato --> trovare rimedio
Altro problema, disassociazione dai nomi presenti in cutoff e CATALOG, da studiare come migliorare


--> consiglio rivedere con sotto anche il codice vechio, troppo complicato ma che ha considerato tanti aspetti. Consiglio di filtrare i df solo per le variabili di una categoria, oltre a RID exam date e VISCODE se usato, o altre var utili per la gerarchia di unione. Quindi magari rinominare con suffisso tutte le variabili prima di vedere se ci sono o meno nell'altro df così da non perdere collegamenti o altro.



#### 10. integrare con funzioni non considerate
Anche se nei file di test non ci sono delle caratteristiche dei file usati possiamo inziare ad aggiungere tali funzioni e testare poi su dati ADNI

#### 11. normazlizzazione volumi
viene mantenuto il nome originale e in CATALOG resta il riferimento dell'unità di misura in mm3. Da valutare se modificare il nome delle colonne post normalizzazione, o creare nuove colonne e cancellare quelle non normalizzate. Nel caso ci sono valutazioni da fare rispetto a Keep_columns_only ion quanto va aggiornato il config con i nomi post normalizzazione.


#### 12. affrontare i metadati 
ora in CATALOG ma con modifiche dummies e volumi o altro si perde il link... come fare?