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
    - you need a configuration file in a yaml format. Check [](`genomake.pipelines.chromake.scripts.config.create_example_config`) for an example. The [](`genomake.pipelines.chromake.scripts.config`) subpackage contains functions to generate such a config file from a samplesheet.
    - The configuration is composed of 3 main fields:
        - SEQUENCINGS
        - PROJECTS
        - JOBS

SEQUENCINGS is used to define the sample of a sequencing run that share similar adapter for trimming the reads, genome reference, and input samples (for ChIP-seq, more than one input can be indicated but only the first one will be used when identifying peak).

Each sequencing must have a parameters field to indicates at least:
  - the genome reference for bowtie2 (BOWTIE2_REF)
  - a bed of blacklisted regions (BLACKLIST_BED), see https://github.com/Boyle-Lab/Blacklist to download the file corresponding to the genome you use
  - a file indicating the chromosome size (CHROM_SIZE), see https://hgdownload.cse.ucsc.edu/goldenpath/hg38/bigZips/ to download the one for GRCh38/hg38. UCSC also host the files for other genomes such as mm10.
  - the genome used, either the .fa file of the reference used to build bowtie2 reference (toplevel.fa for ensembl) or a string such as hg38 or mm10 if the genome was configured in homer with configureHomer.pl (GENOME)
  - Adaptor trimming will be realized if the `R1_ADAPTOR` and the `R2_ADAPTOR`fields are present

```{.yaml}
SEQUENCING:
  MO211:
    SAMPLES:
      PSMD6_F1_Ci:
        R1: <PATH_TO_R1_fastq>
        TYPE: H3K27AC
        R2: <PATH_TO_R2_fastq>
      PSMD6_F1_Fa:
        R1: <PATH_TO_R1_fastq>
        TYPE: ATAC
        R2: <PATH_TO_R2_fastq>
    INPUT:
      Input_Batch1:
        R1: <PATH_TO_R1_fastq>
        R2: <PATH_TO_R2_fastq>
    PATH: <PATH_TO_R1_fastq>
    R1_ADAPTOR: CTGTCTCTTATACACATCT (modify to the sequence corresponding to your samples or remove this field to not trim)
    R2_ADAPTOR: CTGTCTCTTATACACATCT (modify to the sequence corresponding to your samples or remove this field to not trim)
    PARAMETERS:
      CUTADAPT: -q 20 --pair-filter=any (cutadapt paramters by default, modify or leave empty)
      BOWTIE2_REF: <PATH>/index-bowtie-2.3.0/Homo_sapiens.GRCh38.dna.toplevel (modify to point to your reference for bowtie2)
      BLACKLIST_BED: <PATH>/hg38-blacklist.v2.bed 
      GENOME: <PATH>/ensembl/release-99/Homo_sapiens.GRCh38.dna.toplevel.fa
      CHROM_SIZE: <PATH>/hg38.chrom.sizes
```

PROJECTS is used to regroup samples of different sequencing when realising peak calling and the minimal number of samples in which a peak is identified to be keep in the final count matrix. To be regrouped, the samples need to shares the same mark. The path of each project indicate where the files resulting of the peak calling will be created. It is recommanded to use different folders for each projects.
    
```{.yaml}
PROJECTS:
  ATAC:
    PROJECT_PATH: <PATH>
    TYPE: ATAC
    MIN_SAMPLES_FOR_PEAKS: 2
    SEQUENCING:
    - MO211
  ChIP_H3K27ME3:
    PROJECT_PATH: <PATH>
    TYPE: H3K27ME3
    MIN_SAMPLES_FOR_PEAKS: 2
    SEQUENCING:
    - MO203
  ChIP_H3K27AC:
    PROJECT_PATH: <PATH>
    TYPE: H3K27AC
    MIN_SAMPLES_FOR_PEAKS: 2
    SEQUENCING:
    - MO203
  ChIP_H2AUB:
    PROJECT_PATH: <PATH>
    TYPE: H2AUB
    MIN_SAMPLES_FOR_PEAKS: 2
    SEQUENCING:
    - MO203
```

The JOBS field is used to indicate the number of cpu to use for multithreadings and the QOS when running jobs on a clusters with an executor like slurm.

```{.yaml}
JOBS:
  CORES_PER_JOBS:
    FASTQC: 10
    CUTADAPT: 10
    BOWTIE2: 30
  QOS_INFOS:
    short:
      MaxWall: 1440
    medium:
      MaxWall: 4320
    long:
      MaxWall: 11520
```
  
You can use the genomake cli API to run snakemake:

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

For more information, check the[Command Line Interface](cli.qmd) and the [Get started]()get_started.qmd) pages of the documentation.

"""

# import all functions that don't start with "_"

from . import  scripts

#from .scripts.get_inputs import *
#from .scripts.get_outputs import *

__all__ = ["scripts"]


version = "1.0.0"
