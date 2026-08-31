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

## B. Cose da cambiare/proposte
### B.1 anticipare RENAME


### B.2 anticipare eliminazione colonne
Non so se spostare completamente l'elminazione delle colonne non utili, tipo variabili che non studiamo, subito dopo il loader, oppure fare uno split, eliminare subito le variabili che possono causare problemi (VISCODE quando c'è VISCODE2). E alla fine della pulizia pre merge eliminare le colonne che ci servivano per calcolare cose come l'età. E magari riutilizzare la stessa finzione dopo il merge per eliminare variabili di qualità o time stamp utili per decidere quale valore tenere nel caso di duplicati. 
--> idea 1 funzione che elimina ma usata 3 volte: quando sai esattamente che colonne assolutamente vuoi eliminare (subito), quando sai quali colonne vuoi tenre x2 pre e post merge.

### B.3 proposta ottimizzazione def drop_if_all_none(df, cols):
(riga 79 di pipeline) Viene chiamata due volte, una per le colonne essenziali e una per quelle anche richieste. Ma potremmo fare una piccola modifica aggiungendo un clco for all'interno della funzione e fornire una lista di liste al posto di cols (esempio: cols = [["APOE4", "MMSE", "Ventricles", "Hippocampus", "AGE"],["DX"], ["EXAMDATE", "VISCODE"]])
In questo modo possono essere proposte diverse combinazione di colonne essenziali, da sole o in combinazione.
Da valutare se il costo computazionale di usare un for è eccessivo.

### B.4 def recompute_age
(riga 122, pipeline) va adattata alle diverse info che i dataset hanno per calcolare l'età. Nel branch di Rossana ci sono già dei miglioramnti. 
Direi di arrotondare l'età al primo valore decimale.

### B.5 def recode(df, cols):
(riga 130, pipeline) valutare di mappare non numericamente ma con stringhe standard poi utili per dummies per non ritrasformarle in numeri o dummies leggibili.

## C. Cosa aggiungere
### C.1 automatic range 
aggiungere funziona che calcola i range per ciascuna variabile (di quelle che ci interessano) e salva su json indicando nome file, quindi per i merge viene riutilizzata.

### C.2 Funzioni analisi
magari qua dobbiamo fare un file precedente a pipeline le cui info poi servono per riempire il config.


## D. Cose da fare/strategia



3. def recode(df, cols):
riga 130 --> valutare di mappare non numericamente ma con stringhe standard poi utili per dummies per non ritrasformarle in numeri.

4. CATALOG r def rename
sia in config che in pipeline Problema attuale

CATALOG è indicizzato per nome grezzo (PTGENDER, NF_LIGHT...), non per concetto. Se la stessa variabile concettuale (es. "genere") appare con nomi diversi tra file (PTGENDER, SEX, Gender...), oggi l'unico modo per gestirlo è:

aggiungere ogni sinonimo come voce separata in CATALOG (duplica parameter/unit/role più volte), oppure aggiungerlo nel self.rename del singolo DatasetConfig (ma allora quel sinonimo non eredita gli attributi di CATALOG — solo il nome standard). In entrambi i casi il nome standard ("GENDER") resta una stringa scritta a mano in più punti → rischio di typo silenziosi.

Strategia proposta: invertire la chiave di CATALOG

Indicizzare CATALOG per nome standard invece che per nome grezzo, e aggiungere alla Var una lista di sinonimi noti:

CATALOG = { "GENDER": Var(parameter="Demographic", aliases=["PTGENDER", "SEX", "Gender"]), "AGE": Var(parameter="Demographic", unit="years", aliases=["AGE"]), ... } Da qui si genera automaticamente la mappa inversa (grezzo → standard) usata per il rename:

def rename_map(): return {alias: std for std, v in CATALOG.items() for alias in v.aliases} Vantaggi:

Un solo punto dove aggiungere un nuovo sinonimo quando lo si scopre in un nuovo file (basta appendere alla lista aliases), senza toccare parameter/unit/role. Il nome standard è scritto una sola volta (come chiave del dizionario) → niente più rischio di typo sparsi tra file diversi. Si può validare a "import time" che nessun alias sia condiviso per errore da due variabili standard diverse (basta un controllo che segnali duplicati in fase di costruzione della reverse map). Cosa resta invariato: self.rename per-file continua a esistere per i casi eccezionali già visti (stesso nome grezzo che significa cose diverse a seconda del file, o override intenzionali) — resta il meccanismo di "ultima parola" che vince sui conflitti, ma sarebbe usato solo per le vere eccezioni, non per i sinonimi comuni ormai gestiti da aliases.

Trade-off da considerare: richiede di riscrivere CATALOG esistente (migrazione una tantum) e serve decidere cosa succede se due file usano lo stesso alias con significati diversi — da gestire con un controllo esplicito invece che lasciarlo implicito come oggi.

Sarebbe da sopostare prima di tutto il renamen e quindi fare le funzioni che hanno bisogno di info da CATALOG dopo il rename.

5. def profile(df, cohort_col="COLPROT") -> pd.DataFrame:
riga 440 --> valutare e discutere quali altre info possono essere utili, tipo numero di visite per sogg con quel valore vero, ... Aggiungere il calcolo di profile anche dopo clenaing2

6. verbose - parametro ORCHESTRATORE
cosa significa? cos ainidca (riga 470)

7. def merge_category(datasets: dict, category: str, mcfg=None):
riga 398 --> capire meglio la logica quindi integrare con regole altre categorie

Dubbio sul fatto che visite combacianti con metodi differenti vengano unite in una sola riga modificando il nome della variabile con il metodo. Da valutre e capire meglio perchè non tenere le cose separate.

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