# fast_orca_logfile_parser.py
# a single function meant to retrieve data from orca logfiles quickly,
# using exclusively regular expressions and reading the file only once.
from fastlogfileparser.generic.iter_patterns import iter_patterns
from .utils.postprocessing import POSTPROCESSING_FUNCTIONS
from .utils.regexes import COMPILED_PATTERNS, DATA, METADATA

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
        get (tuple[str]): Fields to retrieve.
        verbose (int, optional): 0 for silent, 1 for info, 2 for debug. Defaults to 0.

    Returns:
        dict: kvp of logfile contents
    """
    with open(target_file, "r") as file:
        logfile_text = file.read()
    # orca does not support composite jobs, but for consistency with other parsers we return as a tuple
    return (iter_patterns(logfile_text, target_file, COMPILED_PATTERNS, get, POSTPROCESSING_FUNCTIONS, verbose=verbose),)
