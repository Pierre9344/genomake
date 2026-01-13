"""
The config module of chromake contains functions to read and write the config file of the chromake pipeline.

"""

import pandas as pd
import yaml
import warnings
import os
#import platform

#def normalize_path(path: Path) -> str:
#    # Convert Path to string and replace backslashes with forward slashes
#    return str(path).replace("\\", "/")

def create_example_config(
    filename: str = "config.yaml",
) :
    """
    Create an example genomake/chromake YAML configuration file
    using the new SEQUENCING / PROJECTS split.

    Parameters
    ----------
    filename : str, optional
        Filename to use if `output` is a directory.

    Returns
    -------
    str
        Path to the written YAML configuration file.
    """

    config = {
        "SEQUENCING": {
            "MO203": {
                "SAMPLES": {
                    "H3K27ac_BAP1": {
                        "R1": "FASTQ/H3K27ac_BAP1_111_R1_001.fastq.gz",
                        "R2": "FASTQ/H3K27ac_BAP1_111_R2_001.fastq.gz",
                        "TYPE": "H3K27AC",
                    },
                    "Hub2A_PSMC5_D4": {
                        "R1": "FASTQ/Hub2A_PSMD6_F1Ci_R1_001.fastq.gz",
                        "R2": "FASTQ/Hub2A_PSMD6_F1Ci_R2_001.fastq.gz",
                        "TYPE": "H2AUB",
                    },
                    "H3K27me3_PSMC5_D4": {
                        "R1": "FASTQ/H3K27me3_PSMC5_D4_R1_001.fastq.gz",
                        "R2": "FASTQ/H3K27me3_PSMC5_D4_R2_001.fastq.gz",
                        "TYPE": "H3K27ME3",
                    },
                    "Hub2A_USP7_CM": {
                        "R1": "FASTQ/Hub2A_USP7_Fa_R1_001.fastq.gz",
                        "R2": "FASTQ/Hub2A_USP7_Fa_R2_001.fastq.gz",
                        "TYPE": "H2AUB",
                    },
                },
                "INPUT": {
                    "Input_Batch1": {
                        "R1": "FASTQ/Input_Batch1_R1_001.fastq.gz",
                        "R2": "FASTQ/Input_Batch1_R2_001.fastq.gz",
                    }
                },
                "PATH": "/scratch/nautilus/projects/CR2TI_lab/SingleCell/Pierre_Solomon/MO203/",
                "R1_ADAPTOR": "AGATCGGAAGAGCACACGTCTGAACTCCAGTCA",
                "R2_ADAPTOR": "AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT",
                "PARAMETERS": {
                    "CUTADAPT": "-q 20 --pair-filter=any"
                }
            },
            "MO208": {
                "SAMPLES": {
                    "H3K27ac_BAP1_AC": {
                        "R1": "FASTQ/H3K27ac_BAP1_AC_S18_R1_001.fastq.gz",
                        "R2": "FASTQ/H3K27ac_BAP1_AC_S18_R2_001.fastq.gz",
                        "TYPE": "H3K27AC",
                    },
                    "H3K27ac_BAP1_HF": {
                        "R1": "FASTQ/H3K27ac_BAP1_HF_S42_R1_001.fastq.gz",
                        "R2": "FASTQ/H3K27ac_BAP1_HF_S42_R2_001.fastq.gz",
                        "TYPE": "H3K27AC",
                    },
                    "Hub2A_USP7_MaVL": {
                        "R1": "FASTQ/Hub2A_USP7_MaVL_S34_R1_001.fastq.gz",
                        "R2": "FASTQ/Hub2A_USP7_MaVL_S34_R2_001.fastq.gz",
                        "TYPE": "H2AUB",
                    },
                },
                "INPUT": {
                    "Input_Batch2": {
                        "R1": "FASTQ/Input_BATCH2_S2_R1_001.fastq.gz",
                        "R2": "FASTQ/Input_BATCH2_S2_R2_001.fastq.gz",
                    }
                },
                "PATH": "/scratch/nautilus/projects/CR2TI_lab/SingleCell/Pierre_Solomon/MO208/",
                "R1_ADAPTOR": "AGATCGGAAGAGCACACGTCTGAACTCCAGTCA",
                "R2_ADAPTOR": "AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT",
                "PARAMETERS": {
                    "CUTADAPT": "-q 20 --pair-filter=any"
                }
            },
            "MO211": {
                "SAMPLES": {
                    "USP7-YVL_S20": {
                        "R1": "FASTQ/USP7-YVL_S20_R1_001.fastq.gz",
                        "R2": "FASTQ/USP7-YVL_S20_R2_001.fastq.gz",
                        "TYPE": "ATAC",
                    },
                    "BAP1-111_S27": {
                        "R1": "FASTQ/BAP1-111_S27_R1_001.fastq.gz",
                        "R2": "FASTQ/BAP1-111_S27_R2_001.fastq.gz",
                        "TYPE": "ATAC",
                    },
                },
                "PATH": "/scratch/nautilus/projects/CR2TI_lab/SingleCell/Pierre_Solomon/MO211/",
                "R1_ADAPTOR": "CTGTCTCTTATACACATCT",
                "R2_ADAPTOR": "CTGTCTCTTATACACATCT",
                "PARAMETERS": {
                    "CUTADAPT": "-q 20 --pair-filter=any"
                }
            },
        },
        "PROJECTS": {
            "ChIP_H3K27AC": {
                "SEQUENCING": ["MO203", "MO208"],
                "TYPE": "H3K27AC",
                "MIN_SAMPLES_FOR_PEAKS": 2,
                "PROJECT_PATH": "/scratch/nautilus/projects/CR2TI_lab/SingleCell/Pierre_Solomon/ChIP_H3K27AC",
            },
            "ChIP_H3K27ME3": {
                "SEQUENCING": ["MO203"],
                "TYPE": "H3K27ME3",
                "MIN_SAMPLES_FOR_PEAKS": 2,
                "PROJECT_PATH": "/scratch/nautilus/projects/CR2TI_lab/SingleCell/Pierre_Solomon/ChIP_H3K27ME3",
            },
            "ChIP_H2AUB": {
                "SEQUENCING": ["MO203", "MO208"],
                "TYPE": "H2AUB",
                "MIN_SAMPLES_FOR_PEAKS": 2,
                "PROJECT_PATH": "/scratch/nautilus/projects/CR2TI_lab/SingleCell/Pierre_Solomon/ChIP_H2AUB",
            },
            "ChIP_ATAC": {
                "SEQUENCING": ["MO211"],
                "TYPE": "ATAC",
                "MIN_SAMPLES_FOR_PEAKS": 2,
                "PROJECT_PATH": "/scratch/nautilus/projects/CR2TI_lab/SingleCell/Pierre_Solomon/ChIP_ATAC",
            },
        },
        "JOBS": {
            "CORES_PER_JOBS": {
                "FASTQC": 10,
                "CUTADAPT": 10,
                "BOWTIE2": 30
            },
            "QOS_INFOS": {
                "short": {"MaxWall": 24 * 60}, # 1 day
                "medium": {"MaxWall": 3 * 24 * 60}, # 3 days
                "long": {"MaxWall": 8 * 24 * 60}, # 8 days in minutes
            },
        },
    }
    
    if (os.path.splitext(filename)[1] == ".yaml") & (os.path.splitext(filename)[0] != ""):
        config_path = filename
        dir_name = os.path.dirname(config_path)
        if dir_name and not ((os.path.exists(dir_name)) & (dir_name != "")):
            print("Parent directory was created: " + dir_name)
            os.makedirs(dir_name, exist_ok=True)
    else:
        config_path = "config.yaml"
        print("filename was not valid. Defaulting to 'config.yaml'")

    with open(config_path, "w", encoding="utf-8") as stream:
        yaml.safe_dump(config, stream, sort_keys=False)

    return ("created the file: " + config_path)


