# fast_gaussian_logfile_parser.py
# a single function meant to retrieve data from gaussian logfiles quickly,
# using exclusively regular expressions and reading the file only once.
from collections import namedtuple

from fastlogfileparser.generic.iter_patterns import iter_patterns
from .utils.postprocessing import POSTPROCESSING_FUNCTIONS
from .utils.preprocessing import crush_ginc_block, split_composite_job
from .utils.regexes import COMPILED_PATTERNS, DATA, METADATA

METADATA_FIELDS = tuple(METADATA.keys())
DATA_FIELDS = tuple(DATA.keys())
ALL_FIELDS = DATA_FIELDS + METADATA_FIELDS


def fast_gaussian_logfile_parser(
    target_file: str,
    is_wavefunction_method: bool = False,
    include_intermediates: bool = True,
    get: tuple = ALL_FIELDS,
    verbose: int = 0,
):
    """Parse Gaussian Logfile, but Fast-ly

    Args:
        target_file (str, optional): Logfile path.
        is_wavefunction_method (bool, optional): Turn on to look for method-specific total energy for wavefunction methods. Defaults to False.
        include_intermediates (bool, optional): Return std_xyz, xyz, and forces for all steps. Defaults to True.
        get (tuple[str]): Fields to retrieve.
        verbose (int, optional): 0 for silent, 1 for info, 2 for debug. Defaults to 0.

    Returns:
        dict: kvp of logfile contents, one per job
    """
    # skip wavefunction regex for non-wavefunction methods
    if not is_wavefunction_method and "wavefunction_energy" in get:
        get = tuple(i for i in get if i != "wavefunction_energy")
    out_tuples = []
    # get the text out of the logfile
    with open(target_file, "r") as file:
        crushed_text = crush_ginc_block(file)
        preprocessed_text_array = split_composite_job(crushed_text)
        # find all the values we want
        for logfile_text in preprocessed_text_array:
            out_dict = iter_patterns(logfile_text, target_file, COMPILED_PATTERNS, get, POSTPROCESSING_FUNCTIONS, verbose=verbose, return_as="dict")
            # fields derived from other fields
            out_dict["normal_termination"] = out_dict["normal_termination"] is not None
            if "std_xyz" in get:
                out_dict["number_of_atoms"] = len(out_dict["std_xyz"][0])
                # remove 1 for the initial geometry printout
                out_dict["number_of_optimization_steps"] = len(out_dict["std_xyz"]) - 1
            if not include_intermediates:
                for arr in ("std_xyz", "xyz", "std_forces"):
                    if out_dict.get(arr, False):
                        out_dict[arr] = out_dict[arr][-1]
            out_tuples.append(namedtuple("job_result", out_dict.keys())(*out_dict.values()))
    return (*out_tuples,)
