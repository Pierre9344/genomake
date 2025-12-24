import argparse # used to parse the cmd
import subprocess
from pathlib import Path

# --- Command handler functions ---

def _cmd_chromake_pipeline(args):
    pipeline_dir = Path(__file__).parent / "pipelines/chromake"


    cmd = [
        "snakemake",
        "--snakefile", str(pipeline_dir / "Snakefile"),
        "--cores", "1",
        "--configfile", args.config_path,
        "--retries ", 3 #♥ try to retry 3 time in case there an error
    ]
    
    if args.jobs <= 0:
        print("--jobs was set to a value inferior or equal to 0. Defaulting to 1")
        cmd.append("--jobs 1")
    else:
        cmd.append(f"--jobs {args.jobs}")

    
    if args.executor == "slurm":
        " ".join(cmd, " --executor slurm")
        value_for_default = ""
        if args.slurm_account != "":
            value_for_default = f"slurm_account={args.slurm_account}"
        if args.runtime <= 0:
            print("--runtime was set to a value inferior or equal to 0. Ignoring it for the snakemake command.")
            if len(value_for_default) > 0:
                value_for_default += ","
            value_for_default += "runtime=120"
        else:
            if len(value_for_default) > 0:
                value_for_default += ","
            value_for_default += f"runtime={args.runtime}"
        
        if args.clusters != "":
            if len(value_for_default) > 0:
                value_for_default += ","
            value_for_default += f"clusters={args.clusters}"
    
        if args.memory <= 0:
            print("--memory was set to a value inferior or equal to 0. Ignoring it for the snakemake command and using default rules values.")
        else:
            if len(value_for_default) > 0:
                value_for_default += ","
            value_for_default += f"mem_mb={args.memory}"
        if args.other_default != "":
            if len(value_for_default) > 0:
                value_for_default += ","
            value_for_default += f"{args.other_default}"
        cmd.append(value_for_default)
    elif args.executor != "":
        cmd.append(f"--executor {args.executor}")
    if args.other_snakemake != "":
        cmd.append(args.other_snakemake)
    if args.print_only:
        print(f"Final snakemake command is: {' '.join(cmd)}")
    else:
        subprocess.run(cmd, check=True)

# --- CLI setup ---

def main():
    parser = argparse.ArgumentParser(
        description="genomake CLI: pipelines to analyze genomic sequencing data"
    )
    
    # Subcommands
    subparsers = parser.add_subparsers(title="commands", dest="command")
    
    # chromake pipeline
    parser_chromake = subparsers.add_parser(
        "chromake", help="Run the chromake pipeline to align ChIP and ATAC sequencing data and identify enriched peaks. Can be run locally or on a slurm cluster."
    )
    parser_chromake.add_argument(
        "--config-path", "-c", type=str, required=True,
        help="Path to the configuration file. See 'genomake.pipelines.chromake.scripts.config.create_example_config()' for an example. This python module also contains a function to generate one from a samplesheet."
    )
    parser_chromake.add_argument(
        "--jobs", "-j", type=int, default=5,
        help="Maximum number of jobs to run concurrently."
    )
    parser_chromake.add_argument(
        "--cores", type=int, default=5,
        help="Number of cores used by snakemake (set the argument with the same name). Not relevant if we use an executor like slurm."
    )
    parser_chromake.add_argument(
        "--executor", "-e", type=str, default="slurm",
        help="Executor to use when launching jobs on performance compute clusters (See https://snakemake.github.io/snakemake-plugin-catalog/plugins/executor/slurm.html). Currently only accept slurm. If you want to use another executor, indicate the name with this argument and set the other parameters with --others."
    )
    parser_chromake.add_argument(
        "--slurm-account", type=str, default="",
        help="Account name associated to the job allocation (used for slurm only). Used only if executor is slurm."
    )
    parser_chromake.add_argument(
        "--runtime", "-r", type=int, default=120,
        help="Jobs max time in minutes. Default to 120 minutes. Please note that some rules may be configured to use more time unless the runtime is set as an higher value than the rule default). Used only if executor is slurm."
    )
    parser_chromake.add_argument(
        "--clusters", type=str, default="",
        help="Same as --clusters for sbatch jobs (e.g. nautilus for the Glicid cluster). Used only if executor is slurm."
    )
    parser_chromake.add_argument(
        "--memory", "-m", type=int, default=2000,
        help="Same as --mem for sbatch jobs. Used only if executor is slurm."
    )
    parser_chromake.add_argument(
        "--others-default", type=str, default="",
        help="Other arguments for the snakemake default-ressource values.. Can be used to set the values besides the ones proposed in this API such as slurm-default or values for another executor like SGE."
    )
    parser_chromake.add_argument(
        "--others-snakemake", type=str, default="--default-resources slurm_output=logs/%x_%j.out slurm_error=logs/%x_%j.err",
        help="Other arguments for the snakemake command. Can be used to set the default value for another executor like SGE."
    )
    parser_chromake.add_argument(
        "--print-only", "-p", type=bool, default=False,
        help="Only print the final snakemake command"
    )
    parser_chromake.set_defaults(func=_cmd_chromake_pipeline)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

# --- Entry point ---
if __name__ == "__main__":
    main()

