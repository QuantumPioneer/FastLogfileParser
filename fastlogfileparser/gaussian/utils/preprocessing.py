def crush_ginc_block(opened_file):
    """Takes an opened logfile, reads and concatenates the "1\1\GINC" block

    Args:
        logfile_text (fileIO): Logfile as read by open()
    """
    out = ""
    in_ginc_block = False
    for line in opened_file:
        # starting a GINC block
        if line[:12] == " 1\\1\\GINC-C-":
            in_ginc_block = True
        # strip last two characters
        elif in_ginc_block:
            # check if block is over
            if "@" in line:
                in_ginc_block = False
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
