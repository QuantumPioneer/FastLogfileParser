import re
import warnings
from collections import namedtuple


def iter_patterns(logfile_text, fname, compiled_patterns_dict, requested_patterns, postprocessing_funcs, verbose=0, return_as="tuple"):
    requested = {k: v for k, v in compiled_patterns_dict.items() if k in requested_patterns}
    # find all the values we want
    out_dict = {}
    for pattern_name, compiled_pattern in requested.items():
        result = re.findall(compiled_pattern, logfile_text)
        if not result:
            result = None
        else:
            # post-process where required
            requires_postprocessing = postprocessing_funcs.get(pattern_name, False)
            if requires_postprocessing:
                try:
                    result = requires_postprocessing(result)
                except Exception as e:
                    if verbose > 0:
                        warnings.warn(f"Failed postprocessing for {pattern_name} on file {fname}, error: {str(e)}")
                    result = None
        out_dict[pattern_name] = result

    # debug info
    if verbose > 2:
        import pprint

        pp = pprint.PrettyPrinter(depth=4)
        pp.pprint(out_dict)

    if return_as == "tuple":
        return namedtuple("job_result", out_dict.keys())(*out_dict.values())
    elif return_as == "dict":
        return out_dict
    else:
        raise RuntimeError(f"Unknown return type {return_as=} (must be 'dict' or 'tuple').")