def update_jobs(config_path: str, jobs: dict) -> None:
    """
    Update or add the JOBS section in an existing YAML config.
    
    CORES_PER_JOBS: number of cpu cores to use for each jobs (>=1)
    
    QOS_INFOS: if using an executor like slurm, indicate the name of the qos (e.g. short), and the associated MaxWall in minutes.

    Parameters
    ----------
    config_path : str
        Path to the YAML config file.
    jobs : dict
        Dictionary containing JOBS information to update.
        Can be a full replacement or partial update.
    
    Example
    -------
    >>> jobs_update = {
    ...     "CORES_PER_JOBS": { "FASTQC": 10, "CUTADAPT": 10, "BOWTIE2": 30 },
    ...     "QOS_INFOS": { "short": {"MaxWall": 2000}, "medium": {"MaxWall": 5000}, "long": {"MaxWall": 15000} }
    ... }
    >>> update_jobs("config.yaml", jobs_update)
    """
    
    with open(config_path) as stream:
        config = yaml.safe_load(stream)

    if not config:
        config = {}

    # Merge jobs into existing config
    if "JOBS" not in config:
        config["JOBS"] = jobs
    else:
        if "CORES_PER_JOBS" in jobs.keys():
            for job_name, job_data in jobs["CORES_PER_JOBS"].items():
                if type(job_data) == int:
                    if "CORES_PER_JOBS" not in config["JOBS"].keys():
                        config["JOBS"]["CORES_PER_JOBS"] = {}
                    config["JOBS"]["CORES_PER_JOBS"][job_name] = job_data
        if "QOS_INFOS" in jobs.keys():
            if "QOS_INFOS" in config["JOBS"].keys():
                # override all value
                for k, i in jobs["QOS_INFOS"].items():
                    # Second loop to make sure the items are corrects. Currently on use MaxWall.
                    for j, l in  jobs["QOS_INFOS"][k].items():
                        if j in {"MaxWall"}:
                            if k not in config["JOBS"]["QOS_INFOS"]:
                                config["JOBS"]["QOS_INFOS"][k] = {}
                            config["JOBS"]["QOS_INFOS"][k]["MaxWall"] = l
                            print("added/overrided config QOS_INFOS " + k + " with " + j)
            else:
                config["JOBS"]["QOS_INFOS"] = jobs["QOS_INFOS"]

    config = check_project_and_sequencing(config)
    with open(config_path, "w", encoding="utf-8") as stream:
        yaml.safe_dump(config, stream, sort_keys=False, default_flow_style=False)


