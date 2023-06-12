import time

from tqdm import tqdm

from fast_gaussian_logfile_parser import fast_gaussian_logfile_parser

start = time.perf_counter()
for file in tqdm(("data/rxn_11.log", "data/rxn_233.log", "data/rxn_236.log")):
    out = fast_gaussian_logfile_parser(file)
end = time.perf_counter()
print(end - start)
