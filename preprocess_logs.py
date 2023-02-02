# make a bunch of symlinks to the files on superclloud

import os
import re
import glob

from tqdm import tqdm

RETRIEVAL_PATTERNS = {
    "gibbs": r" Sum of electronic and thermal Free Energies=\s+(-?\d+\.\d+)",
    "e0_zpe": r" Sum of electronic and zero-point Energies=\s+(-?\d+\.\d+)",
    "e0": r"HF=(-?\d+.\d+)",
    "zpe": r"ZeroPoint=(-?\d+.\d+)",
    "cpu_time": r" Job cpu time: \s+(\d+ days\s+\d+ hours\s+\d+ minutes\s+\d+\.?\d+ seconds)",
    "wall_time": r" Elapsed time: \s+(\d+ days\s+\d+ hours\s+\d+ minutes\s+\d+\.?\d+ seconds)",
    "num_atoms": r"Atom    (\d+) has atomic number  \d{1,3} and mass   \d+\.\d+\n Molecular mass:   \d+\.\d+ amu",
    "frequencies": r" Frequencies --\s+(-?\d+.\d+)\s+(-?\d+.\d+)\s+(-?\d+.\d+)",
    "std_forces": (
        r" Forces in standard orientation:\n"
        r" -------------------------------------------------------------------\n"
        r" Center     Atomic                   Forces \(Hartrees/Bohr\)\n"
        r" Number     Number              X              Y              Z\n"
        r" -------------------------------------------------------------------\n"
        r"([\s+\d+\s+\d+\s+-?\d+\.\d+\s+-?\d+\.\d+\s+-?\d+\.\d+]+)\n"
        r" -------------------------------------------------------------------"
    ),
    "std_xyz": (
        r"                         Standard orientation:                         \n"
        r" ---------------------------------------------------------------------\n"
        r" Center     Atomic      Atomic             Coordinates \(Angstroms\)\n"
        r" Number     Number       Type             X           Y           Z\n"
        r" ---------------------------------------------------------------------\n"
        r"([\s+\d+\s+\d+\s+\d+\s+-?\d+\.\d+\s+-?\d+\.\d+\s+-?\d+\.\d+]+)\n"
        r" ---------------------------------------------------------------------"
    ),
    "xyz": (
        r"                          Input orientation:                          \n"
        r" ---------------------------------------------------------------------\n"
        r" Center     Atomic      Atomic             Coordinates \(Angstroms\)\n"
        r" Number     Number       Type             X           Y           Z\n"
        r" ---------------------------------------------------------------------\n"
        r"([\s+\d+\s+\d+\s+\d+\s+-?\d+\.\d+\s+-?\d+\.\d+\s+-?\d+\.\d+]+)\n"
        r" ---------------------------------------------------------------------"
    ),
    "steps": r"Number of steps in this run=\s+(\d+) ",
}

COMPILED_PATTERNS = {
    pattern_name: re.compile(pattern)
    for (pattern_name, pattern) in RETRIEVAL_PATTERNS.items()
}


def _unix_time_to_seconds(intime):
    """Take '0 days  0 hours 20 minutes 45.6 seconds' formatted times and convert to seconds."""
    out_times = []
    for timestr in intime:
        tmp = timestr.split()
        out_times.append(
            float(tmp[0]) * 86400
            + float(tmp[2]) * 3600
            + float(tmp[4]) * 60
            + float(tmp[6])
        )
    return out_times


def _str_list_to_floats(l):
    return [float(i) for i in l]


def _num_atoms_reducer(l):
    return int(l[0])


def _columns_to_floats(l):
    """Converts the force and coordinate table into 3D array of floats.
    Axis 0 is the timesteps, axis 1 is the atoms, axis 2 is the columns"""
    out_l = []
    for step in l:
        out_l.append([_str_list_to_floats(line.split()) for line in step.splitlines()])
    return out_l


POSTPROCESSING_FUNCTIONS = {
    "cpu_time": _unix_time_to_seconds,
    "wall_time": _unix_time_to_seconds,
    "e0": _str_list_to_floats,
    "zpe": _str_list_to_floats,
    "e0_zpe": _str_list_to_floats,
    "gibbs": _str_list_to_floats,
    "num_atoms": _num_atoms_reducer,
    "frequencies": lambda l: [_str_list_to_floats(list(i)) for i in l],
    "steps": _str_list_to_floats,
    "std_forces": _columns_to_floats,
    "std_xyz": _columns_to_floats,
    "xyz": _columns_to_floats,
}


def preprocess_logs(
    log_dir: str = "$HOME/semi-dft/data/screen",
    target_dir: str = "$HOME/semi-dft/data/dft",
    filename_fstring: str = "rxn_{:d}_oo.log",
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
        log_fname = os.path.join(log_dir, filename_fstring.format(rxn_num))
        target_fname = os.path.join(target_dir, filename_fstring.format(rxn_num))

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
                out_dict[rxn_num][pattern_name] = result

        # check the last line of the file to see if it converged
        # fast way to get to the last line thanks to:
        # https://stackoverflow.com/questions/46258499/how-to-read-the-last-line-of-a-file-in-python
        with open(target_fname, "rb") as file:
            file.seek(-2, os.SEEK_END)
            while file.read(1) != b"\n":
                file.seek(-2, os.SEEK_CUR)
            last_line = file.readline().decode()
            # ends with Normal termination ... or else did not converge
            # True if converged, False otherwise
            out_dict[rxn_num]["converged"] = last_line.split(" ")[1] == "Normal"

    if verbose > 1:
        import pprint

        pp = pprint.PrettyPrinter(depth=4)
        pp.pprint(out_dict)
    return out_dict


if __name__ == "__main__":
    preprocess_logs(verbose=2)
