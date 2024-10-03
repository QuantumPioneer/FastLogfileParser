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
    "mulliken_charges_summed": (
        r" Mulliken charges and spin densities with hydrogens summed into heavy atoms:\n"
        r"               1          2\n"
        r"((?:\s+\d+\s+[a-zA-Z]{1,3}\s+-?\d+\.\d+\s+-?\d+\.\d+)+)\n"
        r" APT charges:"
    ),
    "charge_and_multiplicity": r" Charge = {1,2}(-?\d) Multiplicity = (\d)",
    "dipole_au": r"   Tot        (-?\d+.\d+)D([\+|-]\d+)",
    "iso_polarizability_au": r"   iso        (-?\d+.\d+)D([\+|-]\d+)",
    "aniso_polarizability_au": r"   aniso      (-?\d+.\d+)D([\+|-]\d+)",
    "dipole_moment_debye": r"    X=\s+(-?\d+.\d+)\s+Y=\s+(-?\d+.\d+)\s+Z=\s+(-?\d+.\d+)",
    "homo_lumo_gap": (
        r" Alpha  occ\. eigenvalues --[\s+-?\d+.\d+]+?\s+(-?\d+.\d+)\n"
        r" Alpha virt\. eigenvalues --\s+(-?\d+.\d+)"
    ),
    "beta_homo_lumo_gap": (
        r"  Beta  occ\. eigenvalues --[\s+-?\d+.\d+]+?\s+(-?\d+.\d+)\n"
        r"  Beta virt\. eigenvalues --\s+(-?\d+.\d+)"
    ),
    "nmr_shielding": r"\s+(\d+)\s+..?\s+Isotropic =\s+(\d+.\d+)\s+Anisotropy =\s+(\d+.\d+)"
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
COMPILED_PATTERNS = {pattern_name: re.compile(pattern) for (pattern_name, pattern) in RETRIEVAL_PATTERNS.items()}
