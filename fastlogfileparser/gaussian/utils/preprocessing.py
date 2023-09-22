def crush_ginc_block(opened_file):
    """Takes an opened logfile, reads and concatenates the GINC block and route section

    Args:
        logfile_text (fileIO): Logfile as read by open()
    """
    out = ""
    in_ginc_block = False
    in_route_section = False
    for line in opened_file:
        # starting a GINC block
        if line[:9] == " 1\\1\\GINC":
            in_ginc_block = True
        # strip last two characters
        elif in_ginc_block:
            # check if block is over
            if "@" in line:
                in_ginc_block = False
            else:
                line = line[1:-1]
        # starting route section
        if line.startswith(" #"):
            in_route_section = True
            line = line[1:-1]
        # strip last two characters
        elif in_route_section:
            # check if block is over
            if (
                " ----------------------------------------------------------------------\n"
                == line
            ):
                in_route_section = False
                line = "\n"
            else:
                line = line[1:-1]
        # append to output
        out += line
    return out


def split_composite_job(opened_file):
    """Takes an opened logfile, breaks into a new set of text for each linked job

    Args:
        logfile_text (fileIO): Logfile as read by open()
    """
    return opened_file.split(" Entering Link")[1:]
