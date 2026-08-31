# Note di modifica by Chiara
Raccolta di pensieri e domande per modificare in secondo luogo pipeline e config.

## Indice:
A. domande
B. Cose da cambiare
C. Cosa aggiungere
D. Cose da fare/strategia


## A. Domande
### A.1 eliminazione colonne
Come mai le colonne che non ci servono vengono rimosse solo in Cleaning_2 e non subito dopo il load? --> discussione B.1

## B. Cose da cambiare
### B.1 anticipare eliminazione colonne
Non so se spostare completamente l'elminazione delle colonne non utili, tipo variabili che non studiamo, subito dopo il loader, oppure fare uno split, eliminare subito le variabili che possono causare problemi (VISCODE quando c'è VISCODE2). E alla fine della pulizia pre merge eliminare le colonne che ci servivano per calcolare cose come l'età. E magari riutilizzare la stessa finzione dopo il merge per eliminare variabili di qualità o time stamp utili per decidere quale valore tenere nel caso di duplicati. 
--> idea 1 funzione che elimina ma usata 3 volte: quando sai esattamente che colonne assolutamente vuoi eliminare (subito), quando sai quali colonne vuoi tenre x2 pre e post merge.

## C. Cosa aggiungere
### C.1 automatic range 
aggiungere funziona che calcola i range per ciascuna variabile (di quelle che ci interessano) e salva su json indicando nome file, quindi per i merge viene riutilizzata.

### C.2 Funzioni analisi
magari qua dobbiamo fare un file precedente a pipeline le cui info poi servono per riempire il config.


## D. Cose da fare/strategia