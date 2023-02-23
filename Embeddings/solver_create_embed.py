from dwave import inspector
from uqo.Problem import Problem, Qubo
import time
import neal
import pandas as pd


def sim_annealingDWAVE(qubo, runs):
    sampler = neal.SimulatedAnnealingSampler()
    milliseconds_bef = int(round(time.time() * 1000))
    answer_opt = sampler.sample_qubo(qubo, num_reads=runs)
    milliseconds_aft = (int(round(time.time() * 1000))) - milliseconds_bef
    energies = []
    for energy, in answer_opt.data(fields=['energy'], sorted_by='energy'):
        energies.append(energy)
    minimum = min(energies)
    return minimum, milliseconds_aft


def sim_annealing(config, qubo):
    solver = "CPU"  # CPU or DAU, simulated annealing
    number_runs = 16
    parameters = {
        "number_iterations": 5,  # total number of iterations per run
        "temperature_start": 1000.0,  # start temperature as float value
        "temperature_end": 1.0,  # end temperature as float value or None
        "temperature_mode": 0,  # 0, 1, or 2 to define the cooling curve
        "temperature_decay": 0.001,  # decay per step if temperature_end is None
        "temperature_interval": 100,  # number of iterations keeping temperature constant
        "offset_increase_rate": 0.0,
        "solution_mode": "COMPLETE",
        "optimization_method": "annealing",  # annealing or parallel tempering are supported methods
        "number_replicas": 26,  # number of replicas for parallel tempering mode
        "annealer_version": 2,  # Digital Annealer version
        "guidance_config": {},
        "auto_tuning": 0,  # EXPERIMENTAL! options of automatic tuning the QUBO
        "bit_precision": 16,  # bit precision (DAU version 2)
        "connection_mode": "CMODE_ASYNC"  # Mode can be CMODE_ASYNC (default) or CMODE_SYNC
    }
    answer_opt = Qubo(config, qubo).with_platform("fujitsu").with_solver(solver).with_params(**parameters).solve(1)
    solutions_opt = answer_opt.solutions
    energies_opt = answer_opt.energies
    occurrences_opt = answer_opt.occurrences
    time_opt = answer_opt.sampleset.info["timing"]["qpu_access_time"]

    minimum = min(energies_opt)
    return solutions_opt, energies_opt, occurrences_opt, [time_opt], minimum


def tabu(config, qubo, runs):
    milliseconds_bef = int(round(time.time() * 1000))
    answer_tabu = Qubo(config, qubo).with_platform("tabu").solve(runs)
    milliseconds_aft = (int(round(time.time() * 1000))) - milliseconds_bef
    solutions_tabu = answer_tabu.solutions
    energies_tabu = answer_tabu.energies
    occurrences_tabu = answer_tabu.num_occurrences

    """    min = min(energies_tabu)
    minpos = energies_tabu.index(min(energies_tabu)) #gets first occurrence
    time_to_sol = (milliseconds_aft/runs) * (minpos+1) #Zeit bis zur besten Lösung"""

    return solutions_tabu, energies_tabu, occurrences_tabu, milliseconds_aft

    # https://support.dwavesys.com/hc/en-us/community/posts/360051504214-The-timing-feature-for-QBSolv


def qsolve(config, qubo, runs):
    x = (
        (0.0, 0.0),  # Start the anneal (time 0.0) at 0.0 (min)
        (5.0, 1.0)  # After 5µs, set the anneal setting to 100% (max)
    )
    # answer_quant = Qubo(config, qubo).with_platform("dwave").with_solver("Advantage_system4.1").with_params(annealing_time=5.0, anneal_schedule=x)
    answer_quant = Qubo(config, qubo).with_platform("dwave").with_solver("Advantage_system4.1").with_params()
    answer_quant.find_pegasus_embedding()
    answer_quant.draw_pegasus_embedding("embedding_pegasus" + time.clock().__str__() + ".pdf")
    print(answer_quant.embedding)

    a_dictionary = {"embeddings": answer_quant.embedding.__str__()}
    file = open("embeddings"+time.clock().__str__()+".txt", "w")
    str_dictionary = repr(a_dictionary)
    file.write("a_dictionary = " + str_dictionary + "\n")
    file.close()

    answer_quant = Qubo(config, qubo).with_platform("dwave").with_solver("Advantage_system4.1").with_params().solve(runs)
    solutions_quant = answer_quant.solutions
    energies_quant = answer_quant.energies
    occurrences_quant = answer_quant.num_occurrences
    # print(answer_quant.sampleset.info["timing"])
    time_quant = answer_quant.sampleset.info["timing"]["qpu_access_time"]  # qpu access time 0.01 sekunde
    timing = answer_quant.sampleset.info["timing"]["qpu_sampling_time"]
    # answer_quant.print_solutions_nice()
    """    min = min(energies_quant)
    minpos = energies_quant.index(min(energies_quant)) #gets first occurrence
    time_to_sol = (time_quant/runs) * (minpos+1) #Zeit bis zur besten Lösung"""

    return solutions_quant, energies_quant, occurrences_quant, time_quant, timing
