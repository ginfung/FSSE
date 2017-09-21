# FSSE
Fast search (sampling) technique for search-based software engineering problems

## Introduction
This repo concludes experiments for paper "Sampling as a Baseline Optimizer for Search-based Software Engineering".
SWAY is a sampling technique for solving search-based software engineering problems.
For more information, please check out our paper!

## Folders Organaization
- _Algorithms:_ source code for different optimizers (NSGA-II, SATIBEA and SWAY)
- _Benchmarks:_ source code for models tested in the paper. 
- _Experiments:_ entrance for different experiements
- _Metrics:_ source code for measuring results (See Section 5.3 of our paper)

## Other files
- _.gitignore:_ untracked files in this repo
- _LICENSE:_ the MIT license
- _addroot.sh:_ We are assuming that current project path has been added to PYTHONPATH. If not, please run this script.
- _debug.py:_ If you include this file inside main function, program will enter debug mode when error arises.
- _repeasts.py:_ including auxiliary functions to plot results


## Run experiments
To run the experiments, one should go to Folder "Experiments". Each file there contains one experiements. For example, to run NSGA-II for POM3 mode,
one should execute
```bash
cd Experiments
python pom3_nsga2.py
```

In this repo, `godview` = `GroundTruth`. Project was developed under python2.7. Python3 should be compatible but not tested.

All results are piped to one folder `tse_rs`. Please make sure you've created such folder within execute path.

To get multi-objective metrics(HV,GD,PFS or GS), go to "Metrics" and run `all_metrics.py`
