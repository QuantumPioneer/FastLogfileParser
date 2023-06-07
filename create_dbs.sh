#!/bin/bash -i

source /home/jwburns/.bashrc

# conda activate nlp-dft

# echo "co2 first round"

# python db_write.py \
# -d ./habs_database_for_julia.db \
# --new-table-name co2firstround \
# -s /home/jwburns/habs_data/semi/co2/co2_first_round_semi_log \
# -t /home/jwburns/habs_data/dft/co2/co2_dft_log \
# --screen-file-fstring rxn_{:0}_oo_habs_co2_cap_ts_xtb_opt.log \
# --dft-file-fstring rxn_{:0}_oo_habs_co2_small_ts_wb97xd_aug19a.log

# echo "co2 sep2"

# python db_write.py \
# -d ./habs_database_for_julia.db \
# --new-table-name co2sep2 \
# -s /data/habs_ts_logs_copy/semi/co2/co2_sep2_log \
# -t /data/habs_ts_logs_copy/dft/co2/co2_sep2_dft_log \
# --screen-file-fstring rxn_{:0}_oo_habs_co2_cap_sep2_ts_xtb_opt.log \
# --dft-file-fstring rxn_{:0}_oo_habs_co2_sep2_ts_wb97xd_sep2a.log

# echo "roo"

# python db_write.py \
# -d ./habs_database_for_julia.db \
# --new-table-name roo \
# -s /data/habs_ts_logs_copy/semi/roo/log \
# -t /data/habs_ts_logs_copy/dft/roo/log \
# --screen-file-fstring rxn_{:0}_oo_habs_roo_sep2_ts_xtb_opt.log \
# --dft-file-fstring rxn_{:0}_oo_habs_roo_ts_wb97xd_sep4a.log

echo "oo_grp"

python db_write.py \
-d ./habs_database_for_julia.db \
--new-table-name oogrp \
-s /data/habs_ts_logs_copy/semi/oo_grp/combo \
-t /data/habs_ts_logs_copy/dft/oo_grp/oo_grp_ts_wb97xd_log_sd_july27 \
--screen-file-fstring rxn_{:0}_ts_opt.log \
--dft-file-fstring rxn_{:0}_oo_g4mp2_ts_wb97xd_opt.log