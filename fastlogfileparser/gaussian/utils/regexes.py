import re

DATA = {
    "gibbs": r" Sum of electronic and thermal Free Energies=\s+(-?\d+\.\d+)",  # Gibbs free energy at 298K, G(298K) = e0 + G_corr
    "e0_zpe": r" Sum of electronic and zero-point Energies=\s+(-?\d+\.\d+)",  # Gibbs free energy at 0K, G(0K) = e0 + ZPE
    "e0_h": r" Sum of electronic and thermal Enthalpies=\s+(-?\d+\.\d+)",  # Enthalpy at 298K, H(298K) = e0 + H_corr
    "hf": r"HF=(-?\d+.\d+)",  # equals e0 only for non-wave function methods e.g., DFT, semi-empirical
    "zpe_per_atom": r"ZeroPoint=(-?\d+.\d+)",  # per atom basis in Gaussian (Hartree/Particle)
    "wavefunction_energy": r"[CBSQB3|MP2|G4|G3|G2|CCSD|CCSD\(T\)]=(-?\d+.\d+)",
    "recovered_energy": r" Recovered energy=\s+(-?\d+.\d+)",
    "scf": r"(?<! >>>>>>>>>> Convergence criterion not met\.\n) SCF Done:  E\(.*\) =  -?(\d+\.\d+)",
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
    "frequency_modes": (
        r"  Atom  AN      X      Y      Z        X      Y      Z        X      Y      Z\n"
        r"([\s+\d+\s+\d\s+-?\d\.\d\d\s+-?\d\.\d\d\s+-?\d\.\d\d\s+-?\d\.\d\d\s+-?\d\.\d\d\s+-?\d\.\d\d\s+-?\d\.\d\d\s+-?\d\.\d\d\s+-?\d\.\d\d]+)\n"
        r"(?:\s+\d+\s+\d+\s+\d+)?\n"
    ),
    "charge_and_multiplicity": r" Charge = {1,2}(-?\d) Multiplicity = (\d)",
}

METADATA = {
    "route_section": r"#([A-Za-z\d\,=\(\)\-\/ \"\.\_]*)",
    "cpu_time": r" Job cpu time: \s+(\d+ days\s+\d+ hours\s+\d+ minutes\s+\d+\.?\d+ seconds)",
    "wall_time": r" Elapsed time: \s+(\d+ days\s+\d+ hours\s+\d+ minutes\s+\d+\.?\d+ seconds)",
    "max_steps": r"Number of steps in this run=\s+(\d+) ",
    "normal_termination": r" Normal termination ",
    "error_string": r" Error termination(.*)\n",
}

RETRIEVAL_PATTERNS = {**DATA, **METADATA}

# other options:
# homo-lumo gap, polarizability, dipole moment, mulliken and APT partial charges, occupancy


COMPILED_PATTERNS = {pattern_name: re.compile(pattern) for (pattern_name, pattern) in RETRIEVAL_PATTERNS.items()}
