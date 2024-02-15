import re

# input coordinates
#  final single point energy
#  total run time
#  title card section (level of theory, etc.) form the input file section
#  charge and multiplicity (also in the input file section)

DATA = {
    "input_coordinates": r"\|[ \d]{3}>.\w{1,2}[ ]{2,3}([\s+\d+\s+\d+\s+-?\d+\.\d+\s+-?\d+\.\d+\s+-?\d+\.\d+]+)\n",
    "energy": r"FINAL SINGLE POINT ENERGY\s+(-?\d+.\d+)\n",
    "charge_and_multiplicity": r"...> \* xyz (-?\d) (\d)\n",
}

METADATA = {
    "route_section": r"  1> !(.+)\n",
    # ignores milliseconds (2 min + 100 ms ~ 2 min)
    "run_time": r"TOTAL RUN TIME:\s+(\d+ days\s+\d+ hours\s+\d+ minutes\s+\d+ seconds)",
}

RETRIEVAL_PATTERNS = {**DATA, **METADATA}

COMPILED_PATTERNS = {pattern_name: re.compile(pattern) for (pattern_name, pattern) in RETRIEVAL_PATTERNS.items()}
