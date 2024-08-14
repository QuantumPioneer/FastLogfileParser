from fastlogfileparser.generic.postprocessing import (
    _str_to_float,
)


POSTPROCESSING_FUNCTIONS = {
    "area": _str_to_float,
    "volume": _str_to_float,
    "energy": _str_to_float,
}
