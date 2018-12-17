import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
import pyodbc
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib.pyplot import figure
import dateparser as dp
import datetime

#figure(num=None, figsize=(19, 6), dpi=80, facecolor='w', edgecolor='k')

def queryingByDate(table, lastaccess):
    date = dp.parse(str(lastaccess))
    end_date = date + datetime.timedelta(days=7)
    query = """
    SELECT *
    FROM [MiningShareITS].[dbo].[""" + table + """]
    where lastaccessdatetime >= '""" + str(date) + """' and lastaccessdatetime <= '""" + str(end_date) + """'
    """
    return query

def datapreprocessingByDate(table):
    query = """SELECT top 1000 CAST(lastaccessdatetime as DATE) as lastaccessdatetime
    FROM [MiningShareITS].[dbo].[""" + table + """]
    GROUP BY CAST(lastaccessdatetime AS DATE) order by lastaccessdatetime asc """
    cnxn = pyodbc.connect(
        'DRIVER={ODBC Driver 13 for SQL Server};SERVER=DESKTOP-VGNG6LG;DATABASE=MiningShareITS;Trusted_Connection=yes;')
    cursor = cnxn.cursor()
    cursor.execute("use MiningShareITS;")
    cursor.execute(query)
    rows = cursor.fetchall()
    listTransactions = []
    for row in rows:
        lastaccess = row.lastaccessdatetime
        datarows = cursor.execute(queryingByDate(table, lastaccess))
        transaction = []
        for datarow in datarows:
            transaction.append(datarow.Matakuliah)
        listTransactions.append(transaction)
        transaction = []

    cnxn.close()
    return listTransactions

def queryingByMahasiswa(table, user, semester, tahun):
    user = user.replace("'", "")
    if semester == 1 :
        query = """
            SELECT [Matakuliah]
            FROM [MiningShareITS].[dbo].[""" + table + """]
            where [Mahasiswa] like '""" + user + """' and MONTH(lastaccessdatetime) <= 6 and YEAR(lastaccessdatetime) = """+str(tahun)+"""
            """

    else:
        query = """
              SELECT [Matakuliah]
              FROM [MiningShareITS].[dbo].[""" + table + """]
              where [Mahasiswa] like '""" + user + """' and MONTH(lastaccessdatetime) > 6 and YEAR(lastaccessdatetime) = """ + str(tahun) + """
              """
    return query


def queryMahasiswaBySemester(table, semester, tahun):
    if semester == 1 :
        query = """SELECT distinct [Mahasiswa]
            FROM [MiningShareITS].[dbo].[MatakuliahITSNamaMahasiswaAksesMKTerakhir] where MONTH(lastaccessdatetime) <= 6 and YEAR(lastaccessdatetime) = """+str(tahun)
    else:
        query = """SELECT distinct [Mahasiswa]
            FROM [MiningShareITS].[dbo].[MatakuliahITSNamaMahasiswaAksesMKTerakhir] where MONTH(lastaccessdatetime) > 6 and YEAR(lastaccessdatetime) = """+str(tahun)
    cnxn = pyodbc.connect(
        'DRIVER={ODBC Driver 13 for SQL Server};SERVER=DESKTOP-VGNG6LG;DATABASE=MiningShareITS;Trusted_Connection=yes;')
    cursor = cnxn.cursor()
    cursor.execute("use MiningShareITS;")
    cursor.execute(query)
    rows = cursor.fetchall()

    print("Jumlah data = "+str(len(rows)))

    listTransactions = []

    for row in rows:
        user = row.Mahasiswa
        datarows = cursor.execute(queryingByMahasiswa(table, user, semester, tahun))
        transaction = []
        for datarow in datarows:
            transaction.append(datarow.Matakuliah)
        listTransactions.append(transaction)
        transaction = []

    cnxn.close()
    return listTransactions

def draw_graph(rules, rules_to_show):
    if rules_to_show > 10:
        rules_to_show = 10
    else:
        rules_to_show = rules_to_show

    import networkx as nx
    G1 = nx.DiGraph()

    color_map = []
    N = 50
    colors = np.random.rand(N)
    strs = []
    for i in range(rules_to_show):
        strs.append("R"+str(i))

    for i in range(rules_to_show):
        G1.add_nodes_from(["R" + str(i)])

        for a in rules.iloc[i][0]:
            G1.add_nodes_from([a])

            G1.add_edge(a, "R" + str(i), color=colors[i], weight=2)

        for c in rules.iloc[i][1]:
            G1.add_nodes_from([c])

            G1.add_edge("R" + str(i), c, color=colors[i], weight=2)

    for node in G1:
        found_a_string = False
        for item in strs:
            if node == item:
                found_a_string = True
        if found_a_string:
            color_map.append('yellow')
        else:
            color_map.append('green')

    edges = G1.edges()
    colors = [G1[u][v]['color'] for u, v in edges]
    weights = [G1[u][v]['weight'] for u, v in edges]

    pos = nx.spring_layout(G1, k=16, scale=1)
    nx.draw(G1, pos, edges=edges, node_color=color_map, edge_color=colors, width=weights, font_size=16,
            with_labels=False)

    for p in pos:  # raise text positions
        pos[p][1] += 0.07
    nx.draw_networkx_labels(G1, pos)
    plt.show()

def runAsociationRule(dataset, filename, supportThreshold, confidenceThreshold):
    te = TransactionEncoder()
    te_ary = te.fit(dataset).transform(dataset)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    resultApriori = apriori(df, min_support=supportThreshold, use_colnames=True)

    resultAsRule = association_rules(resultApriori, metric="confidence", min_threshold=confidenceThreshold)
    resultAsRule["antecedent_len"] = resultAsRule["antecedents"].apply(lambda x: len(x))

    #fitler
    resultAsRule = resultAsRule[(resultAsRule['antecedent_len'] >= 2)]

    #resultAsRule.to_csv(filename)
    print(resultAsRule)

    support = resultAsRule['support'].values
    confidence = resultAsRule['confidence'].values

    for i in range(len(support)):
        support[i] = support[i] + 0.0015 * (random.randint(1, 10) - 5)
        confidence[i] = confidence[i] + 0.0015 * (random.randint(1, 10) - 5)

    plt.scatter(support, confidence, alpha=0.5, marker="*")
    plt.xlabel('support')
    plt.ylabel('confidence')
    plt.show()

    draw_graph(resultAsRule, resultAsRule.shape[0])

    return resultAsRule

supportThreshold = 0.01
confidenceThreshold = 0.7
semester = 2
tahun = 2018
dataset = queryMahasiswaBySemester("MatakuliahITSNamaMahasiswaAksesMKTerakhir",semester,tahun)
result = runAsociationRule(dataset, "asrule_th"+str(tahun)+"_smt"+str(semester)+"_s"+str(supportThreshold)+"_c"+
                           str(confidenceThreshold)+".csv", supportThreshold, confidenceThreshold)
res = result[['antecedents', 'support']]
print(res)





