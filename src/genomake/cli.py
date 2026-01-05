import argparse # used to parse the cmd
import subprocess
from pathlib import Path

# --- Command handler functions ---

def _cmd_chromake_pipeline(args):
    pipeline_dir = Path(__file__).parent / "pipelines/chromake"
    cmd = [
        "snakemake",
        "--snakefile", str(pipeline_dir / "Snakefile"),
        "--configfile", args.config_path,
        "--retries 3" # try to retry 3 time in case there an error
    ]
    if args.cores <= 0:
        print("--cores was set to a value inferior or equal to 0. Defaulting to 1")
        cmd.append("--cores 1")
    else:
        cmd.append(f"--cores {args.cores}")
    if args.jobs <= 0:
        print("--jobs was set to a value inferior or equal to 0. Defaulting to 1")
        cmd.append("--jobs 1")
    else:
        cmd.append(f"--jobs {args.jobs}")
    if args.others_snakemake != "":
        cmd.append(args.others_snakemake)
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
        help="Maximum number of jobs to run concurrently. Default to 5."
    )
    parser_chromake.add_argument(
        "--cores", type=int, default=1,
        help="Number of cores used by snakemake (set the argument with the same name). Not relevant if we use an executor like slurm. Default to 1."
    )
    parser_chromake.add_argument(
        "--others-snakemake", type=str, default="",
        help="Other arguments for the snakemake command. Can be used to set the default value for an executor like slurm. Default to ''"
    )
    # --executor slurm --default-resources --slurm-delete-logfiles-older-than 0 --slurm-logdir "logs"
    parser_chromake.add_argument(
        "--print-only", "-p", action="store_true", default=False,
        help="Only print the final snakemake command. Default to 5"
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

