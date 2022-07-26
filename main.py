from src import qubo_converter_analysis, qubo_generator

#qubo_converter_analysis.convert_qubo_to_matrice(example_qubo)

#config = Config(configpath=r"C:\Users\SofieLouise\PycharmProjects\quantum\config.json")
#connection = config.create_connection()


size = 40
qubo = qubo_generator.rand(size, "BINARY", low=-5, high=5)
qubo = qubo_converter_analysis.convert_qubo_to_matrice(qubo)
qubo_converter_analysis.analysis(qubo)


"""answer_tabu = Qubo(config, qubo).with_platform("tabu").solve(5)
answer_tabu.print_solutions_nice()"""
"""problem = Qubo(config, qubo).with_platform("dwave").with_solver("DW_2000Q_6")
problem.find_chimera_embedding()
problem.draw_chimera_embedding("embedding.pdf")"""

"""answer_quant = problem.solve(1)
answer_quant.print_solutions_nice()"""



#stand 20.7: 50 anneals, -5/5 range, QuantenComp 50 schlechtere Ergebnisse als Tabu
