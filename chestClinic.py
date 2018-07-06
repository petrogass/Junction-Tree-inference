import bayesNets as bn
import probTable as p
"""
Creo le tabelle associate ai nodi della rete bayesiana.
"""
asia = p.createTable(["A"], [0.99, 0.01], [[0,1]])
tbc = p.createTable(["A", "T"], [0.99, 0.01, 0.95, 0.05], [[0,1],[0,1]])
smoker = p.createTable(["S"], [0.5, 0.5], [[0,1]])
cancer = p.createTable(["S", "L"], [0.99, 0.01, 0.9, 0.1], [[0,1],[0,1]])
bronchitis = p.createTable(["S", "B"], [0.7, 0.3, 0.4, 0.6], [[0,1],[0,1]])
tbcOrCancer = p.createTable(["T", "L", "E"], [1, 0, 0, 1, 0, 1, 0, 1], [[0,1],[0,1],[0,1]])
dyspnoea = p.createTable(["B", "E", "D"], [0.9, 0.1, 0.3, 0.7, 0.2, 0.8, 0.1, 0.9], [[0,1],[0,1],[0,1]])
xray = p.createTable(["E", "X"], [0.95, 0.05, 0.02, 0.98], [[0,1],[0,1]])
"""
Imposto le tabelle da assegnare ai nodi del junction tree.
"""
a= p.createTable(["A", "E"], [1, 1, 1, 1], [[0,1],[0,1]])
a = p.multiply(asia, tbc)

b = p.createTable(["S", "B", "E"], [1, 1, 1, 1, 1, 1, 1, 1], [[0,1],[0,1],[0,1]])
b = p.multiply(smoker, bronchitis)

c = p.createTable(["S", "L", "E"], [1, 1, 1, 1, 1, 1, 1, 1], [[0,1],[0,1],[0,1]])
c = p.multiply(c, cancer)

d = p.createTable(["T", "L", "E"], [1, 1, 1, 1, 1, 1, 1, 1], [[0,1],[0,1],[0,1]])
d = p.multiply(d, tbcOrCancer)

e = p.createTable(["B", "E", "D"], [1, 1, 1, 1, 1, 1, 1, 1], [[0,1],[0,1],[0,1]])
e = p.multiply(e, dyspnoea)

f = p.createTable(["E", "X"], [1, 1, 1, 1], [[0,1],[0,1]])
f = p.multiply(f, xray)
"""
Metto in vita i nodi e gli assegno le tabelle.
"""
node1 = {'table': b, 'neighbours': [], 'separators': []}
node2 = {'table': c, 'neighbours': [], 'separators': []}
node3 = {'table': e, 'neighbours': [], 'separators': []}
node4 = {'table': d, 'neighbours': [], 'separators': []}
node5 = {'table': f, 'neighbours': [], 'separators': []}
node6 = {'table': a, 'neighbours': [], 'separators': []}
"""
Imposto le adiacenze tra nodi.
"""
node1['neighbours'].append(node2)
node1['neighbours'].append(node3)

node2['neighbours'].append(node1)
node2['neighbours'].append(node4)

node3['neighbours'].append(node1)
node3['neighbours'].append(node5)

node4['neighbours'].append(node2)
node4['neighbours'].append(node6)

node5['neighbours'].append(node3)

node6['neighbours'].append(node4)
"""
Creo le tabelle dei separatori.
"""
g = p.createTable(["S", "E"], [1, 1, 1, 1], [[0,1],[0,1]])
h = p.createTable(["B", "E"], [1, 1, 1, 1], [[0,1],[0,1]])
i = p.createTable(["L", "E"], [1, 1, 1, 1], [[0,1],[0,1]])
j = p.createTable(["E"], [1, 1], [[0,1]])
k = p.createTable(["T"], [1, 1], [[0,1]])
"""
Metto in vita i separatori e gli assegno le tabelle.
"""
sep1 = {'name': 'stc', 'table': g}
sep2 = {'name': 'btc', 'table': h}
sep3 = {'name': 'ctc', 'table': i}
sep4 = {'name': 'tc', 'table': j}
sep5 = {'name': 't', 'table': k}
"""
Imposto le relazioni di adiacenza tra nodi e separatori.
"""
node1['separators'].append(sep1)
node1['separators'].append(sep2)

node2['separators'].append(sep1)
node2['separators'].append(sep3)

node3['separators'].append(sep2)
node3['separators'].append(sep4)

node4['separators'].append(sep3)
node4['separators'].append(sep5)

node5['separators'].append(sep4)

node6['separators'].append(sep5)
"""
Chiamo l'algoritmo di inferenza
"""
bn.inference(node1, [node1, node2, node3, node4, node5, node6], [sep1, sep2, sep3, sep4, sep5],{})