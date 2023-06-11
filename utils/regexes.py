import re

RETRIEVAL_PATTERNS = {
    "gibbs": r" Sum of electronic and thermal Free Energies=\s+(-?\d+\.\d+)",
    "e0_zpe": r" Sum of electronic and zero-point Energies=\s+(-?\d+\.\d+)",
    "e0": r"HF=(-?\d+.\d+)",  # they can optionally be a newline and space between each symbol including the digits, this is why sig figs are getting cut off
    "zpe": r"ZeroPoint=(-?\d+.\d+)",  # they can optionally be a newline and space between each symbol including the digits
    "cpu_time": r" Job cpu time: \s+(\d+ days\s+\d+ hours\s+\d+ minutes\s+\d+\.?\d+ seconds)",
    "wall_time": r" Elapsed time: \s+(\d+ days\s+\d+ hours\s+\d+ minutes\s+\d+\.?\d+ seconds)",  # also get it for the DFT simulation
    "num_atoms": r"Atom    (\d+) has atomic number  \d{1,3} and mass   \d+\.\d+\n Molecular mass:   \d+\.\d+ amu",  # just use length of xyz coords instead, the thermochemistry is not always output
    "frequencies": r" Frequencies --\s+(-?\d+.\d+)\s+(-?\d+.\d+)\s+(-?\d+.\d+)",
    "std_forces": (
        r" Forces in standard orientation:\n"
        r" -------------------------------------------------------------------\n"
        r" Center     Atomic                   Forces \(Hartrees/Bohr\)\n"
        r" Number     Number              X              Y              Z\n"
        r" -------------------------------------------------------------------\n"
        r"([\s+\d+\s+\d+\s+-?\d+\.\d+\s+-?\d+\.\d+\s+-?\d+\.\d+]+)\n"
        r" -------------------------------------------------------------------"
    ),
    "std_xyz": (
        r"                         Standard orientation:                         \n"
        r" ---------------------------------------------------------------------\n"
        r" Center     Atomic      Atomic             Coordinates \(Angstroms\)\n"
        r" Number     Number       Type             X           Y           Z\n"
        r" ---------------------------------------------------------------------\n"
        r"([\s+\d+\s+\d+\s+\d+\s+-?\d+\.\d+\s+-?\d+\.\d+\s+-?\d+\.\d+]+)\n"
        r" ---------------------------------------------------------------------"
    ),
    "xyz": (
        r"                          Input orientation:                          \n"
        r" ---------------------------------------------------------------------\n"
        r" Center     Atomic      Atomic             Coordinates \(Angstroms\)\n"
        r" Number     Number       Type             X           Y           Z\n"
        r" ---------------------------------------------------------------------\n"
        r"([\s+\d+\s+\d+\s+\d+\s+-?\d+\.\d+\s+-?\d+\.\d+\s+-?\d+\.\d+]+)\n"
        r" ---------------------------------------------------------------------"
    ),
    "steps": r"Number of steps in this run=\s+(\d+) ",
}

COMPILED_PATTERNS = {
    pattern_name: re.compile(pattern)
    for (pattern_name, pattern) in RETRIEVAL_PATTERNS.items()
}
