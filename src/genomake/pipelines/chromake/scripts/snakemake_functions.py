"""
The snakemake_functions module contains functions called inside the snakefile.

"""


def select_clusters_spec(attempt: int, default_time_min: int, cfg: dict)->str:
    """
    Identify the name qos and partition from the config file using the time of the job. This function is called by the `get_qos_from_time`and `get_partition_from_time` functions.

    Parameters
    ----------
    attempt : int
        Current attempt of the job (set by snakemake)
        
    default_time_min: int
        Time in minute that the job ask to the executor
        
    cfg: dict
        Configuration file of the chromake pipeline

    Returns
    -------
    str
        The name of the tier (qos, partition) to use depending on the time requested by a rule.
    """

    runtime_minutes = attempt * default_time_min
    selected_tier = None

    for tier_name, tier_info in cfg["JOBS"]["SCHEDULER_PROFILES"].items():
        if tier_name == "default":
            continue
        
        maxwall = tier_info.get("MaxWall")
        if maxwall is None:
            continue
        if maxwall >= runtime_minutes:
            if selected_tier is None or maxwall < cfg["JOBS"]["SCHEDULER_PROFILES"][selected_tier]["MaxWall"]:
                selected_tier = tier_name

    # fallback to 'long' if none found
    return selected_tier or "default"

def get_qos_from_time(attempt: int, default_time_min: int, cfg: dict)->str:
    """
    Identify the name qos to use from the config file using the time of the job. This function is used when an executor is set.

    Parameters
    ----------
    attempt : int
        Current attempt of the job (set by snakemake)
        
    default_time_min: int
        Time in minute that the job ask to the executor
        
    cfg: dict
        Configuration file of the chromake pipeline

    Returns
    -------
    str
        The name of the qos to use for the rule.
    """
    
    tier = select_clusters_spec(attempt, default_time_min, cfg)
    return cfg["JOBS"]["SCHEDULER_PROFILES"][tier]["qos_name"]

def get_partition_from_time(attempt: int, default_time_min: int, cfg: dict)->str:
    """
    Identify the name qos to use from the config file using the time of the job. This function is used when an executor is set.

    Parameters
    ----------
    attempt : int
        Current attempt of the job (set by snakemake)
        
    default_time_min: int
        Time in minute that the job ask to the executor
        
    cfg: dict
        Configuration file of the chromake pipeline

    Returns
    -------
    str
        The name of the partition to use for the rule.
    """
    tier = select_clusters_spec(attempt, default_time_min, cfg)
    return cfg["JOBS"]["SCHEDULER_PROFILES"][tier]["partition_name"]



def detect_macs_version():
    """
    Detect which version of macs (macs2 or macs3) is installed in the python environment. If no version is found this function raise an error.
    
    Returns
    -------
    str
        The name of the program (macs2 or macs3).

    """
    from importlib.util import find_spec
    if find_spec("MACS3"):
        CALLER = "macs3"
    elif find_spec("MACS2"):
        CALLER = "macs2"
    else:
        raise RuntimeError("Neither MACS2 nor MACS3 is installed!")
    return CALLER