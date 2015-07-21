#!/cm/shared/apps/python/2.7.6/bin/python
# -*- coding: utf-8 -*-

import os
import argparse
import getpass
from slurm.slurm_parse_sample_file import slurm_tab_sample_files
from slurm.slurm_write_sh_files import write_sh_files


def slurm_cmd(stage, prefix, job_name, output_dir,
              sequences_dir, sample_name, exec_dir,
              genome_version, genome,
              bowtie_version, annotation,
              control_file, refseq_file, cpus_per_task):

    cmd = exec_dir + "/" + "gt_screen_workflow.py " + " \\\n" \
          + "--debug 0 " + " \\\n" \
          + "--stage " + stage + " \\\n" \
          + "--project_name " + job_name + " \\\n" \
          + "--output_dir " + output_dir + " \\\n" \
          + "--sequences_dir " + sequences_dir + " \\\n" \
          + "--sample_file " + sample_name + " \\\n" \
          + "--genome_version " + genome_version + " \\\n" \
          + "--genomes " + genome + " \\\n" \
          + "--bowtie2 " + bowtie_version + " \\\n" \
          + "--annotation " + annotation + " \\\n" \
          + "--control_file " + control_file + " \\\n" \
          + "--refseq_file " + refseq_file + " \\\n" \
          + "--num_cpus " + str(cpus_per_task) + "\n"

    return cmd


if __name__ == '__main__':
    # required arguments
    parser = argparse.ArgumentParser(description='slurm_gt_screens_rk-lab.py')
    parser.add_argument('--debug', required=False, type=int, help='Debug level')
    parser.add_argument('--stage', required=False, type=str, default="all",
            help='Analysis steps: [all,alignment,filter,sort,duplicates,index,insertions,annotate,count,fisher,plot], defaults: %(default)s')
    parser.add_argument('--sample_file', required=True, type=str,
                        help='sample file FORMAT: AF_H2O2_run1 afauster hg19 /path/to/sample/file ')
    parser.add_argument('--prefix', required=False, type=str,
                        help="prefix of output file")
    parser.add_argument('--output_dir', required=False, type=str,
                        help="output_dir")
    parser.add_argument('--exec_dir', required=False, type=str, help='exec_dir')
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
    parser.add_argument('--genomes', required=False, type=str,
                        help='path to genome version')
    parser.add_argument('--genome_version', required=False, type=str,
                        help='Genome version')
    parser.add_argument('--bowtie2', required=False, type=str,
                        help='Bowtie version')
    parser.add_argument('--annotation', dest='annotation', required=False,
                        help='Annotation file.')
    parser.add_argument('--control_file', dest='control_file', required=False,
                        help='Control file with insertions for fisher-test.')
    parser.add_argument('--refseq_file', dest='refseq_file', required=False,
                        help='Refseq file with start & end position of gene.')
    
    args = parser.parse_args()

    if not args.cpus_per_task:
        args.cpus_per_task = str("1")
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
    if not args.genomes:
        args.genomes = "hg19.fa"
    if not args.bowtie2:
        args.bowtie2 = "bowtie2"
    if not args.refseq_file:
        args.refseq_file = "All_genes_data_ct_srt_sed.txt"
    if not args.control_file:
        args.control_file="HAP1_insertions.txt"

    print args

    #run
    samples = slurm_tab_sample_files(args.sample_file)
    for each_sample in samples:
        job_name = each_sample[0]
        sample_dir = each_sample[3].rsplit("/",1)[0]
        sample_name = each_sample[3].rsplit("/",1)[1]
        cmd = slurm_cmd(args.stage, args.prefix, job_name, args.output_dir,
                        sample_dir, sample_name, args.exec_dir,
                        args.genome_version, args.genomes,
                        args.bowtie2, args.annotation,
                        args.control_file, args.refseq_file,
                        str(args.cpus_per_task))
        print job_name
        print cmd
        write_sh_files(job_name, str(args.ntasks), str(args.cpus_per_task), str(args.mem),
                       str(args.time), args.queue, args.account,
                       args.output_dir, args.prefix, cmd)
