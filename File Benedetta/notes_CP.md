# Note di modifica by Chiara
Raccolta di pensieri e domande per modificare in secondo luogo pipeline e config.

## Indice:
A. domande
B. Cose da cambiare
C. Cosa aggiungere
D. Cose da fare/strategia


## A. Domande
### A.1 Anticipare rename
Pro e contro di anticipare il rename il prima possibile

### A.2 eliminazione colonne
Come mai le colonne che non ci servono vengono rimosse solo in Cleaning_2 e non subito dopo il load? --> discussione B.2

### A.3 aggiunta info di log
def profile(df, cohort_col="COLPROT") -> pd.DataFrame:
riga 440 --> valutare e discutere quali altre info possono essere utili, tipo numero di visite per sogg con quel valore vero, ... Aggiungere il calcolo di profile anche dopo clenaing2

### A.4 line removal
ci son 2 funzioni per rimuovere soggetti e righe (single subject ecc...) in cleaning 2. Un idea sarebbe fare 1 sola fase di pulizia pre merge e qua non mettere nemmeno questa possibilità e togliere il flag true e false dalle info del file. E mettere questi removal direttamente post merge.

### A.5 Merge
rivedere la strategia di merge --> spunto analsi Rossana



## B. Cose da cambiare/proposte
### B.1 anticipare RENAME
Riprendere codic Rossana, anticipare RENAME permette di poi usare i nomi standard delle varribaili.
Cambiamento discutibile.

### B.2 anticipare eliminazione colonne
Non so se spostare completamente l'elminazione delle colonne non utili, tipo variabili che non studiamo, subito dopo il loader, oppure fare uno split, eliminare subito le variabili che possono causare problemi (VISCODE quando c'è VISCODE2). E alla fine della pulizia pre merge eliminare le colonne che ci servivano per calcolare cose come l'età. E magari riutilizzare la stessa finzione dopo il merge per eliminare variabili di qualità o time stamp utili per decidere quale valore tenere nel caso di duplicati. 
--> idea 1 funzione che elimina ma usata 3 volte: quando sai esattamente che colonne assolutamente vuoi eliminare (subito), quando sai quali colonne vuoi tenre x2 pre e post merge.

### B.3 proposta ottimizzazione def drop_if_all_none(df, cols):
(riga 79 di pipeline) Viene chiamata due volte, una per le colonne essenziali e una per quelle anche richieste. Ma potremmo fare una piccola modifica aggiungendo un clco for all'interno della funzione e fornire una lista di liste al posto di cols (esempio: cols = [["APOE4", "MMSE", "Ventricles", "Hippocampus", "AGE"],["DX"], ["EXAMDATE", "VISCODE"]])
In questo modo possono essere proposte diverse combinazione di colonne essenziali, da sole o in combinazione.
Da valutare se il costo computazionale di usare un for è eccessivo.

### B.4 def recompute_age
(riga 122, pipeline) va adattata alle diverse info che i dataset hanno per calcolare l'età. Nel branch di Rossana ci sono già dei miglioramnti. 
Direi di **arrotondare** l'età al primo valore decimale.

### B.5 def recode(df, cols):
(riga 130, pipeline) valutare di mappare non numericamente ma con stringhe standard poi utili per dummies per non ritrasformarle in numeri o dummies leggibili.

