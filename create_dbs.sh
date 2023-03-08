#!/bin/bash -i

source /home/jwburns/.bashrc

mytime python db_write.py -d ./oo_data_test.db -s /home/jwburns/semi-dft/data/screen -t /home/jwburns/semi-dft/data/dft -f rxn_{:d}_oo.log