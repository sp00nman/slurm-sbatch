#!/cm/shared/apps/python/2.7.6/bin/python
# -*- coding: utf-8 -*-

import os
import getpass
import argparse
from slurm.slurm_parse_sample_file import slurm_tab_sample_files
from slurm.slurm_write_sh_files import write_sh_files


def slurm_cmd(sample_dir, sample_name, screen_name):

    cmd = "genetrap_screen_analysis.sh " + "\\\n" \
          + "-i " + sample_name + " \\\n" \
          + "-s " + screen_name + " \\\n" \
          + "-d " + sample_dir + "\n"

    return cmd


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='slurm_gt_screens_tb-lab.py')
    parser.add_argument('--debug', required=False, type=int, help='Debug level')
    parser.add_argument('--sample_file', required=True, type=str,
                        help='sample file FORMAT:  path/to/sample/file')
    parser.add_argument('--prefix', required=False, type=str,
                        help="prefix of output file")
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
    parser.add_argument('--output_dir', required=False, type=str, help='output directory')
    parser.add_argument('--genome', required=False, type=str,
                        help="Reference genome; default hg18")

    args = parser.parse_args()

    if not args.cpus_per_task:
        args.cpus_per_task = str("1")
    if not args.ntasks:
        args.ntasks = str("1")
    if not args.mem:
        args.mem = str("10000")
    if not args.time:
        args.time = "1:0:0"
    if not args.queue:
        args.queue = "shortq"
    if not args.account:
        args.account = getpass.getuser()
    if not args.output_dir:
        args.output_dir = os.getcwd()
    if not args.prefix:
        args.prefix = "SAMPLE"
    if not args.genome:
        args.genome = "hg18"

    samples = slurm_tab_sample_files(args.sample_file)

    for each_sample in samples:
        job_name = each_sample[0]
        sample_dir = each_sample[3].rsplit("/", 1)[0]
        sample_name = each_sample[3].rsplit("/", 1)[1]
        cmd = slurm_cmd(sample_dir, sample_name,
                        screen_name=each_sample[0])
        if args.debug:
            print job_name
            print cmd
        write_sh_files(job_name, str(args.ntasks), str(args.cpus_per_task),
                       str(args.mem), str(args.time), args.queue, args.account,
                       args.output_dir, args.prefix, cmd)
