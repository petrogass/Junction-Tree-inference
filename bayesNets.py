from copy import copy
import probTable as p

"""
Nel codice che segue si assume che un nodo abbia una struttura del genere:
node = {'table': , 'neighbours': [], 'separators': []}
e che un separatore abbia una struttura del genere:
sep = {'name': , 'table': }
dove table è una tabella di probabilità, neighbours è una lista di nodi adiacenti, separators è una lista di separatori dai nodi
adiacenti e name è un id per il separatore.
"""

def findSeparator(node1, node2):
	"""
	Trova e restituisce il separatore di due nodi adiacenti.
	Parametri:
		node1: un nodo
		node2: un nodo adiacente a node1
	"""
	for sep1 in node1['separators']:
		for sep2 in node2['separators']:
			if sep1['name'] == sep2['name']:
				return sep1

def update(sender, receiver):
	"""
	Implementa il "message passing" da un nodo a un altro adiacente.
	Parametri:
		sender: un nodo
		receiver: un nodo adiacente
	"""
	sep = findSeparator(sender, receiver)
	sharedColumns = set(sender['table'].columns).intersection(set(sep['table'].columns)).difference(set(["probs"]))
	newSepTable = p.marginalize(sender['table'], list(sharedColumns))
	receiver['table'] = p.divide(p.multiply(receiver['table'], newSepTable), sep['table'])
	sep['table'] = newSepTable	
	
def distributeEvidence(node, ignore = None):
	"""
	Propaga ricorsivamente i messaggi dal nodo da cui viene chiamato verso le foglie.
	Parametri:
		node: nodo da cui inizia la ricorsione
		ignore: nodo verso cui non propagare il messaggio (nodo da cui il messaggio è arrivato)
	"""
	neighbours = copy(node['neighbours'])
	if ignore in neighbours:
		neighbours.remove(ignore)
	for neighbour in neighbours:
		update(node, neighbour)
		distributeEvidence(neighbour, node)
	

def collectEvidence(node, ignore = None):
	"""
	Propaga ricorsivamente i messaggi dalle foglie verso il nodo chiamante.
	Parametri:
		node: nodo da cui inizia la ricorsione
		ignore: nodo verso cui non propagare il messaggio (nodo da cui il messaggio è arrivato)
	"""
	neighbours = copy(node['neighbours'])
	if ignore in neighbours:
		neighbours.remove(ignore)
	for neighbour in neighbours:
		collectEvidence(neighbour, node)
		update(neighbour, node)
	
		
def inference(root, nodes, separators, observations):
	"""
	Implementa l'algoritmo di inferenza per grafi orientati basato sul Junction tree.
	Parametri:
		root: nodo, radice scelta del Junction tree
		nodes: lista dei nodi del Junction tree
		separators: lista dei separatori del Junction tree
		observations: dizionario, ogni coppia key:value è del tipo "nomeColonna":valoreColonna, rappresenta le variabili da osservare
		margVars: lista di stringhe	
	"""
	for var,obs in observations.items():
		for node in nodes:
			if var in node['table'].columns:
				p.observe(node['table'], var, obs)
				break
				
	collectEvidence(root)
	print("Evidence collected")
	
	distributeEvidence(root)
	print("Evidence distributed")
	
	margVars = set(root['table'].columns)
	for node in nodes:
		margVars = margVars.union(set(node['table'].columns))	
	margVars.remove('probs')	
	
	for margVar in list(margVars):
		for node in nodes:
			if margVar in node['table'].columns:
				table = p.marginalize(node['table'], [margVar])
				table["probs"] = table["probs"] / sum(table["probs"])
				print(table)
				break