"""
This is the 'chromake' subpackage.

Used to contains a snakemake pipeline and functions to align sequencing data of ChIP-seq and ATAC-seq experiments, identify peaks, and realize a read count.
"""

# import all functions that don't start with "_"

from . import  scripts

#from .scripts.get_inputs import *
#from .scripts.get_outputs import *

__all_ = ["scripts"]