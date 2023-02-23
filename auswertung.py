import matplotlib.pyplot as plt
import numpy
import openpyxl
import ast
import pandas
import group

#group.py auswerten

excel_file = openpyxl.load_workbook('auswertungQC_haupt_vers2.xlsx')
excel_sheet = excel_file['Tabelle1']

count = 2
countY = 0
for i in range(136):
    x = excel_sheet['Y'+count.__str__()].value
    print(x)
    count = count+1
    if x == 1:
        y = group.timingData[countY][0]
    if x == 2:
        y = group.timingData[countY][0]+group.timingData[countY][1]
    if x == 3:
        y = group.timingData[countY][0]+group.timingData[countY][1]+group.timingData[countY][2]
    if x == 4:
        y = group.timingData[countY][0]+group.timingData[countY][1]+group.timingData[countY][2]+group.timingData[countY][3]
    if x == 5:
        y = group.timingData[countY][0]+group.timingData[countY][1]+group.timingData[countY][2]+group.timingData[countY][3]+group.timingData[countY][4]
    countY = countY+1

    print(x)
    p = {"x": y.__str__()}
    table = pandas.DataFrame(p, index=[0])
    table.to_csv('run.csv', mode='a', index=True, header=False)

#plt.plot(data1) #zeigt das zu beginn immer die besten ergebnisse alle abspeichern
#plt.show()

"""data1 = ast.literal_eval(excel_sheet['H57'].value)
data1_opt = ast.literal_eval(excel_sheet['F57'].value)
data2 = ast.literal_eval(excel_sheet['H58'].value)
data2_opt = ast.literal_eval(excel_sheet['F58'].value)
data3 = ast.literal_eval(excel_sheet['H59'].value)
data3_opt = ast.literal_eval(excel_sheet['F59'].value)
data4 = ast.literal_eval(excel_sheet['H60'].value)
data4_opt = ast.literal_eval(excel_sheet['F60'].value)
data5 = ast.literal_eval(excel_sheet['H61'].value)
data5_opt = ast.literal_eval(excel_sheet['F61'].value)

print(data1_opt,data2_opt,data3_opt,data4_opt,data5_opt)
a = [[i-data1_opt for i in data1],[i-data2_opt for i in data2],[i-data3_opt for i in data3],[i-data4_opt for i in data4],[i-data5_opt for i in data5]]

meanA = numpy.mean([i-data1_opt for i in data1])
print(meanA)
meanA = numpy.mean([i-data2_opt for i in data2])
print(meanA)
meanA = numpy.mean([i-data3_opt for i in data3])
print(meanA)
meanA = numpy.mean([i-data4_opt for i in data4])
print(meanA)
meanA = numpy.mean([i-data5_opt for i in data5])
print(meanA)
mean = numpy.mean(a)
print(mean)
b = (a[0]+a[1]+a[2]+a[3]+a[4]).__str__()
b = {"group": b}
a = [a[0],a[1],a[2],a[3],a[4],a[0]+a[1]+a[2]+a[3]+a[4]]

plt.boxplot(a)
plt.xticks([1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, "All"])
plt.show()"""

#table = pd.DataFrame(b, index=[0])
#table.to_csv('group.py', mode='a', index=True, header=False)

#wichtig! die gesamtliste aller 5 matritzen muss irgendwo gespeichert werden, csv maybe. um diese später zu nutzen für die hauptanalysen der eigenschaften

"""Für jede Gruppe durchschnittliche Abweichung des Ergebnis in 1. Zeit und
 2. Ergebniswert vergleichen. (Graphik und Tabelle)

Für HPT -> entscheidung für 20 statt 30 wegen zeitlicher Komponenten, auch noch in tabelle aufzeigen
einmal die übersichtsmatrix und dann noch drei mal jeweils die einzelnen matrizen zu einer graphik.
direkte vergleiche einfügen, reichen boxplots.


Comparing Tabu Search! Wie?

Zeit: QPU Access time = QPU Sampling time + QPU Programming Time, also vergleiche ich beides, und lasse mir die zeit den beiden
anderen Metaheuristiken mitgeben."""

