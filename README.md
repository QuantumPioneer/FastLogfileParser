# FastLogfileParser
## Parse logfiles from computational chemistry software, but fast-ly

Install with `pip install fastlogfileparser` or `conda` (forthcoming!).

 1. ~10x faster than `cclib`
 2. **zero** dependencies, supports all modern Python version
 3. Supports linked jobs, returns a separate result dictionary for each job
 4. Retrieves values at every step, not just convergence

## Usage
### Gaussian

There is a single function `fast_gaussian_logfile_parser` inside `fastlogfileparser.gaussian` which reads logfiles and returns the result as a [namedtuple](https://docs.python.org/3/library/collections.html#collections.namedtuple) (which prevents accidentally changing the values and allows using `.` syntax to access them).

#### Usage Example

```python
from fastlogfileparser.gaussian import fast_gaussian_logfile_parser as fglp

# read all jobs from the logfile
job_1, job_2, ..., job_n = fglp("data/result.log")

# access results
print(job_1.frequency_modes)

# show all available values retrieved from the file
print(job_1._fields)

# can also be accessed via
from fastlogfileparser.gaussian import FIELDS
```

Fast logfile parser is fastest when you ask it to retrieve only the fields you want, i.e.:
```python
job_1, job_2, job_3 = fglp(FNAME, get=("gibbs", "scf"))
```

#### Retrieved Values

| Quantity | Key | Type | Frequency |
| -------- | --- | ---- | --------- |
| Gibbs free energy at 298K | `gibbs` | float | 1/job |
| Gibbs free energy at 0K | `e0_zpe` | float | 1/job |
| Enthalpy at 298K | `e0_h` | float | 1/job |
| E0 $^1$ | `E0` | float | 1/job |
| Per-atom Zero Point Energy | `zpe_per_atom` | float | 1/job |
| Standardized xyz coords | `std_xyz` | list[float] | 1/step/job |
| ... | ... | ... | ... | 
| Number of Atoms $^2$ | `number_of_atoms` | int | 1/job |
| Number of Optimization Steps $^2$ | `number_of_optimization_steps` | int | 1/job |

$1$ equals E0 only for non-wavefunction methods <br>
$2$ requires `std_xyz` to be parsed to find these values <br>

## How much fast-ly-er?
`FastLogfileParser` uses REGEX and only REGEX to retrieve data from logfiles, spending as much time in Python's excellent C-based REGEX library as possible.

See `comparison.py` to run for yourself (install with `pip install .[demos]`), but in short:
 - compared to `cclib`, `fastlogfileparser` is ~10x as fast and returns all values for intermediate steps in simulation (but `cclib` supports retrieving a different set of values)
 - compared to `ase`, `fastlogfileparser` is ~2x slower, but returns _far more_ values and in a more readily accessible format

## Development Notes
`FastLogfileParser` is written in a purely functional style.

### Running Tests
Install `FastLogfileParser` with the optional `[dev]` dependencies, i.e. from a local clone run `pip install -e ".[dev]"

Rather than keep the gigantic log files saved in the git repo directly, they are compressed to make cloning easier.
Before running tests, navigate to `test` and run `python data_loader.py decompress` to prepare the needed logfiles.

To add new data for the tests to the repo, perform the previous step and then run `python data_loader.py compress`.
This may take some time to finish executing (a minute or so).