def check_project_and_sequencing(config: dict) -> dict:
    """
    Ensures that projects with no associated sequencing samples are removed from the config,
    and removes empty sequencing projects, while making sure the mark is considered in the filtering process.

    Parameters
    ----------
    config : dict
        Loaded YAML config (as a dictionary).

    Returns
    ------- 
    dict
        Updated config dictionary.
    """
    if "SEQUENCING" not in config:
        return config
    
    # Loop through the sequencing section and clean empty sequencing projects
    for sequencing_name, sequencing_data in config["SEQUENCING"].items():
        # If there are no samples and inputs, remove the sequencing project
        if not sequencing_data.get("SAMPLES") and not sequencing_data.get("INPUT"):
            del config["SEQUENCING"][sequencing_name]
            print(f"Removed sequencing project '{sequencing_name}' as it has no samples or inputs.")
        else:
            if sequencing_data.get("INPUT"):
                if len(sequencing_data.get("INPUT")) == 0:
                    del config["SEQUENCING"][sequencing_name]["INPUT"]
                    print(f"Removed the input field of sequencing project {sequencing_name} as it was empty.")
            
            for sample_name, sample_data in config["SEQUENCING"][sequencing_name]["SAMPLES"].items():
                if (sample_data["TYPE"] in ["H3K27AC", "H3K27ME3", "H2AUB"]):
                    if "INPUT" in sequencing_data.keys():
                        for input_name, input_data in sequencing_data["INPUT"].items():
                            if ("R1" not in input_data.keys()) or ("R1" not in input_data.keys()) or ("R2" not in input_data.keys()):
                                print(f"Sequencing {sequencing_name} contains samples from ChIP-seq experiment but INPUT field ({input_name}) is not valid. Please check your configuration file.")
                    else:
                        print(f"Sequencing {sequencing_name} contains samples from ChIP-seq experiment but INPUT field is missing. Please check your configuration file.")
    # Now loop through the projects and remove references to empty sequencing projects
    if "PROJECTS" in config:
        for project_key, project_data in config["PROJECTS"].items():
            project_mark = project_data.get("TYPE")  # Get the mark associated with the project
            
            if isinstance(project_data.get("SEQUENCING"), list):
                # Filter out sequencing projects that no longer have samples for the project mark
                updated_sequencing_projects = [
                    seq_proj for seq_proj in project_data["SEQUENCING"].items()
                    if seq_proj in config["SEQUENCING"] and 
                       config["SEQUENCING"][seq_proj].get("SAMPLES") and
                       any(sample_data["TYPE"] == project_mark for sample_data in config["SEQUENCING"][seq_proj]["SAMPLES"].values())
                ]
                
                # If the list is empty, remove the sequencing from the project
                if updated_sequencing_projects != project_data["SEQUENCING"]:
                    project_data["SEQUENCING"] = updated_sequencing_projects
                    print(f"Updated project '{project_key}' to reflect current sequencing projects: {updated_sequencing_projects}")
                    
                    # If no valid sequencing projects remain, remove the project
                    if not updated_sequencing_projects:
                        del config["PROJECTS"][project_key]
                        print(f"Removed project '{project_key}' as it has no valid sequencing projects.")
    
    return config

