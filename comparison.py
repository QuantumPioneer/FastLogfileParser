from time import perf_counter
import os

from ase.io.gaussian import read_gaussian_out
from cclib.parser import Gaussian
from fastlogfileparser.gaussian import fast_gaussian_logfile_parser as fglp


FNAME = "test/data/rxn_11.log"


def timeit(func):
    def wrapper_function(*args, **kwargs):
        print("Starting {:s}...".format(func.__name__))
        start = perf_counter()
        func(*args, **kwargs)
        stop = perf_counter()
        print("{:s} took {:.4f} seconds.\n".format(func.__name__, stop - start))

    return wrapper_function


@timeit
def test_fglp():
    job_1, job_2, job_3 = fglp(FNAME)
    print("Per-job free energy:", job_1["gibbs"], job_2["gibbs"], job_3["gibbs"])
    print("Total Energy (eV)", job_1["scf"][-1])


@timeit
def test_cclib():
    # cclib does not support reading from link jobs, so we have to split the logfile manually
    f_text = ""
    with open(FNAME, "r") as file:
        for line in file:
            f_text += line
    separate_files = f_text.split(" Entering Link")[1:]
    temp_fname = "temp.log"
    for i in range(3):
        with open(temp_fname, "w") as temp_file:
            temp_file.write(separate_files[i])
        p = Gaussian(temp_fname)
        cclib_result = p.parse()
        print("Free energy:", cclib_result.freeenergy)
    os.remove(temp_fname)


@timeit
def test_ase():
    with open(FNAME, "r") as file:
        res = read_gaussian_out(file)
        print("Total Energy (eV):", res.get_total_energy() * 0.03674930495120813)


test_fglp()
test_cclib()
test_ase()
