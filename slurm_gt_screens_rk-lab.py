#!/cm/shared/apps/python/2.7.6/bin/python
# -*- coding: utf-8 -*-

import os
import argparse
import getpass
from slurm.slurm_parse_sample_file import slurm_tab_sample_files
from slurm.slurm_write_sh_files import write_sh_files


def slurm_cmd(sample_dir, sample_name, screen_name, ref_genome):
        
    cmd = "BaF3_screen_workflow.sh " + "\\\n" \
        + "-i " + sample_dir + "/" + sample_name + " \\\n" \
        + "-s " + screen_name + " \\\n" \
        + "-g " + ref_genome + "\n"

    return cmd


if __name__ == '__main__':
    # required arguments
    parser = argparse.ArgumentParser(description='slurm_gt_screens_rk-lab.py')
    parser.add_argument('--debug', required=False, type=int, help='Debug level')
    parser.add_argument('--sample_file', required=True, type=str,
                        help='sample file FORMAT: ')
    parser.add_argument('--prefix', required=False, type=str,
                        help="prefix of output file")
    parser.add_argument('--output_dir', required=False, type=str,
                        help="output_dir")
    parser.add_argument('--cpus_per_task', required=False, type=str, default=1,
                        help='number of cpus per task (default: 4 %(default)s)')
    parser.add_argument('--ntasks', required=False, type=str, default=1,
                        help='number of tasks (default: 1 %(default)s)')
    parser.add_argument('--mem', required=False, type=str, default=6000,
                        help='memory usage in MB (default: %(default)s)')
    parser.add_argument('--time', required=False, type=str, default="10:00:00",
                        help='FORMAT: HH:MM:SS (default: %(default)s)')
    parser.add_argument('--queue', required=False, type=str, default="mediumq",
                        choices=["shortq", "mediumq", "longq"],
                        help='cluster queue/partition (default: %(default)s)')
    parser.add_argument('--account', required=False, type=str, help='username')

    args = parser.parse_args()

    if not args.cpus_per_task:
        args.cpus_per_task = str("4")
    if not args.ntasks:
        args.ntasks = str("1")
    if not args.mem:
        args.mem = str("6000")
    if not args.time:
        args.time = "10:0:0"
    if not args.queue:
        args.queue = "mediumq"
    if not args.account:
        args.account = getpass.getuser()
    if not args.output_dir:
        args.output_dir = os.getcwd()
    if not args.prefix:
        args.prefix = "SAMPLE"

    print args

    #run
    samples = slurm_tab_sample_files(args.sample_file)

    for each_sample in samples:
        job_name = each_sample[0]
        sample_dir = each_sample[3].rsplit("/",1)[0]
        sample_name = each_sample[3].rsplit("/",1)[1]
        cmd = slurm_cmd(sample_dir, sample_name, 
            screen_name=each_sample[0], ref_genome=each_sample[2])
        print job_name
        print cmd
        write_sh_files(job_name, args.ntasks, args.cpus_per_task, args.mem,
                       args.time, args.queue, args.account,
                       args.output_dir, args.prefix, cmd)