def remove_sequencing(config_path: str, sequencing_name: str) -> None:
    """
    Remove an entire sequencing project from the YAML config.

    Parameters
    ----------
    config_path : str
        Path to the YAML config file.
    sequencing_name : str
        Name of the sequencing project to remove.
    """

    # Load existing config
    with open(config_path) as stream:
        config = yaml.safe_load(stream)

    if not config:
        print("Config is empty.")
        return

    # Remove the sequencing project from SEQUENCING section
    if "SEQUENCING" in config and sequencing_name in config["SEQUENCING"]:
        del config["SEQUENCING"][sequencing_name]
        print(f"Removed sequencing project '{sequencing_name}' from SEQUENCING.")
    else:
        print(f"Sequencing project '{sequencing_name}' not found in SEQUENCING.")

    # Now call check_project_and_sequencing to ensure everything is cleaned up
    config = check_project_and_sequencing(config)
    with open(config_path, "w", encoding="utf-8") as stream:
        yaml.safe_dump(config, stream, sort_keys=False, default_flow_style=False)

def remove_samples(config_path: str, sequencing_name: str, samples: list[str]) -> None:
    """
    Remove specific samples from a project in the YAML config.

    Parameters
    ----------
    config_path : str
        Path to the YAML config file.
    sequencing_name : str
        Name of the project containing the samples.
    samples : list of str
        List of sample names to remove.
    """

    # Load existing config
    with open(config_path) as stream:
        config = yaml.safe_load(stream)

    if "SEQUENCING" not in config or sequencing_name not in config["SEQUENCING"]:
        print(f"Sequencing project '{sequencing_name}' not found in config.")
        return

    sequencing_project = config["SEQUENCING"][sequencing_name]
    project_samples = sequencing_project.get("SAMPLES", {})

    for sample in samples:
        if sample in project_samples:
            del project_samples[sample]
            print(f"Removed sample '{sample}' from sequencing project '{sequencing_name}'.")
        else:
            print(f"Sample '{sample}' not found in sequencing project '{sequencing_name}'.")

    # If no samples remain, remove the SAMPLES key
    if not project_samples:
        sequencing_project.pop("SAMPLES", None)
        print(f"No samples left in sequencing project '{sequencing_name}', removing SAMPLES.")

    # If no samples and inputs remain, remove the sequencing project
    if not sequencing_project.get("SAMPLES") and not sequencing_project.get("INPUT"):
        remove_sequencing(config_path, sequencing_name)
        print(f"Sequencing project '{sequencing_name}' has no samples or inputs left, removing project.")

    # Now call the check function to ensure the PROJECTS section is updated
    config = check_project_and_sequencing(config)
    with open(config_path, "w", encoding="utf-8") as stream:
        yaml.safe_dump(config, stream, sort_keys=False, default_flow_style=False)

