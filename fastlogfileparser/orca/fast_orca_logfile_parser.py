# fast_orca_logfile_parser.py
# a single function meant to retrieve data from orca logfiles quickly,
# using exclusively regular expressions and reading the file only once.
import re
import warnings
from collections import namedtuple

from .utils.regexes import COMPILED_PATTERNS, METADATA, DATA
from .utils.postprocessing import POSTPROCESSING_FUNCTIONS

METADATA_FIELDS = tuple(METADATA.keys())
DATA_FIELDS = tuple(DATA.keys())
ALL_FIELDS = DATA_FIELDS + METADATA_FIELDS


def fast_orca_logfile_parser(
    target_file: str,
    get: tuple = ALL_FIELDS,
    verbose: int = 0,
):
    """Parse Orca Logfile, but Fast-ly

    Args:
        target_file (str, optional): Logfile path.
        verbose (int, optional): 0 for silent, 1 for info, 2 for debug. Defaults to 0.

    Returns:
        dict: kvp of logfile contents
    """
    out_tuples = []
    # get the text out of the logfile
    with open(target_file, "r") as file:
        logfile_text = file.read()
        # find all the values we want
        out_dict = {}
        for pattern_name, compiled_pattern in COMPILED_PATTERNS.items():
            # skip fields not requested by user
            if pattern_name not in get:
                continue
            result = re.findall(compiled_pattern, logfile_text)
            if not result:
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
        out_tuples.append(namedtuple("job_result", out_dict.keys())(*out_dict.values()))

    # debug info
    if verbose > 2:
        import pprint

        pp = pprint.PrettyPrinter(depth=4)
        pp.pprint(out_dict)

    return (*out_tuples,)
