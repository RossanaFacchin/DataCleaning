# ADNI Cleaning 1 — ADNIMERGE

Riscrittura del primo passo di pulizia dati ADNI (`adni_cleaning1.ipynb`), adattato
al file `ADNIMERGE_05Mar2026.csv` ed eseguibile in locale, senza datalake.

Questo README è pensato per chi conosce il **vecchio** script (notebook + Excel di
supporto) e deve capire **cosa è cambiato**. Per ogni pezzo trovi: a cosa serve,
come si collega al vecchio mondo, e cosa aspettarti come risultato.

---

## 1. L'idea in una frase

Il lavoro è diviso in due file, e la divisione è tutto:

- **`config.py` = decisioni e dati.** Cosa tenere, come rinominare le variabili,
  quali soglie usare. È la parte che una persona sceglie. Sostituisce il vecchio
  file Excel `ADNI_variables_statistics.xlsx`.
- **`pipeline.py` = logica.** Le operazioni di pulizia vere e proprie, scritte una
  volta sola. Non si tocca per cambiare un dataset: si cambia solo il `config.py`.

Regola pratica per orientarsi: davanti a qualsiasi cosa, chiediti *«è una decisione/
un dato, o è un calcolo?»*. Se è una decisione (il nome standard di una variabile,
una soglia clinica) sta nel `config`; se è un calcolo (quanti valori mancano, il
minimo e il massimo) lo fa la `pipeline` e non lo scrivi a mano da nessuna parte.

---

## 2. Il `config.py`: perché, com'è fatto, come si scrive

Questa è la parte più importante da capire per chi arriva dal vecchio script.

### 2.1 Perché l'abbiamo tolto dall'Excel

Il vecchio `ADNI_variables_statistics.xlsx` mescolava **due cose diverse** nella
stessa tabella:

1. **Decisioni umane** — a che gruppo appartiene una variabile (`parameter`), come si
   rinomina (`orig_variable_code → variable_code`), se è un predittore, la sua unità.
2. **Statistiche calcolate dai dati** — tipo, range, numero di validi/mancanti, in
   quali coorti manca, `keep`/`drop`. Queste il codice le *ricava*, non le sceglie.

Il problema è che il notebook **leggeva e riscriveva lo stesso Excel a ogni giro**.
Da qui tre grane che forse hai già notato studiando il vecchio codice:

- l'ordine di esecuzione contava (il file cambiava sotto i piedi);
- i continui checkpoint "apri l'Excel e verifica a mano" prima di proseguire;
- il rischio concreto di corrompere il file.

La soluzione è separare le due cose:

- le **decisioni** vanno in `config.py` — che è *codice*, quindi versionato in git,
  leggibile in un diff, e se sbagli il nome di un campo il programma si ferma con un
  errore chiaro invece di produrre dati sbagliati in silenzio;
- le **statistiche** non si scrivono più a mano: le rigenera la funzione `profile()`
  in un CSV, ogni volta che serve.

In una riga: **l'Excel era insieme input e output; ora l'input è il `config.py` e
l'output è un report che si ricalcola da solo.**

### 2.2 Com'è strutturato

`config.py` ha sei sezioni. Ecco cosa contengono e a quale pezzo del vecchio mondo
corrispondono:

| Sezione in `config.py` | Cosa contiene | Da dove viene |
|------------------------|---------------|---------------|
| `POLICY` | Regole globali: valori-segnaposto dei mancanti, soglia keep/drop 65% | Numeri prima scritti a mano dentro le celle |
| `cutoff()` | Legge `cutoffs.json` (solo se serve) | `load_cutoffs` del vecchio codice |
| `RECODE` | Mappe stringa→codice (es. `DX`: CN→0, MCI→1) | Le mappe *dentro* le funzioni `categorize_*` |
| `CATALOG` | La tabella delle variabili | Le **righe** del foglio Excel |
| `DatasetConfig` + `ADNIMERGE` | La "scheda d'identità" del file | I valori scritti a mano in cima a ogni blocco del notebook |
| helper | Funzioncine di comodo (`rename_map`, `columns_in`) | — |

Il pezzo che sostituisce direttamente l'Excel è il **`CATALOG`**. Ogni riga del
vecchio foglio diventa una voce `Var`, e le colonne del foglio diventano i campi:

