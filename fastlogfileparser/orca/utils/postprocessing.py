from fastlogfileparser.generic.postprocessing import (
    _charge_and_multiplicity,
    _columns_to_floats,
    _str_to_float,
    _unix_time_to_seconds,
)

POSTPROCESSING_FUNCTIONS = {
    # gaussian-based column converter expects more fields, we wrap it like this:
    "input_coordinates": lambda in_list: [i[0] for i in _columns_to_floats(in_list)],
    "run_time": _unix_time_to_seconds,
    "route_section": lambda in_list: in_list[0],
    "charge_and_multiplicity": _charge_and_multiplicity,
    "energy": _str_to_float,
}
