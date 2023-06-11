# fast_gaussian_logfile_parser.py
# a single function meant to retrieve data from gaussian logfiles quickly,
# using exclusively regular expressions and reading the file only once.
#
# Use reaction id 11, 236, and 233 as test cases
import os
import re

from tqdm import tqdm

from utils.regexes import COMPILED_PATTERNS
from utils.postprocessing import POSTPROCESSING_FUNCTIONS


def fast_gaussian_logfile_parser(
    log_dir: str = "$HOME/semi-dft/data/screen",
    target_dir: str = "$HOME/semi-dft/data/dft",
    screen_filename_fstring: str = "rxn_{:d}_oo.log",
    dft_filename_fstring: str = "rxn_{:d}_oo.log",
    verbose: int = 1,
):
    out_dict = {}
    # verbose - control the amount of output - 0 only progress bars, 1 for some, 2 for a ton (debugging only, prints huge lists)
    # assume that the logfiles from initial screening and then dft are in nlp-dft/data/screen or dft
    log_dir = os.path.expandvars(log_dir)
    target_dir = os.path.expandvars(target_dir)

    # not all reactions were run in both, need to pair them up
    log_files = os.listdir(log_dir)
    target_files = os.listdir(target_dir)

    # files are formatted as rxn_###_name so we pull out ###
    target_files_rxn_numbers = set(int(i.split("_")[1]) for i in target_files)
    logfiles_rxn_numbers = set(int(i.split("_")[1]) for i in log_files)
    all_rxn_numbers = target_files_rxn_numbers.union(logfiles_rxn_numbers)

    # get only the rxns which passed the semi-emperical step and were then run in DFT
    paired_rxns = target_files_rxn_numbers.intersection(logfiles_rxn_numbers)

    if verbose:
        orphaned_logs = sorted(
            logfiles_rxn_numbers.symmetric_difference(
                target_files_rxn_numbers
            ).intersection(logfiles_rxn_numbers)
        )
        orphaned_targets = sorted(
            target_files_rxn_numbers.symmetric_difference(
                logfiles_rxn_numbers
            ).intersection(target_files_rxn_numbers)
        )
        if verbose == 1:
            print(
                "{:d} total screening/dft pairings were found.".format(len(paired_rxns))
            )
            print(
                "{:d} screening logfiles had no corresponding dft file".format(
                    len(orphaned_logs)
                )
            )
            print(
                "{:d} dft logfiles had no corresponding screening file".format(
                    len(orphaned_targets)
                )
            )
        elif verbose > 1:
            print(
                "The following screening logfiles had no corresponding dft file (total {:d} orphaned):".format(
                    len(orphaned_logs)
                ),
                orphaned_logs,
            )
            print(
                "The following dft logfiles had no corresponding screening file (total {:d} orphaned):".format(
                    len(orphaned_targets)
                ),
                orphaned_targets,
            )
            print(
                "Paired semi and dft files ({:d} total):".format(len(paired_rxns)),
                sorted(paired_rxns),
            )

    # loop through the paired files to determine if they converged and read the logs
    for idx, rxn_num in enumerate(tqdm(paired_rxns, desc="Parsing files...")):
        out_dict[rxn_num] = {}
        # open the files with no error handling, we know the files are there
        log_fname = os.path.join(log_dir, screen_filename_fstring.format(rxn_num))
        target_fname = os.path.join(target_dir, dft_filename_fstring.format(rxn_num))

        # get the text out of the logfile
        with open(log_fname, "r") as file:
            logfile_text = file.read()
            # find all the values we want
            for pattern_name, compiled_pattern in COMPILED_PATTERNS.items():
                result = re.findall(compiled_pattern, logfile_text)
                requries_postprocessing = POSTPROCESSING_FUNCTIONS.get(
                    pattern_name, False
                )
                if requries_postprocessing:
                    try:
                        result = requries_postprocessing(result)
                    except:
                        result = None
                if pattern_name == "std_xyz":
                    result = result[-1] if result else result
                out_dict[rxn_num][pattern_name] = result
        if rxn_num in paired_rxns:
            # check the last line of the file to see if it converged
            # fast way to get to the last line thanks to:
            # https://stackoverflow.com/questions/46258499/how-to-read-the-last-line-of-a-file-in-python
            try:
                with open(target_fname, "rb") as file:
                    file.seek(-2, os.SEEK_END)
                    while file.read(1) != b"\n":
                        file.seek(-2, os.SEEK_CUR)
                    last_line = file.readline().decode()
                    # ends with Normal termination ... or else did not converge
                    # True if converged, False otherwise
                    out_dict[rxn_num]["converged"] = last_line.split(" ")[1] == "Normal"
            except:
                out_dict[rxn_num]["converged"] = "System Error"

        else:
            out_dict[rxn_num]["converged"] = "No DFT"

    if verbose > 1:
        import pprint

        pp = pprint.PrettyPrinter(depth=4)
        pp.pprint(out_dict)
    return out_dict


if __name__ == "__main__":
    preprocess_logs(verbose=2)
