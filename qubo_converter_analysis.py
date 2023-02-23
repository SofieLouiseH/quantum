from numpy import linalg
import numpy
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

def analysis_linAlg(matrice):
    determinant = linalg.det(matrice)
    rank = linalg.matrix_rank(matrice)
    return determinant,rank

def analysis_Stat(energies):
    variance = numpy.var(energies) # before
    streuung = sum([sum(i) for i in zip(*energies)]) #now, der perfekte wert ist der mittelwert bei einer gleichverteilung den ich aus eingabe übernehme und vergleichen kann
    #print(streuung)
    return streuung # PRÜFEN

def varianceRes(energies,occurrences):
    res = [a*b for a,b in zip(energies,occurrences)]
    variance = numpy.var(res)
    return variance

def prune_qubo(matrice):
    pruned_qubo = scipy.spare.csr_matrix.prune(matrice)
    #tbc
    return(pruned_qubo)

def convert_allQubos_to_clusData(qubos):
    #whats qubos input
    clusMatrice = []
    for qubo in qubos:
        result = [qubo[key] for key in sorted(qubo.keys())]
        clusMatrice.append(result)

def cluster_kmeans(matrices):
    clustering = KMeans(n_clusters=3, init='random',
    n_init=10, max_iter=300,
    tol=1e-04, random_state=0).fit(matrices)
    print(clustering)

def time_to_sol(qtime, qmin, ttime, tmin, optmin):
    optmin = optmin*optmin
    tmin = tmin*tmin
    qmin = qmin*qmin

    if qmin == optmin == tmin:
        return qtime, ttime

    if qmin != optmin == tmin:
        diff = numpy.sqrt(abs(optmin - qmin))
        procent = numpy.sqrt(qmin)/100 * diff
        qtime = qtime + (qtime * procent)
        return qtime, ttime

    if qmin == optmin != tmin:
        diff = numpy.sqrt(abs(optmin - tmin))
        procent = numpy.sqrt(tmin)/ 100 * diff
        ttime = ttime + (ttime * procent)
        return qtime, ttime

    else:
        diff = numpy.sqrt(abs(optmin - qmin))
        procent = numpy.sqrt(qmin) / 100 * diff
        qtime = qtime + (qtime * procent)
        diff = numpy.sqrt(abs(optmin - tmin))
        procent = numpy.sqrt(tmin)/100 * diff
        ttime = ttime + (ttime * procent)
        return qtime, ttime


#statistische Auswertung - Abweichung vom durchschnittlichen Ergebnis, Qualitätsdifferenz prozentual zu Tabusearch - outvcome speichern und verarbeitung betrachten

#https://arxiv.org/pdf/2110.08325.pdf