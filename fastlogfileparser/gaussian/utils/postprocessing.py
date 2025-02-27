from fastlogfileparser.generic.postprocessing import (
    _charge_and_multiplicity,
    _columns_to_floats,
    _freq_modes,
    _str_list_to_floats,
    _str_to_float,
    _unix_time_to_seconds,
)


def _fortran_float_to_float(in_list):
    """Gaussian emits this:
    0.122109D+01 (printed in two places, but identical)
    which is parsed as this by regex:
    [('0.118671', '+01'), ('0.118671', '+01')]
    which we convert to this:
    1.18671
    """
    return _str_to_float(['e'.join(in_list[0])])


def _hl_gap(in_list):
    """Calculates HOMO-LUMO gap from the
    HOMO and LUMO energies

    Can be printed multiple times - take the first occurrence"""
    return float(in_list[0][1]) - float(in_list[0][0])


def _mulliken(in_list):
    out = []
    for i in in_list:
        inner_out = []
        for row in i.split(sep="\n"):
            atom_idx, _, mulliken_charge = row.split()
            inner_out.append([int(atom_idx), float(mulliken_charge)])
        out.append(inner_out)
    return out


# def _mulliken_densities(in_list):
#     out = []
#     for i in in_list:
#         inner_out = []
#         for row in i.split(sep="\n"):
#             atom_idx, _, mulliken_charge, spin_density = row.split()
#             inner_out.append([int(atom_idx), float(mulliken_charge), float(spin_density)])
#         out.append(inner_out)
#     return out

def _nmr(in_list):
    return [[int(i[0])] + _str_list_to_floats(i[1:]) for i in in_list]


POSTPROCESSING_FUNCTIONS = {
    "cpu_time": _unix_time_to_seconds,
    "wall_time": _unix_time_to_seconds,
    "e0": _str_to_float,
    "e0_h": _str_to_float,
    "hf": _str_to_float,
    "scf": _str_list_to_floats,
    "recovered_energy": _str_list_to_floats,
    "zpe_per_atom": _str_to_float,
    "wavefunction_energy": _str_to_float,
    "e0_zpe": _str_to_float,
    "gibbs": _str_to_float,
    "frequency_modes": _freq_modes,
    "frequencies": lambda in_list: [float(i) for sublist in in_list for i in sublist],
    "max_steps": lambda in_list: int(in_list[0]),
    "std_forces": _columns_to_floats,
    "std_xyz": _columns_to_floats,
    "xyz": _columns_to_floats,
    "route_section": lambda in_list: in_list[0],
    "charge_and_multiplicity": _charge_and_multiplicity,
    "mulliken_charges_summed": _mulliken,
    # "mulliken_charges_spin_densities_summed": _mulliken_densities,
    "dipole_au": _fortran_float_to_float,
    "aniso_polarizability_au": _fortran_float_to_float,
    "iso_polarizability_au": _fortran_float_to_float,
    "dipole_moment_debye": lambda in_list: _str_list_to_floats(in_list[-1]),  # always choose last printing
    "homo_lumo_gap": _hl_gap,
    "beta_homo_lumo_gap": _hl_gap,
    "nmr_shielding": _nmr,
}
