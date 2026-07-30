# ADNIMERGE — Pipeline di preprocessing

Pipeline Python (pandas) per la pulizia del dataset ADNIMERGE, organizzata in step sequenziali che operano sullo stesso file di output (`ADNIMERGE_cleaned_02.csv`), sovrascrivendolo ad ogni fase.

## File coinvolti

| File | Ruolo |
|---|---|
| `ADNIMERGE_cleaned_01.csv` | Dataset sorgente, già rinominato secondo il `CATALOG` di `config.py` |
| `ADNIMERGE_cleaned_02.csv` | Output della pipeline, letto e sovrascritto dagli step successivi al primo |
| `config.py` | Contiene le decisioni/dati della pipeline (soglie, mappe di ricodifica, catalogo variabili) — mai logica |

## Funzione di supporto

```python
save_dataset(df, path)
```
Salva il DataFrame su CSV (`index=False`) e stampa il percorso e la shape risultante. Richiamata al termine di ogni step che modifica i dati.

## Step della pipeline

### STEP 1 — Rimozione colonne con troppi valori mancanti
```python
remove_param_few_subjects(df, threshold=config.MISSING_KEEP_THRESHOLD)
```
Calcola, per ogni colonna, la percentuale di valori validi (`notna().mean()`) e scarta quelle sotto la soglia `MISSING_KEEP_THRESHOLD` (0.65) definita in `config.py`.

- **Input:** `ADNIMERGE.source` (`ADNIMERGE_cleaned_01.csv`)
- **Output:** `OUTPUT_FILE` (`ADNIMERGE_cleaned_02.csv`)

### STEP 2 — Conversione in dummy delle variabili categoriche
```python
classes_to_dummies(df, ref_list)
count_dummy_columns(original_df, final_df, converted_columns)
```
Converte in variabili binarie (one-hot, `dtype=int`) le colonne categoriche `GENDER`, `MARRY`, `ETHNICITY`, `RACE`, `DX` tramite `pd.get_dummies`. `count_dummy_columns` conta quante colonne dummy sono state generate, in totale e per variabile originale.

- **Input:** `DUMMY_INPUT = OUTPUT_FILE` (output dello STEP 1)
- **Output:** `DUMMY_OUTPUT` (`ADNIMERGE_cleaned_02.csv`, sovrascrive)

### STEP 3 — Rimozione righe senza dati volumetrici
```python
drop_if_all_none(df, key_columns)
```
Elimina le righe in cui **tutte** le colonne chiave (`KEY_COLUMNS = ['Ventricles', 'Hippocampus', 'WholeBrain', 'ICV']`) sono nulle, mantenendo quelle con almeno un valore valido.

- **Input/Output:** `OUTPUT_FILE` (`ADNIMERGE_cleaned_02.csv`, letto e sovrascritto)

### STEP 4 — Riallineamento dei tipi di colonna
```python
realign_column_types(df)
```
Ispeziona ogni colonna e la converte al tipo corretto in base al contenuto reale:
- numerico intero → `Int64` (nullable, gestisce i `NaN`)
- numerico non intero → `float64`
- non convertibile → `str`

Restituisce anche `type_report`, un log delle sole colonne il cui tipo è cambiato.

- **Input/Output:** `OUTPUT_FILE` (`ADNIMERGE_cleaned_02.csv`, letto e sovrascritto)

> **Nota:** poiché il CSV non conserva i dtype, ad ogni rilettura del file le colonne `Int64` con valori mancanti possono tornare a essere inferite come `float64` da pandas. Per un controllo persistente dei tipi, ripetere `realign_column_types` dopo ogni lettura, oppure passare a un formato che preserva i dtype (es. Parquet).

## Convenzioni della pipeline

- Il blocco iniziale di ogni step (import, `ADNIMERGE.source`, `OUTPUT_FILE`, eventuale `CUTOFFS_FILE`) **non va mai modificato**: si può solo aggiungere codice sotto.
- Variabili di comodo come `INPUT_FILE = OUTPUT_FILE` vanno definite subito prima del loro utilizzo, non in testa al file.
- Ogni funzione di trasformazione lavora su una copia (`df.copy()`) e restituisce sia il DataFrame sia un'informazione di log (colonne scartate, righe eliminate, colonne convertite, ecc.).
- Ogni step che modifica i dati termina con `save_dataset(...)` e, dove previsto, una verifica di coerenza (rilettura del file e confronto della shape).

### STEP 5 — Visualizzazione outlier (boxplot) e conteggio IQR
```python
select_measurement_columns(df, exclude_keywords, exclude_exact)
count_outliers_iqr(series)
plot_outliers_boxplot(df, columns, title, output_path, n_cols=5)
```
Individua le sole colonne di **misurazione** (punteggi clinico-cognitivi e volumetriche), scartando automaticamente id, protocollo, date, età e variabili demografiche (incluse le dummy `GENDER_`, `MARRY_`, `ETHNICITY_`, `RACE_`, `DX_`) tramite `select_measurement_columns`. Per ogni colonna mantenuta, `count_outliers_iqr` conta gli outlier con il metodo IQR (1.5×IQR oltre Q1/Q3); `plot_outliers_boxplot` genera una griglia di boxplot (uno per colonna, per gestire le diverse scale) con il conteggio di outlier riportato in ogni titolo, e salva l'immagine su file.

- **Input:** `OUTPUT_FILE` (`ADNIMERGE_cleaned_02.csv`, sola lettura)
- **Output:** immagine PNG con la griglia di boxplot; nessuna modifica al dataset

