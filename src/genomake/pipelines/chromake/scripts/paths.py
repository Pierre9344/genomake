from pathlib import Path
import yaml

def load_config(path):
    with open(path) as f:
        return yaml.safe_load(f)

def get_all_fastq_related_paths(cfg: dict,
                            mode: str):
    res = []
    for sequencing_name, sequencing_data in cfg["SEQUENCING"].items():
        base = Path(sequencing_data["SAMPLE_PATH"])
        if mode == "sequencing":
            res.append(base)
        elif mode == "fastq_raw":
            for sample in sequencing_data.get("SAMPLES", {}).values():
                res.append(base / sample["R1"])
                res.append(base / sample["R2"])
            for inp in sequencing_data.get("INPUT", {}).values():
                res.append(base / inp["R1"])
                res.append(base / inp["R2"])
        elif mode == "fastqc_raw":
            for sample in sequencing_data.get("SAMPLES", {}).values():
                res.append(base / "QC/FASTQC/RAW" / sample["R1"].replace(".gz", ".html"))
                res.append(base / "QC/FASTQC/RAW" / sample["R2"].replace(".gz", ".html"))
            for inp in sequencing_data.get("INPUT", {}).values():
                res.append(base / "QC/FASTQC/RAW" / inp["R1"].replace(".gz", ".html"))
                res.append(base / "QC/FASTQC/RAW" / inp["R2"].replace(".gz", ".html"))
        elif mode == "multiqc_raw":
            res.append(base / "QC/RAW/multiqc_report.html")
        else:
            print(f"There is an error, chromake.scripts.path.get_path dont recognize the {mode} mode!")      
    return res
        
def get_sequencing_fastq_related_paths(cfg: dict,
                                       project_name: str,
                                       mode: str):
    res = []
    if project_name in cfg["SEQUENCING"].keys():
        base = Path(cfg["SEQUENCING"][project_name]["SAMPLE_PATH"])
        if mode == "sequencing":
            res.append(base)
        elif mode == "fastq_raw":
            for sample in cfg["SEQUENCING"][project_name].get("SAMPLES", {}).values():
                res.append(base / sample["R1"])
                res.append(base / sample["R2"])
            for inp in cfg["SEQUENCING"][project_name].get("INPUT", {}).values():
                res.append(base / inp["R1"])
                res.append(base / inp["R2"])
        elif mode == "fastqc_raw":
            for sample in cfg["SEQUENCING"][project_name].get("SAMPLES", {}).values():
                res.append(base / "QC/FASTQC/RAW" / sample["R1"].replace(".gz", ".html"))
                res.append(base / "QC/FASTQC/RAW" / sample["R2"].replace(".gz", ".html"))
            for inp in cfg["SEQUENCING"][project_name].get("INPUT", {}).values():
                res.append(base / "QC/FASTQC/RAW" / inp["R1"].replace(".gz", ".html"))
                res.append(base / "QC/FASTQC/RAW" / inp["R2"].replace(".gz", ".html"))
        elif mode == "multiqc_raw":
            res.append(base / "QC/RAW/multiqc_report.html")
    else:
        print(f"There is an error, the configuration file don't contains a {project_name} project!")
    return res