| Colonna Excel | Campo in `Var` |
|---------------|----------------|
| `parameter` | `Var.parameter` (il gruppo: ID, Demographic, Biomarker…) |
| `orig_variable_code` → `variable_code` | la **chiave** del catalogo (nome grezzo) → `Var.rename` (nome standard) |
| `Unit` | `Var.unit` |
| `metadati_fattori` = 'predittore' | `Var.role="predittore"` |
| `metadati_normalizzazione` | `Var.role="normalizzazione"` |
| `type_variable`, `classes`, `range`, `valid_values`, `missing_values`, `missing_pop`, `del` | **niente** — le rigenera `profile()` |

Quindi la riga di Excel `PTGENDER … parameter=Demographic … variable_code=GENDER`
diventa una sola riga di codice:

```python
"PTGENDER": Var("Demographic", rename="GENDER"),
```

E i valori che nel notebook erano scritti a mano in cima a ogni blocco (es.
`columns_must_be_verified`, `viscode_reference='VISCODE'`, le chiamate `categorize_*`,
l'`if file_code=='UCSFFSL'`) diventano campi della `DatasetConfig`:

| Nel notebook (a mano nella cella) | Campo in `DatasetConfig` |
|-----------------------------------|--------------------------|
| `columns_must_be_verified = [...]` | `essential_columns` |
| `single_column_required = ['DX']` | `also_required` |
| `find_exam_code(..., viscode_reference='VISCODE')` | `viscode_reference` |
| le chiamate `binarization_gender`, `categorize_marry`… | `recode_columns` (+ le mappe in `RECODE`) |
| `add_calculated_age(...)` presente | `recompute_age=True` |
| pulizia `FLDSTRENG`/`FSVERSION` | `clean_fs_fields=True` |
| `get_ATN_profile(...)` presente (file CSF) | `compute_atn=True`, `atn_method=...` |

### 2.3 Come si scrive

Tre casi pratici, che coprono quasi tutto quello che farai.

**A) Aggiungere una variabile** (equivale ad aggiungere una riga all'Excel).
Aggiungi una voce al `CATALOG`. La chiave è il nome **grezzo** (come sta nel CSV),
`rename` è il nome **standard** che vuoi in uscita (omettilo se non cambia):

```python
CATALOG = {
    ...
    "MOCA": Var("Cognitive", role="predittore"),          # tenuta col suo nome
    "PTEDUCAT": Var("Demographic", rename="EDUCATION"),   # rinominata
}
```

**B) Ricodificare una categoria** (equivale a una funzione `categorize_*`).
Aggiungi la mappa a `RECODE` e poi elenca la colonna in `recode_columns` del dataset:

```python
RECODE = {
    ...
    "DX": {"CN": 0, "MCI": 1, "Dementia": 2},   # stringa -> codice
}
# e nel DatasetConfig:
recode_columns = ["PTGENDER", "DX", ...]
```

**C) Configurare un file** (equivale a scrivere l'intestazione di un blocco del
notebook). Compili una `DatasetConfig`. Questa è quella di ADNIMERGE, commentata:

```python
ADNIMERGE = DatasetConfig(
    file_code="ADNIMERGE",
    source="ADNIMERGE_05Mar2026.csv",
    essential_columns=["APOE4","MMSE","Ventricles","Hippocampus","AGE"],  # tieni riga se >=1 c'è
    also_required=["DX"],                     # ...e in più DX deve esserci
    recode_columns=["PTGENDER","PTMARRY","PTETHCAT","PTRACCAT","DX"],
    recompute_age=True,                       # ricalcola l'età a ogni visita
    clean_fs_fields=True,                     # sistema FLDSTRENG/FSVERSION
    # compute_atn resta False: ADNIMERGE non calcola l'ATN
)
```

Cosa **non** devi fare: aprire `pipeline.py` per cambiare un dataset. Se ti trovi a
volerlo modificare per aggiungere un file, probabilmente quella cosa era una
decisione e andava nel `config`. La `pipeline` cambia solo se serve una *nuova
operazione* che prima non esisteva.

---

## 3. I file del pacchetto

| File | Cos'è | Si modifica? |
|------|-------|--------------|
| `config.py` | Decisioni e dati (ex Excel) | Sì, qui si lavora |
| `pipeline.py` | La logica di pulizia | No, si legge |
| `ADNIMERGE_05Mar2026.csv` | I dati grezzi in ingresso | No |
| `README.md` | Questo documento | — |

