def _unix_time_to_seconds(intime):
    """Take '0 days  0 hours 20 minutes 45.6 seconds' formatted times and convert to seconds."""
    out_times = []
    for timestr in intime:
        tmp = timestr.split()
        out_times.append(
            float(tmp[0]) * 86400
            + float(tmp[2]) * 3600
            + float(tmp[4]) * 60
            + float(tmp[6])
        )
    return out_times


def _str_list_to_floats(l):
    return [float(i) for i in l]


def _num_atoms_reducer(l):
    return int(l[0])


def _columns_to_floats(l):
    """Converts the force and coordinate table into 3D array of floats.
    Axis 0 is the timesteps, axis 1 is the atoms, axis 2 is the columns"""
    out_l = []
    for step in l:
        out_l.append([_str_list_to_floats(line.split()) for line in step.splitlines()])
    return out_l


POSTPROCESSING_FUNCTIONS = {
    "cpu_time": _unix_time_to_seconds,
    "wall_time": _unix_time_to_seconds,
    "e0": _str_list_to_floats,
    "e0_h": _str_list_to_floats,
    "zpe": _str_list_to_floats,
    "e0_zpe": _str_list_to_floats,
    "gibbs": _str_list_to_floats,
    "num_atoms": _num_atoms_reducer,
    "frequencies": lambda l: [_str_list_to_floats(list(i)) for i in l],
    "steps": _str_list_to_floats, # TODO: should be integer, also currently it is parsing max step but not actual step 
    "std_forces": _columns_to_floats,
    "std_xyz": _columns_to_floats,
    "xyz": _columns_to_floats,
}
