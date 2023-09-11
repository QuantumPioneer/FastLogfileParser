import re

# TODO: parse "SCF Done" equivalent energy for each step; for xtb, that is "Recovered energy=". This is the e0 for most methods.  
# TODO: need to post-process e0 for different level of theory
# TODO: 

RETRIEVAL_PATTERNS = {
    
    ## variables that only needs to be parsed once per file
    "gibbs": r" Sum of electronic and thermal Free Energies=\s+(-?\d+\.\d+)", # Gibbs free energy at 298K, G(298K) = e0 + G_corr  
    "e0_zpe": r" Sum of electronic and zero-point Energies=\s+(-?\d+\.\d+)", # Gibbs free energy at 0K, G(0K) = e0 + ZPE
    "e0_h": r" Sum of electronic and thermal Enthalpies=\s+(-?\d+\.\d+)", # Enthalpy at 298K, H(298K) = e0 + H_corr 
    "hf": r"HF=(-?\d+.\d+)", # equals e0 only for non-wave function methods e.g., DFT, semi-empirical
    "zpe": r"ZeroPoint=(-?\d+.\d+)",
    "cpu_time": r" Job cpu time: \s+(\d+ days\s+\d+ hours\s+\d+ minutes\s+\d+\.?\d+ seconds)",
    "wall_time": r" Elapsed time: \s+(\d+ days\s+\d+ hours\s+\d+ minutes\s+\d+\.?\d+ seconds)",  # also get it for the DFT simulation
    "frequencies": r" Frequencies --\s+(-?\d+.\d+)\s+(-?\d+.\d+)\s+(-?\d+.\d+)",
    # "num_atoms": r"Atom    (\d+) has atomic number  \d{1,3} and mass   \d+\.\d+\n Molecular mass:   \d+\.\d+ amu",
        
    ## variables that need to be parsed during each step 
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
