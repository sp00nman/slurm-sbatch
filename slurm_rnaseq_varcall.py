#!/cm/shared/apps/python/2.7.6/bin/python
# -*- coding: utf-8 -*-

import getpass
import os
import argparse
from slurm.slurm_parse_sample_file import slurm_dir_sample_files
from slurm.slurm_write_sh_files import write_sh_files
from slurm.slurm_parse_region_file import slurm_read_region_file


def slurm_cmd(stage, sample_dir,
              sample_name, prefix,
              exec_dir, output_dir,
              job_name, genome,
              gene, region):

    cmd = exec_dir + "/rnaseq_varcall.py " + " \\\n" \
        + "--stage " + stage + " \\\n" \
        + "--project_name " + prefix + "_" + job_name + "_" + gene + " \\\n" \
        + "--input_file " + sample_name + " \\\n" \
        + "--sample_dir " + sample_dir + " \\\n" \
        + "--output_dir " + output_dir + " \\\n" \
        + "--ref_genome " + genome + " \\\n" \
        + "--region " + region + " \\\n\n"
    return cmd


if __name__ == "__main__":

    # required arguments
    parser = argparse.ArgumentParser(description='slurm_rnaseq_varcall.py')
    parser.add_argument('--debug', required=False, type=int, help='Debug level')
    parser.add_argument('--stage', required=False, type=int, help='stage')
    parser.add_argument('--sample_file', required=True, type=str,
                        help='sample file FORMAT:  path/to/sample/file')
    parser.add_argument('--prefix', required=False, type=str,
                        help="prefix of output file")
    parser.add_argument('--output_dir', required=False, type=str,
                        help="output_dir")
    parser.add_argument('--exec_dir', required=False, type=str, help='exec_dir')
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
    parser.add_argument('--region_file', required=True, type=str,
                        help='region file gene chr:start-end')
    parser.add_argument('--genome', required=False, type=str,
                        help='path to genome version')

    args = parser.parse_args()

    if not args.stage:
        args.stage = "all"
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
        args.genome = "hg19.fa"
    if not args.region_file:
        args.region_file = "region_file.txt"

    print args

    # read in sample file
    # /path/to/sample/file
    # /path/to/nextsample/file
    samples = slurm_dir_sample_files(args.sample_file)

    # read in gene region file
    # ADAMTS17  15:99971589-100342005
    # gene will be part of job_name ; not needed to extract region
    gene_regions = slurm_read_region_file(args.region_file)

    for each_sample in samples:
        print "processing sample " + str(each_sample[1])
        cmd = ""
        # eg CEMM_05
        job_name = each_sample[1].rsplit("_")[0] + "_" + \
                   each_sample[1].rsplit("_")[1]
        # create output_dir
        output_dir = args.output_dir + "/" + job_name
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        # eg. /path/to/samplefile --> withough "/"
        sample_dir = each_sample[0]
        # eg. CEMM_05_accepted_hits.bam
        sample_name = each_sample[1]

        for gene_region in gene_regions:
            gene = gene_region[0]
            region = gene_region[1]
            gene_cmd = slurm_cmd(args.stage, sample_dir,
                                 sample_name, args.prefix,
                                 args.exec_dir, output_dir,
                                 job_name, args.genome,
                                 gene, str(region))
            cmd += gene_cmd

        write_sh_files(job_name, str(args.ntasks),
                       str(args.cpus_per_task), str(args.mem),
                       args.time, args.queue,
                       args.account, output_dir,
                       args.prefix, cmd)
