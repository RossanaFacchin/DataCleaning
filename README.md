"""
ANALISI ESPLORATIVA DEL DATASET ADNIMERGE
==========================================

Questo script esegue un'analisi esplorativa (EDA) del dataset
ADNIMERGE_05Mar2026.csv, proveniente dallo studio ADNI (Alzheimer's
Disease Neuroimaging Initiative). Non modifica o pulisce i dati: si
limita a ispezionarli e a produrre riepiloghi utili come punto di
partenza per una successiva fase di data cleaning.

REQUISITI
---------
- Python 3
- pandas
- matplotlib

Il file ADNIMERGE_05Mar2026.csv deve trovarsi nella stessa cartella
dello script (oppure va aggiornato il percorso in pd.read_csv(...)).

COSA FA LO SCRIPT, PASSO PER PASSO
-----------------------------------
1. CARICAMENTO DATI
   Legge il CSV in un DataFrame pandas e ne stampa le prime righe
   con df.head().

2. ESPLORAZIONE DELLE COLONNE
   Stampa l'elenco completo delle colonne (come lista, riga per riga,
   e con il conteggio totale).

3. VALORI UNICI PER COLONNA
   - Mostra i valori unici della colonna PTGENDER come esempio.
   - Con un ciclo su tutte le colonne, stampa per ciascuna il numero
     di valori unici e la relativa distribuzione di frequenza
     (value_counts).
   - Costruisce un DataFrame riepilogativo (summary) con colonna e
     numero di valori unici, ordinato dal più basso al più alto.

4. ANALISI DEI VALORI MANCANTI (NaN)
   - Per ogni colonna calcola numero e percentuale di valori nulli,
     stampandoli a video.
   - Crea due DataFrame di riepilogo (null_summary e un secondo
     summary con formattazione leggermente diversa) ordinati per
     numero di nulli decrescente.
   - Isola le sole colonne con oltre il 40% di valori nulli,
     contandole.

5. STATISTICHE DESCRITTIVE
   - df.describe(include='all') per una panoramica generale su tutte
     le colonne.
   - Un ciclo che stampa describe() separatamente per ogni colonna.

6. ANALISI DEGLI OUTLIER
   Per ogni colonna numerica, calcola gli outlier con il metodo IQR
   (Interquartile Range):
   - IQR = Q3 - Q1
   - limiti: Q1 - 1.5*IQR e Q3 + 1.5*IQR
   - conta quanti valori cadono fuori da questi limiti e la relativa
     percentuale.
   Il risultato è raccolto in outlier_df, ordinato per percentuale di
   outlier decrescente.
   (È presente anche un blocco commentato che, se riattivato, disegna
   un boxplot per ogni colonna numerica con matplotlib.)

7. RIGHE DUPLICATE
   Conta il numero di righe duplicate nel dataset con
   df.duplicated().sum().

OUTPUT
------
Lo script è pensato per l'esecuzione interattiva (es. Jupyter
Notebook o console): produce solo output testuale a schermo (stampe
e DataFrame), senza salvare file su disco. Se si riattiva il blocco
commentato dei boxplot, verranno mostrati anche grafici a schermo
tramite plt.show().

NOTE
----
- Alcune sezioni sono ridondanti (es. il calcolo dei nulli viene
  ripetuto tre volte in forme leggermente diverse): probabilmente
  derivano da iterazioni successive dello script più che da una
  progettazione finale; si potrebbe consolidarle in un'unica
  funzione riutilizzabile.
- L'import di pandas e matplotlib.pyplot è ripetuto due volte nel
  file.
- Lo script non salva alcun risultato (né i DataFrame di riepilogo
  né i grafici): se serve conservarli, andrebbero aggiunte righe di
  .to_csv() o plt.savefig().
"""