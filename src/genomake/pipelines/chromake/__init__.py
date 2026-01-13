"""
Chromake pipeline

This subpackage is used to contains a snakemake pipeline and functions to align sequencing data of ChIP-seq and ATAC-seq experiments, identify peaks, and realize a read count.

The ressources used can be modified. In particular, the number of cores can be specified in the config file while other ressources (memory, runtime) will necessite to copy and modify the snakefile included in this subpackage.

Notes
-----

This subpackage contains submodules ([](`genomake.pipelines.chromake.scripts.config`) and [](`genomake.pipelines.chromake.scripts.config`)). Among them, [paths](`genomake.pipelines.chromake.scripts.paths`) is used by the snakefile to track the files it generate, while [config](`genomake.pipelines.chromake.scripts.config`) was created to help the user create the YAML config file needed by snakemake.

Examples
--------

To run the pipeline:
    - you need at least 60 Go of RAM.
    - you need a config file. Check [](`genomake.pipelines.chromake.scripts.config.create_example_config`) for an example. The [](`genomake.pipelines.chromake.scripts.config`) subpackage contains functions to generate such a config file from a samplesheet.
    - you can use the genomake cli API to run snakemake:

```{.bash}
genomake chromake -c ./config.yaml --cores 250 --local-cores 1 --jobs 8
```

All options can be checked with a:
```{.bash}
genomake chromake -h
```

The "--others-snakemake" option allow to specify additionnal arguments in the final command. It can be useful to unlock the working directory, try a dry run or specify an executor (slurm in my example).


```{.bash}
genomake chromake -c ./config.yaml \
--cores 250 --local-cores 1 --jobs 8 \
--others-snakemake "--executor slurm --default-resources slurm_account=singlecell \
clusters=nautilus --slurm-logdir ./logs --slurm-keep-successful-logs \
--slurm-delete-logfiles-older-than 0 \
--rerun-incomplete -np --unlock" -p
```

This command will print the command next as the "-p" argument was used, without it, the command will be executed):
    
```{.bash}
snakemake --snakefile <PATH to snakefile in installation> \
--configfile ./config.yaml --retries 4 --cores 250 --jobs 8 \
--local-cores 1 --executor slurm \
--default-resources slurm_account=singlecell clusters=nautilus \
--slurm-logdir ./logs --slurm-keep-successful-logs \
--slurm-delete-logfiles-older-than 0 --rerun-incomplete
```

"""

# import all functions that don't start with "_"

from . import  scripts

#from .scripts.get_inputs import *
#from .scripts.get_outputs import *

__all__ = ["scripts"]


version = "1.0.0"
