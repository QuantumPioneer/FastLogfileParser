# fast_gaussian_logfile_parser.py
# a single function meant to retrieve data from gaussian logfiles quickly,
# using exclusively regular expressions and reading the file only once.
import os
import re

from utils.regexes import COMPILED_PATTERNS
from utils.preprocessing import crush_ginc_block
from utils.postprocessing import POSTPROCESSING_FUNCTIONS


def fast_gaussian_logfile_parser(
    target_file: str,
    status_only: bool = False,
    verbose: int = 1,
):
    """Parse Gaussian Logfile, but Fast-ly

    Args:
        target_file (str, optional): Logfile path.
        status_only (bool, optional): Retrieve ONLY the status of the job, but nearly instantly. Defaults to False.
        verbose (int, optional): 0 for silent, 1 for info, 2 for debug. Defaults to 1.

    Returns:
        dict: kvp of logfile contents
    """
    out_dict = {}

    # shortcut if only the status is needed
    if status_only:
        try:
            # check the last line of the file to see if it converged
            # fast way to get to the last line thanks to:
            # https://stackoverflow.com/questions/46258499/how-to-read-the-last-line-of-a-file-in-python
            with open(target_file, "rb") as file:
                file.seek(-2, os.SEEK_END)
                while file.read(1) != b"\n":
                    file.seek(-2, os.SEEK_CUR)
                last_line = file.readline().decode()
                # ends with Normal termination ... or else did not converge
                # True if converged, False otherwise
                out_dict["status"] = last_line.split(" ")[1] == "Normal"
        except:
            out_dict["status"] = "System Error"
        return out_dict

    # get the text out of the logfile
    with open(target_file, "r") as file:
        logfile_text = crush_ginc_block(file)
        # find all the values we want
        for pattern_name, compiled_pattern in COMPILED_PATTERNS.items():
            result = re.findall(compiled_pattern, logfile_text)
            # post-process where required
            requires_postprocessing = POSTPROCESSING_FUNCTIONS.get(pattern_name, False)
            if requires_postprocessing:
                try:
                    result = requires_postprocessing(result)
                except:
                    result = None
            out_dict[pattern_name] = result

    # add the number of atoms
    out_dict["number_of_atoms"] = len(out_dict["std_xyz"][0])

    # debug info
    if verbose > 1:
        import pprint

        pp = pprint.PrettyPrinter(depth=4)
        pp.pprint(out_dict)

    return out_dict