def create_samplesheet_from_config(
    config_path: str,
    output_path: str,
    strand_columns: bool = False,
    excel: bool = True
) -> str:
    """
    Create a samplesheet table (CSV or Excel) from a YAML config, resolving relative paths
    by adding the sequencing project path. Includes both SAMPLES and INPUTS.

    Parameters
    ----------
    config_path : str
        Path to the YAML config file.
    output_path : str
        Path to save the generated table (CSV by default; Excel if excel=True).
    strand_columns : bool, optional
        If True, each strand (R1, R2) PATH will be a separate column (wide format);
        if False, each strand will be in separate rows and a STRAND columns will be added to differentiate them (long format).
    excel : bool, optional
        If True, save as Excel (.xlsx). Otherwise, save as CSV.

    Returns
    -------
    str
        Path to the generated samplesheet file.
    """

    # Load YAML config
    with open(config_path) as stream:
        config = yaml.safe_load(stream)

    rows = []
    sequencing = config.get("SEQUENCING", {})  # Get SEQUENCING instead of PROJECTS
    projects = config.get("PROJECTS", {})  # Get PROJECTS

    # Iterate over sequencing projects
    for seq_name, seq_data in sequencing.items():
        proj_path = seq_data.get("PATH", "")  # Get project root path
        samples = seq_data.get("SAMPLES", {})
        inputs = seq_data.get("INPUT", {})

        # Process SAMPLES
        for sample_name, sample_data in samples.items():
            mark = sample_data.get("TYPE", "")

            if strand_columns:
                # Wide format: separate R1 and R2 into distinct columns
                row = {
                    "SAMPLE": sample_name,
                    "SEQUENCING": seq_name,  # SEQUENCING
                    "PROJECT": "",  # Will update later for regular samples
                    "TYPE": mark,  # The mark type (H3K27AC, H2AUB, etc.)
                    "R1": "",  # Placeholder for R1 path
                    "R2": ""   # Placeholder for R2 path
                }

                # Add R1 and R2 paths
                for strand, path in sample_data.items():
                    if strand == "R1":
                        if proj_path and not os.path.isabs(path):
                            row["R1"] = proj_path + path
                        else:
                            row["R1"] = path  # Use path as is if it's absolute or no proj_path

                        
                    elif strand == "R2":
                        if proj_path and not os.path.isabs(path):
                            row["R2"] = proj_path + path
                        else:
                            row["R2"] = path  # Use path as is if it's absolute or no proj_path

                rows.append(row)  # Add row for sample with R1 and R2 in separate columns
            else:
                # Long format: one row per strand (R1 or R2)
                sample_type = sample_data.get("TYPE", "")
                for strand, path in sample_data.items():
                    if strand != "TYPE":
                        # Resolve relative path to full path using project path
                        full_path = (proj_path + path) if proj_path and not os.path.isabs(path) else path
                        rows.append({
                            "SAMPLE": sample_name,
                            "SEQUENCING": seq_name,  # SEQUENCING
                            "PROJECT": "",  # Will update later for regular samples
                            "TYPE": sample_type,  # The mark type (H3K27AC, H2AUB, etc.)
                            "STRAND": strand,  # Set STRAND (R1 or R2)
                            "PATH": full_path
                        })

        # Process INPUTS (same logic as samples)
        for input_name, input_data in inputs.items():
            if strand_columns:
                # Wide format: separate R1 and R2 into distinct columns for INPUTS
                row_input = {
                    "SAMPLE": input_name,
                    "SEQUENCING": seq_name,  # SEQUENCING
                    "PROJECT": "INPUT",  # Mark as INPUT
                    "TYPE": "",  # No mark for INPUT
                    "R1": "",  # Placeholder for R1 path
                    "R2": ""   # Placeholder for R2 path
                }

                # Add R1 and R2 paths for INPUTS
                for strand, path in input_data.items():
                    if strand == "R1":
                        full_path = (proj_path + path) if proj_path and not os.path.isabs(path) else path
                        row_input["R1"] = full_path
                    elif strand == "R2":
                        full_path = (proj_path + path) if proj_path and not os.path.isabs(path) else path
                        row_input["R2"] = full_path
                rows.append(row_input)  # Add row for INPUT with R1 and R2 in separate columns
            else:
                # Long format: one row per strand for input
                for strand, path in input_data.items():
                    # Resolve relative path to full path using project path
                    full_path = (proj_path + path) if proj_path and not os.path.isabs(path) else path
                    rows.append({
                        "SAMPLE": input_name,
                        "SEQUENCING": seq_name,  # SEQUENCING
                        "PROJECT": "INPUT",  # Mark as INPUT
                        "TYPE": "",  # No mark for INPUT
                        "STRAND": strand,  # Set STRAND (R1 or R2)
                        "PATH": full_path
                    })

    # Now, we need to update the PROJECT field for regular samples
    for row in rows:
        if row["PROJECT"] == "":  # Only update if it's not an input
            mark = row["TYPE"]
            for project_key, project_data in projects.items():
                if mark == project_data.get("TYPE"):
                    # If the mark matches, associate the project
                    row["PROJECT"] = project_key
                    break

        # For INPUT samples, we assign the project directly as "INPUT"
        if row["PROJECT"] == "":
            row["PROJECT"] = "INPUT"

    # Convert the list of rows into a DataFrame
    df = pd.DataFrame(rows)

    # Save as Excel or CSV
    if  os.path.dirname(output_path) not in [".", ""]:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
    if excel:
        df.to_excel(output_path, index=False)
    else:
        df.to_csv(output_path, index=False)

    return output_path


