import qubo_generator
import qubo_converter_analysis
import solver
from uqo.client.config import Config
import pandas as pd
import time
import qubo_var

config = Config(configpath=r"C:\Users\SofieLouise\PycharmProjects\quantum\config.json")
connection = config.create_connection()

def execution(sparedegree, scale):
    for i in range(3):  # qubos
        runs = 5
        size = 146  # 145 sicher - 0.97 according to qpu aktuell on leap
        anneals = 30
        #qubo = qubo_generator.uniform(size, "BINARY", low=-1000000, high=1000000)
        #qubo = qubo_generator.rand(size, "BINARY", low=-1000000, high=1000000)
        qubo = qubo_generator.uniform_spare40(size, "BINARY", low=-1000000, high=1000000)
        #qubo = qubo_generator.rand_spare40(size, "BINARY", low=-1000000, high=1000000)
        #qubo = qubo_var.qubo3
        #qubo = qubo_generator.normal(size, "BINARY", low=sparedegree, high=scale) #float, 0%, sa 10, normal
        #print(qubo)
        qubo_name = time.clock()
        qubo_matr = qubo_converter_analysis.convert_qubo_to_matrice(qubo)
        det, rank = 0, 146 #qubo_converter_analysis.analysis_linAlg(qubo_matr)
        variance_mat = qubo_converter_analysis.analysis_Stat(qubo_matr)

        sim_annealing = solver.sim_annealingDWAVE(qubo, 20)  # no Runtime required
        optimum = round(sim_annealing[0], 2)
        solutionsq, solutionst, occurrencesq, occurrencest, energyq, energyt, timeQ, timeT, timing = [], [], [], [], [], [], [], [], []
        timet, timeq = 0, 0

        for j in range(runs):
            if j == 0:
                print(1)
                tabu = solver.tabu(config, qubo, anneals)
                print(connection.show_quota())
                qsolve = solver.qsolve(config, qubo, anneals)
                print(connection.show_quota())
                [energyq.append(i) for i in qsolve[1]]
                [energyt.append(i) for i in tabu[1]]
                [occurrencest.append(i) for i in tabu[2]]
                [occurrencesq.append(i) for i in qsolve[2]]
                timet = timet + tabu[3]
                timeq = timeq + qsolve[3]
                timing.append(qsolve[4])
                timeQ.append(qsolve[3])
                timeT.append(tabu[3])

            if j != 0 and round(min(energyt), 2) != optimum:
                tabu = solver.tabu(config, qubo, anneals)
                timet = timet + tabu[3]
                timeQ.append(qsolve[3])
                timing.append(qsolve[4])
                [energyt.append(i) for i in tabu[1]]
                [occurrencest.append(i) for i in tabu[2]]

            if j != 0 and round(min(energyq), 2) != optimum:
                print(connection.show_quota())
                qsolve = solver.qsolve(config, qubo, anneals)
                print(connection.show_quota())
                timeq = timeq + qsolve[3]
                timeQ.append(qsolve[3])
                timing.append(qsolve[4])
                [energyq.append(i) for i in qsolve[1]]
                [occurrencesq.append(i) for i in qsolve[2]]

        tmin = min(energyt)
        qmin = min(energyq)
        variance_resQ = qubo_converter_analysis.varianceRes(energyq, occurrencesq)  # wird über alle runs genommen

        parameters = {"Size": size, "Solution_optimal": sim_annealing[0], "Rank": rank, "optQ": qmin, "OptSingleQ": energyq.__str__(), "optT": tmin,
                      "Determinant": round(det, 2), "VarianceMat": round(variance_mat, 4), "TimeT": timet,
                      "TimeSingleT": timeT.__str__(), "TimeQ": timeq, "TimeSingleQ": timeQ.__str__(),
                      "TimeOpt": sim_annealing[1], "variance_resQ": round(variance_resQ, 4), "Qubo_format": qubo_name.__str__(),
                      "TimingData": timing.__str__()}

        parameters2 = {"Qubo_format": qubo_name.__str__(),
                       "QEnergiesOcc_all": sorted(list(zip(energyq, occurrencesq)), key=lambda x: x[0]).__str__(),
                       "TEnergiesOcc_all": sorted(list(zip(energyt, occurrencest)), key=lambda x: x[0]).__str__()}

        #parameters3 = {"Qubo": qubo.__str__()} #für HPT!!

        table = pd.DataFrame(parameters, index=[0])
        table.to_csv('all_params.csv', mode='a', index=True, header=False)

        table2 = pd.DataFrame(parameters2, index=[0])
        table2.to_csv('all_params2.csv', mode='a', index=True, header=False)

        #table3 = pd.DataFrame(parameters3, index=[0])
        #table3.to_csv('HPT_matrix3.csv', mode='a', index=True, header=False)