Mettili tutti nella stessa cartella.

---

## 4. Come si esegue

Da terminale, nella cartella:

```bash
python3 pipeline.py
```

**Output atteso:**

```
cleaning1 ADNIMERGE: 11458 righe x 118 colonne
scritti: ADNIMERGE_cleaned_01.csv, ADNIMERGE_report.csv
```

Vengono creati due file: `ADNIMERGE_cleaned_01.csv` (il dataset pulito) e
`ADNIMERGE_report.csv` (le statistiche di qualità, che prima si riscrivevano a mano
nell'Excel e ora si rigenerano da sole).

---

## 5. Cosa fa, passo per passo

La funzione `run_cleaning1()` in `pipeline.py` esegue queste azioni in ordine. Per
ognuna: cosa faceva il notebook originale, l'obiettivo, e l'output atteso.

### Passo 0 — Caricamento (`load`)
- **Notebook:** scaricava il file dal datalake. **Qui:** `pd.read_csv`.
- **Obiettivo:** portare i dati grezzi in memoria.
- **Output atteso:** ~16.421 righe.

### Passo 1 — Uniformare i valori mancanti (`replace_unknown`)
- **Obiettivo:** i dataset clinici indicano "dato assente" in tanti modi diversi
  (`"Unknown"`, `-4`, `9999`…). Questo passo li trasforma tutti in un unico valore
  mancante standard (`NaN`), così i conteggi successivi sono corretti.
- **Output atteso:** stesso numero di righe, ma i segnaposto ora sono `NaN`.

### Passo 2 — Scartare le righe senza dati importanti (`drop_if_all_none`, 1ª volta)
- **Obiettivo:** buttare via le righe che non hanno **nessuna** delle misure chiave
  (`APOE4, MMSE, Ventricles, Hippocampus, AGE`). Una riga si tiene se ne ha almeno una.
- **Output atteso:** ~16.421 righe (in pratica non scarta quasi nulla, perché `AGE`
  è quasi sempre presente — è un controllo di sicurezza più che un taglio).

### Passo 3 — Richiedere la diagnosi (`drop_if_all_none`, 2ª volta, su `DX`)
- **Obiettivo:** tenere solo le righe che hanno la diagnosi clinica `DX`.
- **Output atteso:** **11.458 righe.** *È qui che avviene il taglio vero* (da ~16.421
  a 11.458): sono le righe senza diagnosi a essere rimosse.

### Passo 4 — Sistemare le date (`parse_dates`)
- **Obiettivo:** trasformare la colonna `EXAMDATE` in vere date, così si possono
  ordinare e sottrarre.
- **Output atteso:** stesso numero di righe; `EXAMDATE` diventa di tipo data.

### Passo 5 — Riconoscere le visite (`dedup_visits` + `add_visit_month`)
- **Obiettivo:** se lo stesso soggetto ha due righe nella stessa data, tenere la più
  completa; poi calcolare `VISIT_MONTH` = mesi trascorsi dalla prima visita.
- **Output atteso:** 11.458 righe (0 duplicati in ADNIMERGE), **2.409 soggetti unici**,
  `VISIT_MONTH` con valori 0, 6, 12, 24…

### Passo 6 — Ricalcolare l'età (`recompute_age`)
- **Obiettivo:** nel file `AGE` è l'età alla prima visita. Questo passo la rinomina in
  `AGE_bl` e crea una nuova `AGE` aggiornata a ogni visita (età iniziale + tempo passato).
- **Output atteso:** compaiono `AGE_bl` (fissa) e `AGE` (che cresce nelle visite successive).

### Passo 7 — Ricodificare le categorie (`recode`)
- **Obiettivo:** trasformare le stringhe in codici numerici secondo le mappe in
  `config.RECODE` (es. `DX`: CN→0, MCI→1, Dementia→2; sesso, stato civile, etnia, razza).
- **Output atteso:** `GENDER` diventa 0/1, `DX` diventa 0/1/2, ecc.

### Passo 8 — Pulire i campi tecnici (`clean_fs_fields`)
- **Obiettivo:** normalizzare `FLDSTRENG` e `FSVERSION` estraendone la parte numerica.
- **Output atteso:** `FLDSTRENG` diventa `1.5T` / `3T`.

### Passo 9 — Rinominare secondo lo standard (`rename_variables`)
- **Notebook:** leggeva la mappa dei nomi dall'Excel. **Qui:** dalla sezione `CATALOG`
  del `config.py`.
- **Obiettivo:** dare a ogni variabile il nome standard del progetto (es. `PTGENDER→GENDER`).
- **Output atteso:** le colonne del `CATALOG` compaiono col nome nuovo.

### Passo 10 — Report di qualità (`profile`)
- **Notebook:** aggiornava a mano l'Excel di supporto. **Qui:** genera un CSV.
- **Obiettivo:** per ogni variabile, calcolare tipo, min/max, quanti valori validi e
  mancanti, in quali coorti manca, e se tenerla o scartarla (soglia 65%).
- **Output atteso:** `ADNIMERGE_report.csv`. Attenzione: «gira» non vuol dire «giusto» —
  il report serve proprio a guardare *cosa* è uscito.

### Risultato finale
Un dataset di **11.458 righe × 118 colonne**, 2.409 soggetti, salvato in
`ADNIMERGE_cleaned_01.csv`.

---

## 6. Quali JSON servono e quali no

Il progetto ha quattro file JSON di settaggio. **Per questo passo (cleaning 1 su
ADNIMERGE) NON ne serve nessuno.** Ecco perché, uno per uno:

| File JSON | A cosa serve | Serve qui? |
|-----------|--------------|------------|
| `cutoffs.json` | Soglie per il profilo ATN (Amiloide/Tau/Neurodegenerazione) | **No** per ADNIMERGE. L'ATN si calcola solo sui file CSF (es. UPENNBIOMK); ADNIMERGE non lo fa, quindi il file non viene nemmeno letto. |
| `normalization_settings.json` | Intervalli per la normalizzazione min-max | **No.** Appartiene a un passo successivo (cleaning 3/4), non a cleaning 1. |
| `volume_values_settings.json` | Intervalli dei volumi cerebrali | **No.** Anche questo è di cleaning 3/4. |
| `cofattori_values_settings.json` | Intervalli dei cofattori (es. APOE) | **No.** Cleaning 2/3/4. |

Prova concreta: se togli `cutoffs.json` dalla cartella e riesegui, `pipeline.py`
**funziona lo stesso** e produce le stesse 11.458 righe, perché ADNIMERGE non lo usa.
Il file `cutoffs.json` diventa necessario solo se in `config.py` un dataset ha
`compute_atn=True` (i file CSF) — e in quel caso, se manca, il codice si ferma con un
errore chiaro invece di produrre dati incompleti in silenzio.

---

## 7. Le scelte fatte (e perché)

Queste sono le decisioni prese in `config.py`, fedeli al blocco ADNIMERGE del notebook:

- **Righe da tenere:** almeno una tra `APOE4/MMSE/Ventricles/Hippocampus/AGE`, **e** la
  diagnosi `DX` presente. È la ragione delle 11.458 righe.
- **Codici delle categorie:** seguono la convenzione del notebook (es. razza:
  White=5, Black=4, Asian=2, Am Indian=1, Hawaiian=3, More than one=0). Non è una
  convenzione nuova: è quella già in uso, per restare compatibili.
- **Niente profilo ATN:** nel notebook l'ATN è solo per i file CSF, non per ADNIMERGE.
  Qui si è mantenuta la stessa scelta (`compute_atn=False`).
- **Età ricalcolata per visita** e **`FLDSTRENG/FSVERSION` normalizzati**, come nel notebook.

Se un domani cambia l'obiettivo dell'analisi (es. serve un dataset centrato sui
biomarcatori invece che sulla diagnosi), si modifica solo `essential_columns` /
`also_required` in `config.py`: la logica in `pipeline.py` resta identica.

---

## 8. Cosa NON fa questo pacchetto

È solo **cleaning 1** (pulizia del singolo file). Restano fuori, come nel progetto
originale, i passi successivi, che seguono lo stesso schema config + pipeline:

- creazione delle variabili dummy e rimozione di soggetti/variabili scarse (cleaning 2);
- normalizzazione dei volumi rispetto all'ICV (cleaning 3/4);
- unione tra file diversi (merge).

E il datalake: qui è sostituito dalla lettura/scrittura di CSV in locale, perché
l'accesso al datalake non è il punto — il punto è come è scritta la pipeline.