**Variante senza grafico:** `count_outliers_for_columns(df, columns)` applica lo stesso conteggio IQR a un elenco di colonne fornito esplicitamente (utile per includere anche colonne extra come `APOE4`, `FSVERSION`, `IMAGEUID` e le variabili `_bl`), stampando solo i risultati testuali senza generare il boxplot; segnala a parte le colonne non numeriche o assenti.

> **Nota:** il numero di outlier dipende dallo stato corrente del file (righe/valori), quindi può variare da un'esecuzione all'altra se nel frattempo sono stati applicati altri step della pipeline (es. `drop_if_all_none`, `realign_column_types`).

### STEP 5 — Visualizzazione outlier (heatmap) e conteggio IQR
```python
select_measurement_columns(df, exclude_keywords, exclude_exact)
count_outliers_iqr(series)
plot_outliers_heatmap(df, columns, title, output_path)
```
Individua le sole colonne di **misurazione** (punteggi clinico-cognitivi e volumetriche), scartando automaticamente id, protocollo, date, età e variabili demografiche (incluse le dummy `GENDER_`, `MARRY_`, `ETHNICITY_`, `RACE_`, `DX_`) tramite `select_measurement_columns`. Per ogni colonna mantenuta, `count_outliers_iqr` conta gli outlier con il metodo IQR (1.5×IQR oltre Q1/Q3); `plot_outliers_heatmap` genera un'**unica immagine a heatmap** (una riga, una cella per colonna), colorata in base alla percentuale di outlier sul totale dei valori validi, con numero assoluto e percentuale annotati in ogni cella.
 
- **Input:** `OUTPUT_FILE` (`ADNIMERGE_cleaned_02.csv`, sola lettura)
- **Output:** immagine PNG con la heatmap; nessuna modifica al dataset
**Variante senza grafico:** `count_outliers_for_columns(df, columns)` applica lo stesso conteggio IQR (tramite `count_outliers_iqr`) a un elenco di colonne fornito esplicitamente in `COLUMNS` (include anche colonne extra come `APOE4`, `FSVERSION`, `IMAGEUID` e le variabili `_bl`), stampando solo i risultati testuali senza generare alcun grafico; segnala a parte le colonne non numeriche o assenti.
 
> **Nota:** il numero di outlier dipende dallo stato corrente del file (righe/valori), quindi può variare da un'esecuzione all'altra se nel frattempo sono stati applicati altri step della pipeline (es. `drop_if_all_none`, `realign_column_types`).
 
### STEP 6 — Confronto e riduzione alle colonne di riferimento (COLONNE_CHIARA)
```python
compare_columns(df, reference_columns)
keep_only_reference_columns(df, reference_columns, extra_columns=None)
```
`COLONNE_CHIARA` è un elenco di riferimento (28 colonne) fornito per definire il set minimo di variabili da mantenere nel dataset. `compare_columns` confronta le colonne effettive del dataset con `COLONNE_CHIARA` in entrambe le direzioni: quali colonne del dataset non sono nell'elenco, e quali colonne dell'elenco non esistono nel dataset (queste ultime perché nel frattempo sono state rinominate — es. `PTGENDER`→`GENDER`— o trasformate in dummy — es. `DX`→`DX_0/1/2`).
 
`keep_only_reference_columns` filtra il dataset mantenendo solo le colonne in `COLONNE_CHIARA`, più un elenco opzionale di `extra_columns` da conservare comunque (es. le dummy `GENDER_0/1`, `MARRY_0.0…3.0`, `ETHNICITY_0.0/1.0`, `RACE_0.0…5.0`, `DX_0/1/2`, e `VISIT_MONTH`) — utile perché queste non compaiono in `COLONNE_CHIARA` ma non vanno scartate. Restituisce anche `dropped_columns` (colonne effettivamente rimosse) e `missing_in_dataset` (colonne richieste ma non trovate).
 
- **Input/Output:** `OUTPUT_FILE` (`ADNIMERGE_cleaned_02.csv`, letto e sovrascritto)
> **Nota:** una prima versione di questo step (senza `extra_columns`) è stata applicata, pushata su GitHub e poi annullata con `git revert`, perché eliminava le colonne dummy che invece si è deciso di mantenere. La versione corrente con `extra_columns` è quella da usare.
 
## Convenzioni di naming
 
- Il file di lavoro `ADNIMERGE_cleaned_02.csv` va sempre riferito come `OUTPUT_FILE`, mai `INPUT_FILE`.
- L'elenco di colonne di riferimento per STEP 6 si chiama `COLONNE_CHIARA` (non `REFERENCE_COLUMNS`, non `COLONNE_KEEP_CHIARA`).
## Step valutati ma non inclusi
 
- **Conversione `QCPASS`** (1/0 → `'complete'`/`'partial'`): non applicabile, la colonna `QCPASS` non è mai esistita nel dataset ADNIMERGE (appartiene al dataset CSF/UPENNBIOMK).
- **Profilo ATN** (`get_abeta_tau_ratios` + `get_ATN_profile`): rimosso per mancanza dei dati necessari — i biomarcatori `AB42_CSF`/`TTAU_CSF`/`PT181_CSF` erano presenti solo in `ADNIMERGE_cleaned_01.csv` (eliminati in STEP 1), `AB40_CSF`/`PT217_PL` non sono mai esistiti nel dataset, e manca il file `cutoffs.json`.