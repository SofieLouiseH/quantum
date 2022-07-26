from numpy import linalg
import networkx as nx
import scipy
from sklearn.cluster import KMeans


def convert_qubo_to_matrice(qubo):
    sorted_keys = sorted(qubo.keys())
    sorted_dict = {key: qubo[key] for key in sorted_keys}
    list_qubo = list(sorted_dict.values()) #durch anzahl der variablen teilen und unterlisten generieren
    list_sep_frequence = len(sorted_dict.keys())
    final_qubo = []
    row = []
    j = 1
    for i in range(list_sep_frequence):
       row.append(list_qubo[i])
       if (list_sep_frequence/j == j or i+1==list_sep_frequence):
           j = 0
           final_qubo.append(row)
           row = []
       j = j+1
    return final_qubo

def analysis(matrice):
    determinant = linalg.det(matrice)
    rank = linalg.matrix_rank(matrice)
    matrice = nx.Graph(matrice)
    connectivity = nx.algebraic_connectivity(matrice) #format überarbeiten
    print(determinant,rank)

def prune_qubo(matrice):
    pruned_qubo = scipy.spare.csr_matrix.prune(matrice)
    return(pruned_qubo)

def convert_allQubos_to_clusData(qubos):
    #abhängig von convert q to m
    x = 2

def cluster_kmeans(matrices):
     #https://stackoverflow.com/questions/20933788/k-means-clustering-on-matrices-instead-of-data
     #https://towardsdatascience.com/k-means-clustering-with-scikit-learn-6b47a369a83c
    clustering = KMeans(n_clusters=3, init='random',
    n_init=10, max_iter=300,
    tol=1e-04, random_state=0)
    clusters = clustering.fit()

#statistische Auswertung - Abweichung vom durchschnittlichen Ergebnis, Qualitätsdifferenz prozentual zu Tabusearch
#generell will man andere QPUs oder andere Solver noch vergleichen / Chimera as top of everything

#https://arxiv.org/pdf/2110.08325.pdf

#zeilen und zeilen sowie spalten und spalten tauschbar, nuller quadrate so also zwischen jeden variablen in der matrix aussen erreichbar
#unabhängige variablen erlauben mehr variablen