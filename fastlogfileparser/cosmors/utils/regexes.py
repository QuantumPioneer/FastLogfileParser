import re

DATA = {
    "area": r"  area=\s+(-?\d+\.\d+)",
    "volume": r"  volume=\s+(-?\d+\.\d+)",
    "energy": r"  Total energy \+ OC corr\. \[a\.u\.\] =\s+(-?\d+\.\d+)",
}

METADATA = {}

RETRIEVAL_PATTERNS = {**DATA, **METADATA}
COMPILED_PATTERNS = {pattern_name: re.compile(pattern) for (pattern_name, pattern) in RETRIEVAL_PATTERNS.items()}
