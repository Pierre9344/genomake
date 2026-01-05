"""
This is the genomake package.

Genomake (Genomic make is a collection of functions and snakemake pipelines to analyze genomic data.

Currently only implement the chromake pipeline.
"""



# load subpackages next when importing the main package
from .pipelines import chromake

# make subpackage listed public so that they can be loaded with
# from <this_package> import *
__all__ = ["chromake"]

version = "1.0.0"
