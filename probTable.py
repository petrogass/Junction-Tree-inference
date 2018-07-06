import pandas as pd
	
def createTable(vars, probs, domains):
	"""
	Questo metodo mette in vita una tabella delle probabilità, sottoforma di dataframe di pandas.
	Parametri:
		vars: lista di stringhe, nome delle variabili nella tavola
		probs: lista di float, valori associati alle realizzazioni delle variabili prese nell'ordine da 00...0 a 11..1(caso binario)
		domains: lista di liste, ogni lista indica il dominio della variabile associata presa nell'ordine
	"""
	table = pd.DataFrame()
	realizationCount = len(probs)
	varCount = len(vars)
	k = 1
	for i in range(varCount - 1, -1, -1):
		varDomain = domains[i]
		domainCount = len(varDomain)
		col = []
		for j in range(0, domainCount):
			col = col + [varDomain[j]] * k
		table[vars[i]] = col * int(realizationCount / (k * domainCount))
		k = k * domainCount
	table['probs'] = probs
	return table
	
def observe(table, obsVar, obsVal):
	"""
	Questo metodo introduce evidenza in una data tabella ponendo a zero le probabilità delle realizzazioni non coerenti con quanto osservato.
	Parametri:
		table: un dataframe creato con createTable()
		obsVar: una stringa, nome della variabile/della colonna
		obsVal: il valore osservato per la variabile, dello stesso tipo dei valori nel dominio della variabile	
	"""
	for i in range(0, len(table)):
		if table.loc[table.index[i], obsVar] != obsVal:
			table.loc[table.index[i], 'probs'] = 0
	return table 

def marginalize(table, vars):
	"""
	Questo metodo svolge l'azione di marginalizzazione su una tabella di probabilità.
	Parametri:
		table: un dataframe creato con createTable()
		vars: lista di stringhe, variabili da non marginalizzare	
	"""
	for column in table.columns:
		if column not in vars + ["probs"]:
			table = table.drop(column, axis=1)
	table['probs'] = table.groupby(vars)['probs'].transform('sum')
	table.drop_duplicates(inplace=True)
	return table
	
def multiply(table1, table2):
	"""
	Questo metodo moltiplica due tabelle di probabilità.
	Parametri:
		table1: un dataframe creato con createTable()
		table2: un dataframe creato con createTable()	
	"""
	columns = set(table1.columns).union(set(table2.columns)).difference(set(["probs"]))
	sharedColumns = list(set(table1.columns).intersection(set(table2.columns)).difference(set(["probs"])))
	reducedCols1 = table1.columns.difference(['probs'])		
	if not sharedColumns:
		table1['tmp'] = 1
		table2['tmp'] = 1
		reducedCols2 = table2.columns.difference(['probs'])
		table = pd.merge(table1, table2[reducedCols2], how='inner', on=['tmp'])		
	else:
		reducedCols2 = table2.columns.difference(['probs'])
		table = pd.merge(table1, table2[reducedCols2], how='inner', on=sharedColumns)
	table.sort_index(axis = 1, inplace = True)
	for i in range(0, len(table)):
		for j in range(0, len(table1)):
			found = False
			for k in range(0, len(table2)):				
				if table1[reducedCols1].iloc[j].equals(table[reducedCols1].iloc[i]) & table2[reducedCols2].iloc[k].equals(table[reducedCols2].iloc[i]):
					table.loc[table.index[i], 'probs'] = table1['probs'].iloc[j] * table2['probs'].iloc[k]
					found = True
					break				
			if found:
				break
	if 'tmp' in table:
		table.drop(['tmp'], axis=1, inplace = True)
		table1.drop(['tmp'], axis=1, inplace = True)
		table2.drop(['tmp'], axis=1, inplace = True)	
	return table
					
def divide(table1, table2):
	"""
	Questo metodo divide due tabelle di probabilità.
	Parametri:
		table1: un dataframe creato con createTable(), dividendo
		table2: un dataframe creato con createTable(), divisore	
	""" 
	columns = set(table1.columns).union(set(table2.columns)).difference(set(["probs"]))
	sharedColumns = list(set(table1.columns).intersection(set(table2.columns)).difference(set(["probs"])))
	reducedCols1 = table1.columns.difference(['probs'])		
	if not sharedColumns:
		table1['tmp'] = 1
		table2['tmp'] = 1
		reducedCols2 = table2.columns.difference(['probs'])
		table = pd.merge(table1, table2[reducedCols2], how='inner', on=['tmp'])		
	else:
		reducedCols2 = table2.columns.difference(['probs'])
		table = pd.merge(table1, table2[reducedCols2], how='inner', on=sharedColumns)
	table.sort_index(axis = 1, inplace = True)
	for i in range(0, len(table)):
		for j in range(0, len(table1)):
			found = False
			for k in range(0, len(table2)):
				if table1[reducedCols1].iloc[j].equals(table[reducedCols1].iloc[i]) & table2[reducedCols2].iloc[k].equals(table[reducedCols2].iloc[i]):
					if table1['probs'].iloc[j] == 0 and table2['probs'].iloc[k] == 0:
						table.loc[table.index[i], 'probs'] = 0
					else:
						table.loc[table.index[i], 'probs'] = table1['probs'].iloc[j] / table2['probs'].iloc[k]
					found = True
					break
			if found:
				break
	if 'tmp' in table:
		table.drop(['tmp'], axis=1, inplace = True)
		table1.drop(['tmp'], axis=1, inplace = True)
		table2.drop(['tmp'], axis=1, inplace = True)	
	return table