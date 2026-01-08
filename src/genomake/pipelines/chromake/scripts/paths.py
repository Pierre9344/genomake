from pathlib import Path
import yaml
import re

def load_config(path):
    with open(path) as f:
        return yaml.safe_load(f)

def get_all_fastq_related_paths(cfg: dict, mode: str):
    res = []
    for sequencing_name, sequencing_data in cfg["SEQUENCING"].items():
        base = Path(sequencing_data["PATH"])
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
                res.append(base / "QC/FASTQC/RAW" / re.sub(r"\.fastq(\.gz)?$", "_fastqc.html", Path(sample["R1"]).name))
                res.append(base / "QC/FASTQC/RAW" / re.sub(r"\.fastq(\.gz)?$", "_fastqc.html", Path(sample["R2"]).name))
            for inp in sequencing_data.get("INPUT", {}).values():
                res.append(base / "QC/FASTQC/RAW" / re.sub(r"\.fastq(\.gz)?$", "_fastqc.html", Path(inp["R1"]).name))
                res.append(base / "QC/FASTQC/RAW" / re.sub(r"\.fastq(\.gz)?$", "_fastqc.html", Path(inp["R2"]).name))
        elif mode == "multiqc_raw":
            res.append(base / "QC/MULTIQC/RAW/multiqc_report.html")
        elif mode == "cutadapt":
            for sample in sequencing_data.get("SAMPLES", {}).values():
                res.append(base / "TRIMMED" / Path(sample["R1"]).name)
                res.append(base / "TRIMMED" / Path(sample["R2"]).name)
            for inp in sequencing_data.get("INPUT", {}).values():
                res.append(base / "TRIMMED" / Path(inp["R1"]).name)
                res.append(base / "TRIMMED" / Path(inp["R2"]).name)
        elif mode == "fastqc_trimmed":
            for sample in sequencing_data.get("SAMPLES", {}).values():
                res.append(base / "QC/FASTQC/TRIMMED" / re.sub(r"\.fastq(\.gz)?$", "_fastqc.html", Path(sample["R1"]).name))
                res.append(base / "QC/FASTQC/TRIMMED" / re.sub(r"\.fastq(\.gz)?$", "_fastqc.html", Path(sample["R2"]).name))
            for inp in sequencing_data.get("INPUT", {}).values():
                res.append(base / "QC/FASTQC/TRIMMED" / re.sub(r"\.fastq(\.gz)?$", "_fastqc.html", Path(inp["R1"]).name))
                res.append(base / "QC/FASTQC/TRIMMED" / re.sub(r"\.fastq(\.gz)?$", "_fastqc.html", Path(inp["R2"]).name))
        elif mode == "multiqc_trimmed":
            res.append(base / "QC/MULTIQC/TRIMMED/multiqc_report.html")
        elif mode == "bam":
            for sample_name, sample_data in sequencing_data["SAMPLES"].items():
                res.append(base / "BAM" / (sample_name + ".bam"))
        elif mode == "bedgraph":
            res.append(base / "HOMER" / (sequencing_name + ".bedgraph"))
        else:
            print(f"There is an error, chromake.scripts.path.get_path dont recognize the {mode} mode!")      
    return res
        
def get_sequencing_fastq_related_paths(cfg: dict,
                                       project_name: str,
                                       mode: str):
    res = []
    if project_name in cfg["SEQUENCING"].keys():
        base = Path(cfg["SEQUENCING"][project_name]["PATH"])
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
                res.append(base / "QC/FASTQC/RAW" / re.sub(r"\.fastq(\.gz)?$", "_fastqc.html", Path(sample["R1"]).name))
                res.append(base / "QC/FASTQC/RAW" / re.sub(r"\.fastq(\.gz)?$", "_fastqc.html", Path(sample["R2"]).name))
            for inp in cfg["SEQUENCING"][project_name].get("INPUT", {}).values():
                res.append(base / "QC/FASTQC/RAW" / re.sub(r"\.fastq(\.gz)?$", "_fastqc.html", Path(inp["R1"]).name))
                res.append(base / "QC/FASTQC/RAW" / re.sub(r"\.fastq(\.gz)?$", "_fastqc.html", Path(inp["R2"]).name))
        elif mode == "multiqc_raw":
            res.append(base / "QC/MULTIQC/RAW/multiqc_report.html")
        
        elif mode == "cutadapt":
            for sample in cfg["SEQUENCING"][project_name].get("SAMPLES", {}).values():
                res.append(base / "TRIMMED" / Path(sample["R1"]).name)
                res.append(base / "TRIMMED" / Path(sample["R2"]).name)
            for inp in cfg["SEQUENCING"][project_name].get("SAMPLES", {}).values():
                res.append(base / "TRIMMED" / Path(inp["R1"]).name)
                res.append(base / "TRIMMED" / Path(inp["R2"]).name)
        elif mode == "fastqc_trimmed":
            for sample in cfg["SEQUENCING"][project_name].get("SAMPLES", {}).values():
                res.append(base / "QC/FASTQC/TRIMMED" / re.sub(r"\.fastq(\.gz)?$", "_fastqc.html", Path(sample["R1"]).name))
                res.append(base / "QC/FASTQC/TRIMMED" / re.sub(r"\.fastq(\.gz)?$", "_fastqc.html", Path(sample["R2"]).name))
            for inp in cfg["SEQUENCING"][project_name].get("SAMPLES", {}).values():
                res.append(base / "QC/FASTQC/TRIMMED" / re.sub(r"\.fastq(\.gz)?$", "_fastqc.html", Path(inp["R1"]).name))
                res.append(base / "QC/FASTQC/TRIMMED" / re.sub(r"\.fastq(\.gz)?$", "_fastqc.html", Path(inp["R2"]).name))
        elif mode == "multiqc_trimmed":
            res.append(base / "QC/MULTIQC/TRIMMED/multiqc_report.html")
        elif mode == "bam":
            for sample_name, sample_data in cfg["SEQUENCING"][project_name]["SAMPLES"].items():
                res.append(base / "BAM" / (sample_name + ".bam"))
            for input_name, sample_data in cfg["SEQUENCING"][project_name]["INPUT"].items():
                res.append(base / "BAM" / (input_name + ".bam"))
    else:
        print(f"There is an error, the configuration file don't contains a {project_name} project!")
    return res


