#!/usr/bin/env python

# author: fschischlik
# submit script for slurm cluster

import argparse
import os
import getpass
from slurm.slurm_parse_sample_file import slurm_id_sample_files
from slurm.slurm_write_sh_files import write_sh_files


def load_modules():

    modules = "module load bowtie/2.2.4\n" \
              + "module load boost/1.55\n" \
              + "module load tophat/2.0.13\n" \
              + "\n"

    return modules


def slurm_cmd(sample_dir, each_sample,
              output_dir, cpus_per_task,
              genome_ref):

    modules = load_modules()

    cmd = modules \
          + "tophat2 \\\n" \
          + "-o " + output_dir + "/" + "tophat_" + each_sample \
          + "-p " + cpus_per_task \
          + "--fusion-search \\\n" \
          + "--keep-fasta-order \\\n" \
          + "--bowtie1 \\\n" \
          + "--no-coverage-search \\\n" \
          + "-r 0 \\\n" \
          + "--mate-std-dev 80 \\\n" \
          + "--max-intron-length 100000 \\\n" \
          + "--fusion-min-dist 100000 \\\n" \
          + "--fusion-anchor-length 13 \\\n" \
          + "--fusion-ignore-chromosomes chrM \\\n" \
          + genome_ref \
          + sample_dir + "/" + each_sample + "_R1.fastq" + " \\\n"\
          + sample_dir + "/" + each_sample + "_R2.fastq"

    return cmd


def run_post(cpus_per_task, genome_ref):

    modules = load_modules()
    cmd_post = modules \
               + "tophat-fusion-post \\\n" \
               + "-p" + cpus_per_task \
               + "--num-fusion-reads 1 " \
               + "--num-fusion-pairs 2 " \
               + "--num-fusion-both 5 " \
               + "--tex-table" \
               + genome_ref

    return cmd_post


if __name__ == '__main__':
    # required arguments
    parser = argparse.ArgumentParser(description='slurm_tophatfusion.py')
    parser.add_argument('--debug', required=False, type=int, help='Debug level')
    parser.add_argument('--post', action="store_true",
                        help="Run tophat-fusion-post", )
    parser.add_argument('--sample_file', required=False, type=str,
                        help='sample file FORMAT:  UPD (unique patient ID')
    parser.add_argument('--prefix', required=False, type=str,
                        help="prefix of output file")
    parser.add_argument('--sample_dir', required=False, type=str,
                        help="sample directory")
    parser.add_argument('--exec_dir', required=False, type=str,
                        help="exec_dir")
    parser.add_argument('--output_dir', required=False, type=str,
                        help="output_dir")
    parser.add_argument('--tophatfusion_ref', required=False, type=str,
                        help="reference databases for tophatfusion")
    parser.add_argument('--cpus_per_task', required=False, type=str, default=1,
                        help='number of cpus per task (default: %(default)s)')
    parser.add_argument('--ntasks', required=False, type=str, default=1,
                        help='number of tasks (default: %(default)s)')
    parser.add_argument('--mem', required=False, type=str, default=8000,
                        help='memory usage in MB (default: %(default)s)')
    parser.add_argument('--time', required=False, type=str, default="2:00:00",
                        help='FORMAT: HH:MM:SS (default: %(default)s)')
    parser.add_argument('--queue', required=False, type=str, default="mediumq",
                        choices=["shortq", "mediumq", "longq"],
                        help='cluster queue/partition (default: %(default)s)')
    parser.add_argument('--account', required=False, type=str, help='username')

    args = parser.parse_args()
    home_dir = os.getenv("HOME")

    if not args.cpus_per_task:
        args.cpus_per_task = str("1")
    if not args.ntasks:
        args.ntasks = str("1")
    if not args.mem:
        args.mem = str("8000")
    if not args.time:
        args.time = "2:0:0"
    if not args.queue:
        args.queue = "mediumq"
    if not args.account:
        args.account = getpass.getuser()
    if not args.output_dir:
        args.output_dir = os.getcwd()
    if not args.sample_dir:
        args.sample_dir = os.getcwd()
    if not args.exec_dir:
        args.exec_dir = home_dir + "/bin/tophat"
    if not args.prefix:
        args.prefix = "SAMPLE"
    if not args.tophatfusion_ref:
        args.tophatfusion_ref = home_dir + "/hg19"

    print args

    if args.post:
        cmd = run_post(str(args.cpus_per_task),
                       args.genome_ref)

    else:
        # read in sample file
        sample_list = slurm_id_sample_files(args.sample_file)

        for each_sample in sample_list:

            print each_sample

            # create output_dir
            output_dir = args.output_dir + "/" + "tophat_" +each_sample
            if not os.path.exists(output_dir):
            os.makedirs(output_dir)

            cmd = slurm_cmd(args.sample_dir, each_sample,
                        args.output_dir, str(args.cpus_per_task),
                        args.tophatfusion_ref)

    write_sh_files(each_sample, str(args.ntasks), str(args.cpus_per_task),
                   str(args.mem), args.time, args.queue, args.account,
                   args.output_dir, args.prefix, cmd)