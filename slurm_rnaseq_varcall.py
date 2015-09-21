#!/cm/shared/apps/python/2.7.6/bin/python
# -*- coding: utf-8 -*-

import getpass
import os
import argparse
from slurm.slurm_parse_sample_file import slurm_paired_sample_files
from slurm.slurm_write_sh_files import write_sh_files
from slurm.slurm_parse_region_file import slurm_read_region_file


def slurm_cmd(exec_dir,
              stage,
              prefix,
              job_name,
              read1,
              read2,
              output_dir,
              star_genome,
              ref_genome,
              gtf,
              known_indels_1000g,
              known_indels_mills,
              dbsnp,
              annovar,
              num_cpus,
              heap_mem):

    cmd = exec_dir + "/rnaseq_varcall.py " + " \\\n" \
        + "--stage " + stage + " \\\n" \
        + "--project_name " + prefix + "_" + job_name + " \\\n" \
        + "--read1 " + read1 + " \\\n" \
        + "--read2 " + read2 + " \\\n" \
        + "--output_dir " + output_dir + " \\\n" \
        + "--star_genome " + star_genome + " \\\n" \
        + "--ref_genome " + ref_genome + " \\\n" \
        + "--gtf " + gtf + " \\\n" \
        + "--known_indels_1000g " + known_indels_1000g + " \\\n" \
        + "--known_indels_mills " + known_indels_mills + " \\\n" \
        + "--dbsnp " + dbsnp + " \\\n" \
        + "--annovar " + annovar + " \\\n" \
        + "--num_cpus " + num_cpus + " \\\n" \
        + "--heap_mem " + heap_mem

    return cmd


if __name__ == "__main__":

    # required arguments
    parser = argparse.ArgumentParser(description='slurm_rnaseq_varcall.py')
    parser.add_argument('--debug', required=False, type=int, help='Debug level')
    parser.add_argument('--stage', required=False, type=str, help='stage')
    parser.add_argument('--sample_file', required=True, type=str,
                        help='sample file '
                             'FORMAT: path/to/sample/file for region or'
                             'FORMAT: path/to/file_R1.fastq \n'
                             '        path/to/file_R2.fastq ...')
    parser.add_argument('--prefix', required=False, type=str,
                        help="prefix of output file")
    parser.add_argument('--output_dir', required=False, type=str,
                        help="output_dir")
    parser.add_argument('--exec_dir', required=False, type=str, help='exec_dir')

    # hardware specific options
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
    parser.add_argument('--heap_mem', dest='heap_mem', required=False,
                        help='Maximum heap size provided to Java. [Xmx[num]g]')

    parser.add_argument('--region_file', required=False, type=str,
                        help='region file gene chr:start-end')
    # aligner options
    parser.add_argument('--star_genome', required=False, type=str,
                        help="Genome directory of star aligner.")
    parser.add_argument('--ref_genome', required=False, type=str,
                        help="reference genome")
    parser.add_argument('--gtf', required=False, type=str,
                        help="gtf file annotation")

    # input files for indel realignment
    # for now at least 2 known indel files have to be provided
    parser.add_argument('--known_indels_1000g', required=False, type=str,
                        help="List of known indel sites [eg. 1000G_phase1.indels.b37.vcf]. ")
    parser.add_argument('--known_indels_mills', required=False, type=str,
                        help="List of known indel sites. [eg. Mills_and_1000G_gold_standard.indels.b37.vcf] ")

    # input files for base recalibration
    parser.add_argument('--dbsnp', required=False, type=str,
                        help="List of known snps.")

    # annovar specific options
    parser.add_argument('--annovar', required=False, type=str,
                        help="Annotate variant with annovar.")

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
    if not args.ref_genome:
        args.genome = "hg19.fa"

    print args

    samples = slurm_paired_sample_files(args.sample_file)

    for each_sample_pair in samples:

        job_name = each_sample_pair[0].rsplit('/') \
            [-1].rstrip('\r\n').rsplit('.')[0]

        print "processing sample " + job_name

        cmd = slurm_cmd(
            exec_dir=args.exec_dir,
            stage=args.stage,
            prefix=args.prefix,
            job_name=job_name,
            read1=each_sample_pair[0].rstrip('\r\n'),
            read2=each_sample_pair[1].rstrip('\r\n'),
            output_dir=args.output_dir,
            star_genome=args.star_genome,
            ref_genome=args.ref_genome,
            gtf=args.gtf,
            known_indels_1000g=args.known_indels_1000g,
            known_indels_mills=args.known_indels_mills,
            dbsnp=args.dbsnp,
            annovar=args.annovar,
            num_cpus=str(args.cpus_per_task),
            heap_mem=args.heap_mem
        )

        write_sh_files(
            job_name=job_name,
            ntasks=str(args.ntasks),
            cpus_per_task=str(args.cpus_per_task),
            mem=str(args.mem),
            time=args.time,
            queue=args.queue,
            account=args.account,
            output_dir=args.output_dir,
            prefix=args.prefix,
            cmd=cmd
        )


    # read in sample file
    # /path/to/sample/file
    # /path/to/nextsample/file
    # samples = slurm_dir_sample_files(args.sample_file)
    #
    # # read in gene region file
    # # ADAMTS17  15:99971589-100342005
    # # gene will be part of job_name ; not needed to extract region
    # gene_regions = slurm_read_region_file(args.region_file)
    #
    # for each_sample in samples:
    #     print "processing sample " + str(each_sample[1])
    #     cmd = ""
    #     # eg CEMM_05
    #     job_name = each_sample[1].rsplit("_")[0] + "_" + \
    #                each_sample[1].rsplit("_")[1]
    #     # create output_dir
    #     output_dir = args.output_dir + "/" + job_name
    #     if not os.path.exists(output_dir):
    #         os.makedirs(output_dir)
    #     # eg. /path/to/samplefile --> withough "/"
    #     sample_dir = each_sample[0]
    #     # eg. CEMM_05_accepted_hits.bam
    #     sample_name = each_sample[1]
    #
    #     for gene_region in gene_regions:
    #         gene = gene_region[0]
    #         region = gene_region[1]
    #         gene_cmd = slurm_cmd(args.stage, sample_dir,
    #                              sample_name, args.prefix,
    #                              args.exec_dir, output_dir,
    #                              job_name, args.genome,
    #                              gene, str(region))
    #         cmd += gene_cmd
    #
    #     # slurm log files are not written to subdirectory
    #     write_sh_files(job_name, str(args.ntasks),
    #                    str(args.cpus_per_task), str(args.mem),
    #                    args.time, args.queue,
    #                    args.account, args.output_dir,
    #                    args.prefix, cmd)
