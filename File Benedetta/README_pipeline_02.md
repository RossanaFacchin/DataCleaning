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
