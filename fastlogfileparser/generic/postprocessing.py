# Post-processors that turn regex matches into useful data types.
#
# All returns from regex parser are lists, so these functions access the lists
# appropriately and then munge the contents.


def _unix_time_to_seconds(in_time):
    """Take ['0 days  0 hours 20 minutes 45.6 seconds'] formatted time and convert to seconds."""
    tmp = in_time[0].split()
    return (
        float(tmp[0]) * 86400
        + float(tmp[2]) * 3600
        + float(tmp[4]) * 60
        + float(tmp[6])
    )


def _charge_and_multiplicity(in_list):
    return [int(in_list[0][0]), int(in_list[0][1])]


def _str_list_to_floats(in_list):
    return [float(i) for i in in_list]


def _str_to_float(in_list):
    return float(in_list[0])


def _columns_to_floats(in_list):
    """Converts the force and coordinate table into 3D array of floats.
    Axis 0 is the timesteps, axis 1 is the atoms, axis 2 is the columns"""
    out_l = []
    for step in in_list:
        out_l.append([_str_list_to_floats(line.split()) for line in step.splitlines()])
    return out_l


def _freq_modes(in_list):
    as_floats = _columns_to_floats(in_list)
    out = []
    for freq_mode_group in as_floats:
        mode_i, mode_j, mode_k = [], [], []
        for atom_row in freq_mode_group:
            mode_i.append(atom_row[0:5])
            mode_j.append(atom_row[0:2] + atom_row[5:8])
            mode_k.append(atom_row[0:2] + atom_row[8:11])
        out.extend([mode_i, mode_j, mode_k])
    return out
