# Esame-AI
Implementazione dell'algoritmo di inferenza su Junction tree. 

Per dimostrare la funzionalità del codice si è scelto come esempio giocattolo il Chest Clinic problem.
Per far girare il codice sono necessari Python3, pandas e il modulo copy di Python.
Assicurandosi che probTable.py, chestClinic.py e bayesNets.py siano nella stessa cartella, navigare da riga di comando in quella cartella e chiamare python chestClinic.py.
In chestClinic.py viene descritto il Junction tree del grafo e come esempio viene chiamato l'algoritmo di inferenza senza dare evidenza ad alcuna variabile.
Verranno stampate a schermo delle tabelle, una per ogni variabile del grafo, a indicare le probabilità marginali di ogni variabile (0 è No e 1 è Sì)

Le diverse lettere stampate a schermo come nome delle colonne indicano le varie variabili:
A: Visit to Asia?
L: Lung Cancer?
T: Tubercolosis?
D: Dyspnea?
B: Bronchitis?
S: Smoker?
E: Tubercolosis or lung cancer?
X: Positive x-ray?

È possibile introdurre evidenza modificando l'ultimo parametro della chiamata a bn.inference() in chestClinic.py, non è possibile però fare più chiamate di fila sullo stesso grafo in quanto quest'ultimo non viene reinizzializzato ogni volta.
Per esempio, se al posto di {} (ultimo parametro nella chiamata a bn.inference) mettiamo {"S":1} e chiamiamo di nuovo chestClinic.py da riga di comando, effettueremo inferenza sul grafo dando come evidenza "Smoker? sì".
L'evidenza inserita deve essere coerente (e.g. {"T":1, "E":0} non lo è) altrimenti il programma non funziona come ci si aspetta.


Per il metodo createTable(vars, probs, domains) ho preso spunto riadattandolo ai miei bisogni dal metodo createCPT(varnames, probs, levelsList) presente a 
questo link http://www.cs.utah.edu/~fletcher/cs6190/homeworks/hw2/BayesianNetworks-template.txt
