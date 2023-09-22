# fast_gaussian_logfile_parser.py
# a single function meant to retrieve data from gaussian logfiles quickly,
# using exclusively regular expressions and reading the file only once.
import re
import warnings
from collections import namedtuple

from .utils.regexes import COMPILED_PATTERNS
from .utils.preprocessing import crush_ginc_block, split_composite_job
from .utils.postprocessing import POSTPROCESSING_FUNCTIONS

FIELDS = COMPILED_PATTERNS.keys()


def fast_gaussian_logfile_parser(
    target_file: str,
    is_wavefunction_method: bool = False,
    verbose: int = 0,
):
    """Parse Gaussian Logfile, but Fast-ly

    Args:
        target_file (str, optional): Logfile path.
        is_wavefunction_method (bool, optional): Turn on to look for method-specific total energy for wavefunction methods. Defaults to False.
        verbose (int, optional): 0 for silent, 1 for info, 2 for debug. Defaults to 0.

    Returns:
        dict: kvp of logfile contents, one per job
    """
    out_tuples = []
    # get the text out of the logfile
    with open(target_file, "r") as file:
        crushed_text = crush_ginc_block(file)
        preprocessed_text_array = split_composite_job(crushed_text)
        # find all the values we want
        for logfile_text in preprocessed_text_array:
            out_dict = {}
            for pattern_name, compiled_pattern in COMPILED_PATTERNS.items():
                if pattern_name == "wavefunction_energy" and not is_wavefunction_method:
                    continue
                result = re.findall(compiled_pattern, logfile_text)
                if not result and not pattern_name == "normal_termination":
                    result = None
                else:
                    # post-process where required
                    requires_postprocessing = POSTPROCESSING_FUNCTIONS.get(
                        pattern_name, False
                    )
                    if requires_postprocessing:
                        try:
                            result = requires_postprocessing(result)
                        except Exception as e:
                            if verbose > 0:
                                warnings.warn(
                                    "Failed postprocessing for {:s} on file {:s}, error: {:s}".format(
                                        pattern_name,
                                        file,
                                        str(e),
                                    )
                                )
                            result = None
                out_dict[pattern_name] = result
            out_dict["number_of_atoms"] = len(out_dict["std_xyz"][0])
            # remove 1 for the initial geometry printout
            out_dict["number_of_optimization_steps"] = len(out_dict["std_xyz"]) - 1
            out_tuples.append(namedtuple('x', out_dict.keys())(*out_dict.values()))

    # debug info
    if verbose > 2:
        import pprint

        pp = pprint.PrettyPrinter(depth=4)
        pp.pprint(out_dict)

    return (*out_tuples,)
