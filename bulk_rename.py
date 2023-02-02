import os

target_dir = "$HOME/nlp-dft/data/dft"
log_dir = "$HOME/nlp-dft/data/screen"

log_dir = os.path.expandvars(log_dir)
target_dir = os.path.expandvars(target_dir)

log_files = os.listdir(log_dir)
target_files = os.listdir(target_dir)

for fname in target_files:
    os.rename(
        os.path.join(target_dir, fname),
        os.path.join(target_dir, "_".join(fname.split("_")[0:2]) + "_oo.log"),
    )

for fname in log_files:
    os.rename(
        os.path.join(log_dir, fname),
        os.path.join(log_dir, "_".join(fname.split("_")[0:2]) + "_oo.log"),
    )