### B.6 CATALOG definizione rename
NB partial implemented
Partire dal nome standard quindi lista di variabili che corrispondono a tale name standard, e non nome grezzo e quindi definisco il rename, ottimizza la compilazione di nuove variabili.
Un solo punto dove aggiungere un nuovo sinonimo quando lo si scopre in un nuovo file (basta appendere alla lista aliases), senza toccare parameter/unit/role. Il nome standard è scritto una sola volta (come chiave del dizionario) → niente più rischio di typo sparsi tra file diversi. Assicurarsi non ci sia lo stesso nome per diversi nomi standard / alias. I casi speciali restano.
Aspetti da verificare:
- dinamica che vince l'ultimo valonre nel rename.
- Cosa succede se ci sono 2 var nello stesso DF che vengono rinominate nello stesso modo? (special cases o eliminazione del duplicato es VISCODE se c'è VISCODE2)
- Come trattare volumi e dummies (magari possiamo aggiungere subito le variabili modificate come aggiuntive standard, ma no alias iniziali.)


## C. Cosa aggiungere
### C.1 automatic range 
aggiungere funziona che calcola i range per ciascuna variabile (di quelle che ci interessano) e salva su json indicando nome file, quindi per i merge viene riutilizzata.

### C.2 Funzioni analisi
magari qua dobbiamo fare un file precedente a pipeline le cui info poi servono per riempire il config.


## D. Cose da fare/strategia


6. verbose - parametro ORCHESTRATORE
cosa significa? cosa inidca (riga 470)



8. cleaned_by_category
riga 495 --> capire come funziona

9. if cfg.volume_row_keys: ---> drop_if_all_none
if da riga 336 a 339 --> non sono sicura sia utile rimuovere la riga se ci sono i volumi nella tabella ma mancano in quella riga. perche potremmo cancallare altri valori utili. dopo il merge concellavamo una riga se non aveva nessun valore tra volumi PET e CSF

Anche keep columns da capire se necessaria... da investigare meglio --> in pipeline, da spostare in gonfig? o mettere lista default e dire ok si ci sono colonne in questa lista tenere solo quelle

Da studiare meglio il meccanismo di accoppiamento delle stesse visite. Attenzione se è necessario prima di agire nel match by bufferdate di fare ordine per ID e DATA in entrambi i df. potrebbe non essere necessario ma non so...il rischio potrebbe essere che una riga ha la setssa data di un altra (match esatto) ma è anche dentro il tempo buffer di 80gg della visita precedente. cosa succede se non trova metches? cancella tutto? non impila? Considerare anche VISCODE? trattamento visite equindistanti da una della base, ordine non cronologico dei dataset, ... mettere in log le distanza tra i match direi di dividere tra esatti e con buffer (buffer medio)

Problema le righe che indicano altre visite o soggetti vengono perse, e non attaccate in fondo. e no rientrano nei log-. --> usare outer join al posto che allign

Problema suffisso nel merge, se una variabile è solo in un metodo e non viene specificato nel nome della variabile in quanto non presente nell'altro file si perde il metodo di questa variabile ed ad un secondo merge per categoria non si saprebbe come operare. aggiungendo il 3 file non viene aggiunto il suffisso perchè non esiste più il nome base, in quanto già suffissato --> trovare rimedio Altro problema, disassociazione dai nomi presenti in cutoff e CATALOG, da studiare come migliorare

--> consiglio rivedere con sotto anche il codice vechio, troppo complicato ma che ha considerato tanti aspetti. Consiglio di filtrare i df solo per le variabili di una categoria, oltre a RID exam date e VISCODE se usato, o altre var utili per la gerarchia di unione. Quindi magari rinominare con suffisso tutte le variabili prima di vedere se ci sono o meno nell'altro df così da non perdere collegamenti o altro.

10. integrare con funzioni non considerate
Anche se nei file di test non ci sono delle caratteristiche dei file usati possiamo inziare ad aggiungere tali funzioni e testare poi su dati ADNI

11. normazlizzazione volumi
viene mantenuto il nome originale e in CATALOG resta il riferimento dell'unità di misura in mm3. Da valutare se modificare il nome delle colonne post normalizzazione, o creare nuove colonne e cancellare quelle non normalizzate. Nel caso ci sono valutazioni da fare rispetto a Keep_columns_only ion quanto va aggiornato il config con i nomi post normalizzazione.

12. affrontare i metadati
ora in CATALOG ma con modifiche dummies e volumi o altro si perde il link... come fare?

13. verificare tutte le mappature RECODE (da fare in un secondo momento)
Controllare sul dizionario dati ADNI tutte le mappature di `config.RECODE`, sia le stringhe di ADNIMERGE sia i codici numerici di PTDEMOG portati dal branch Assignment_analysis_fr (D031). In particolare: MARRY 6 → married, RACE 8 e 9 → hawaiian, RACE "/" → mixed, e i valori multipli tipo "1|5" → mixed. Le mappature sono state portate tali e quali, ritenute accurate.

14. rivedere catalog.json (dopo i passi 4-6 del 20/10/2026)
- Definizioni: sono in bozza (scritte da Claude), da rileggere voce per voce; le voci create dalla migrazione dei rename hanno "Definizione in bozza" e vanno completate.
- Due rename del generatore di bozze, migrati tali e quali ma clinicamente dubbi: CDR `CDGLOBAL -> CDRSB` (CDR globale 0-3 non e' il Sum of Boxes 0-18) e APOERES `GENOTYPE -> APOE4` (genotipo vs numero di alleli e4). Vedi DECISIONI D017.
- Codici standard: verificati solo MMSE (LOINC 72106-8) e MoCA (LOINC 72172-0). Completare a mano su Athena / loinc.org / AD-Mapper (D033).
- Domini nuovi introdotti: History (PTADBEG, PTCOGBEG, PTADDX), QC, Metadata: confermare o rinominare.