def create_config_from_table(
    table_path: str,
    output_path: str,
    proj_paths: dict[str, str],
    jobs: dict = None,
    sequencings: dict[str, str] = None
) -> str:
    """
    Create a YAML config from a table. Supports SAMPLES and optional INPUT files.

    Parameters
    ----------
    table_path : str
        Path to the input CSV or Excel table.
    output_path : str
        Path to write the YAML config.
    proj_paths : dict
        Dictionary of project_name -> project_path.
    jobs : dict, optional
        Default JOBS settings (CORES_PER_JOBS, QOS_INFOS).
    sequencings : dict
        Dictionary of sequencings informations (PATH, R1_ADAPTOR, R2_ADAPTOR).

    Returns
    -------
    str
        Path to the written YAML config file.
    """

    # Load table
    if os.path.splitext(table_path)[1] == ".csv":
        df = pd.read_csv(table_path)
    elif os.path.splitext(table_path)[1] in {".xls", ".xlsx"}:
        df = pd.read_excel(table_path)
    else:
        raise ValueError(f"Unsupported table format: {os.path.splitext(table_path)[1]}")

    # Check required columns
    required_cols = {"SAMPLE", "SEQUENCING", "PROJECT", "TYPE", "STRAND", "PATH"}
    missing_cols = required_cols - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    # Initialize config
    config = {"SEQUENCING": {}}
    if jobs:
        config["JOBS"] = jobs

    # Initialize the PROJECTS field
    config["PROJECTS"] = {}

    # Iterate over each row and populate the config
    for _, row in df.iterrows():
        sample_name = row["SAMPLE"]
        seq_name = row["SEQUENCING"]
        proj_name = row["PROJECT"]
        mark = row["TYPE"]
        strand = row["STRAND"]
        sample_path = row["PATH"]

        # Get the sequencing path for the current sequencing project
        sequencing = sequencings.get(seq_name, "")
        proj_path = proj_paths.get(proj_name, "")

        # If the sequencing project is not in the config, initialize it
        if seq_name not in config["SEQUENCING"]:
            config["SEQUENCING"][seq_name] = {"SAMPLES": {}}
            config["SEQUENCING"][seq_name].update(sequencing)

        # Determine if the sample is an INPUT or regular SAMPLE
        if proj_name == "INPUT":
            if "INPUT" not in config["SEQUENCING"][seq_name].keys():
                config["SEQUENCING"][seq_name]["INPUT"] = {}
            target_dict = config["SEQUENCING"][seq_name]["INPUT"]
        else:
            target_dict = config["SEQUENCING"][seq_name]["SAMPLES"]

        # Normalize the sample path (remove the sequencing root path and make it relative to the sequencig folder)
        try:
            if os.path.isabs(sample_path):
                # Remove the sequencing path portion from the sample path
                sample_path = sample_path[len(sequencing["PATH"]):]
        except ValueError:
            # Path is outside project; keep absolute and warn
            warnings.warn(f"Sample path {sample_path} does not start with the expected sequencing path {sequencing['PATH']}, keeping absolute path")

        # Initialize sample entry
        target_dict.setdefault(sample_name, {})

        # Add R1 and R2 paths for this sample
        if strand == "R1":
            target_dict[sample_name]["R1"] = sample_path
        elif strand == "R2":
            target_dict[sample_name]["R2"] = sample_path

        # If it's not an input sample, set the TYPE
        if proj_name != "INPUT":
            target_dict[sample_name]["TYPE"] = mark

        # Add the project to the PROJECTS section (only if the project is not INPUT)
        if proj_name != "INPUT":
            if proj_name not in config["PROJECTS"]:
                config["PROJECTS"][proj_name] = {
                    "PROJECT_PATH": proj_path,
                    "TYPE": mark,
                    "MIN_SAMPLES_FOR_PEAKS": 2,
                    "SEQUENCING": []  # Initialize the list for sequencing projects
            }
            # Add the sequencing project to the list of associated sequencing projects
            if seq_name not in config["PROJECTS"][proj_name]["SEQUENCING"]:
                config["PROJECTS"][proj_name]["SEQUENCING"].append(seq_name)

    #config = check_project_and_sequencing(config)
    with open(output_path, "w", encoding="utf-8") as fh:
        yaml.safe_dump(config, fh, sort_keys=False, default_flow_style=False)

    return output_path


