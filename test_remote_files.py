from fabric.connection import Connection

host = "greencloud.mit.edu"
user = "admin"

gcloud_ssh_connection = Connection(host, user)
gcloud_sftp_connection = gcloud_ssh_connection.sftp()


def ropen(fname, mode):
    return gcloud_sftp_connection.open(fname, mode)


with ropen(
    "/volume1/home/users/oscar/supercloud/backup/project/habs/data/ts/semi/co2/co2_first_round_semi_log/rxn_0_oo_habs_co2_cap_ts_xtb_opt.log",
    "r",
) as file:
    for line in file:
        print(line)
        break
