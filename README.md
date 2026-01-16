# About genomake

Genomake (genomic make) is a python package to analyze genomic data using snakemake pipeline.


# Current pipeline

## chromake

Chromake is a pipeline to analyze ATAC-seq and ChIP-seq experiment.

It currently supports the epigenetic marks H3K27Ac, H3K27me3, and H2Aub (H2A Ubiquitination):

| Experiment 	| Epigenetic mark 	| Full name                                                                             	| Config recognized names 	|
|------------	|-----------------	|---------------------------------------------------------------------------------------	|-------------------------	|
| ChIP-seq   	| H3K27Ac         	| Acetylation of the lysine residue at N-terminal position 27 of the histone H3 protein 	| H3K27AC                 	|
| ChIP-seq   	| H3K27me3        	| Tri-methylation of lysine 27 on histone H3 protein                                    	| H3K27ME3                	|
| ChIP-seq   	| H2Aub           	| Histone 2A Ubiquitination                                                             	| H2AUB                   	|
| ATAC-seq   	| None            	| Assay for Transposase-Accessible Chromatin                                            	| ATAC                    	|


Steps realized:

    1. FASTQ trimming using cutadapt
    2. QC (fastqc and multiqc) of raw and trimmed fastq files.
    3. Alignment on genome (using bowtie2).
    4. Peak calling (using macs2).
    5. Read count (bedtools and samtools) /!\ WIP /!\
    

# Documentation

Documentation was generated using [quartodoc](https://machow.github.io/quartodoc/get-started/overview.html). While there is no website currently, you can access it by downloading the project from github then go into the Docs folder and launch the commands next:

```{.bash}
cd <path to genomake base folder>
pip install .
cd Docs
quartodoc build
quarto render .
```