def check_sample_files_exist(config_path: str) -> bool:
    """
    Check if all R1 and R2 FASTQ files listed in the config exist.

    Parameters
    ----------
    config_path : str
        Path to the YAML config file.

    Returns
    -------
    bool
        True if all R1 and R2 files exist, False otherwise.
    """
    # Load YAML config
    with open(config_path, "r", encoding="utf-8") as fh:
        config = yaml.safe_load(fh)

    all_exist = True

    # Check the SEQUENCING section
    sequencing_data = config.get("SEQUENCING", {})

    for seq_name, seq_data in sequencing_data.items():
        samples = seq_data.get("SAMPLES", {})
        sample_path = seq_data.get("PATH", "")

        for sample_name, sample_data in samples.items():
            # R1 and R2 paths
            r1_path = sample_data.get("R1")
            r2_path = sample_data.get("R2")

            # Check if R1 exists
            if r1_path:
                r1_path = sample_path + r1_path
              #  if platform.system() == "Windows":
              #      r1_path = r1_path.replace(os.sep, "/")
                if not os.path.exists(r1_path):
                    warnings.warn(f"Sample '{sample_name}' in sequencing '{seq_name}': R1 file '{r1_path}' does not exist.")
                    all_exist = False

            # Check if R2 exists
            if r2_path:
                r2_path = sample_path + r2_path
                if not os.path.exists(r2_path):
                    warnings.warn(f"Sample '{sample_name}' in sequencing '{seq_name}': R2 file '{r2_path}' does not exist.")
                    all_exist = False

    return all_exist













