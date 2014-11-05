#!/usr/bin/env python

# author: fschischlik
# submit script for slurm cluster

import argparse
import os
import getpass
from slurm.slurm_parse_sample_file import slurm_id_sample_files
from slurm.slurm_write_sh_files import write_sh_files
from slurm.slurm_write_config import write_config_file


def slurm_cmd(exec_dir, sample_dir, each_sample, output_dir, cpus_per_task):

    load_modules = "load module boost/1.55(default)\n"\
                   + "load module samtools/0.1.19\n"\
                   + "load module blat/35.1\n"\
                   + "load module bowtie/1.0.1\n"\
                   + "load module R/3.1.0\n"\
                   + "load module gsnap/2013.7.20\n" \
                   + "\n"

    cmd = load_modules \
          + exec_dir + "/defuse.pl \\\n"\
          + "-c " + output_dir + "/" + each_sample + "_config.txt \\\n"\
          + "-1 " + sample_dir + "/" + each_sample + "_R1.fastq" + " \\\n"\
          + "-2 " + sample_dir + "/" + each_sample + "_R2.fastq" + "\\\n"\
          + "-o " + output_dir + "/" + each_sample + "/ \\\n"\
          + "-p " + cpus_per_task

    return cmd


if __name__ == '__main__':
    # required arguments
    parser = argparse.ArgumentParser(description='slurm_defuse.py')
    parser.add_argument('--debug', required=False, type=int, help='Debug level')
    parser.add_argument('--sample_file', required=True, type=str,
                        help='sample file FORMAT:  UPD (unique patient ID')
    parser.add_argument('--prefix', required=False, type=str,
                        help="prefix of output file")
    parser.add_argument('--sample_dir', required=False, type=str,
                        help="sample directory")
    parser.add_argument('--exec_dir', required=False, type=str,
                        help="exec_dir")
    parser.add_argument('--output_dir', required=False, type=str,
                        help="output_dir")
    parser.add_argument('--defuse_ref', required=False, type=str,
                        help="reference databases for defuse")
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
        home_dir = os.getenv("HOME")
        args.exec_dir = home_dir + "/src/defuse-0.6.2"
    if not args.prefix:
        args.prefix = "SAMPLE"
    if not args.defuse_ref:
        args.defuse_ref = home_dir + "/reference_defuse"

    print args

    # read in sample file
    sample_list = slurm_id_sample_files(args.sample_file)

    for each_sample in sample_list:

        print each_sample

        config = "ensembl_version    = 69\n"\
                 + "ensembl_genome_version     = GRCh37\n"\
                 + "ucsc_genome_version        = hg19\n"\
                 + "source_directory           = " + args.exec_dir + "\n"\
                 + "dataset_directory          = " + args.defuse_ref + "\n"\
                 + "gene_models                = $(dataset_directory)/" \
                   "Homo_sapiens.$(ensembl_genome_version).$(ensembl_version).gtf\n"\
                 + "genome_fasta               = $(dataset_directory)/" \
                   "Homo_sapiens.$(ensembl_genome_version).$(ensembl_version).dna.chromosomes.fa\n"\
                 + "repeats_filename           = $(dataset_directory)/repeats.txt\n"\
                 + "est_fasta                  = $(dataset_directory)/est.fa\n"\
                 + "est_alignments             = $(dataset_directory)/intronEst.txt\n"\
                 + "unigene_fasta              = $(dataset_directory)/Hs.seq.uniq\n"\
                 + "samtools_bin               = samtools\n"\
                 + "bowtie_bin                 = bowtie\n"\
                 + "bowtie_build_bin           = bowtie-build\n"\
                 + "blat_bin                   = blat\n"\
                 + "fatotwobit_bin             = faToTwoBit\n"\
                 + "r_bin                      = R\n"\
                 + "rscript_bin                = Rscript\n"\
                 + "gmap_bin                   = gmap\n"\
                 + "gmap_setup_bin             = gmap_setup\n"\
                 + "gmap_index_directory       = $(dataset_directory)/gmap\n"\
                 + "dataset_prefix             = $(dataset_directory)/defuse\n"\
                 + "chromosome_prefix          = $(dataset_prefix).dna.chromosomes\n"\
                 + "exons_fasta                = $(dataset_prefix).exons.fa\n"\
                 + "cds_fasta                  = $(dataset_prefix).cds.fa\n"\
                 + "cdna_regions               = $(dataset_prefix).cdna.regions\n"\
                 + "cdna_fasta                 = $(dataset_prefix).cdna.fa\n"\
                 + "reference_fasta            = $(dataset_prefix).reference.fa\n"\
                 + "rrna_fasta                 = $(dataset_prefix).rrna.fa\n"\
                 + "ig_gene_list               = $(dataset_prefix).ig.gene.list\n"\
                 + "repeats_regions            = $(dataset_directory)/repeats.regions\n"\
                 + "est_split_fasta1           = $(dataset_directory)/est.1.fa\n"\
                 + "est_split_fasta2           = $(dataset_directory)/est.2.fa\n"\
                 + "est_split_fasta3           = $(dataset_directory)/est.3.fa\n"\
                 + "est_split_fasta4           = $(dataset_directory)/est.4.fa\n"\
                 + "est_split_fasta5           = $(dataset_directory)/est.5.fa\n"\
                 + "est_split_fasta6           = $(dataset_directory)/est.6.fa\n"\
                 + "est_split_fasta7           = $(dataset_directory)/est.7.fa\n"\
                 + "est_split_fasta8           = $(dataset_directory)/est.8.fa\n"\
                 + "est_split_fasta9           = $(dataset_directory)/est.9.fa\n"\
                 + "prefilter1                 = $(unigene_fasta)\n"\
                 + "scripts_directory          = $(source_directory)/scripts\n"\
                 + "tools_directory            = $(source_directory)/tools\n"\
                 + "data_directory             = $(source_directory)/data\n"\
                 + "bowtie_threads             = " + str(args.cpus_per_task) + "\n"\
                 + "bowtie_quals               = --phred33-quals\n"\
                 + "max_insert_size            = 500\n"\
                 + "chromosomes                = 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,X,Y,MT\n"\
                 + "mt_chromosome              = MT\n"\
                 + "gene_sources               = IG_C_gene,IG_D_gene,IG_J_gene,IG_V_gene, " \
                   "processed_transcript,protein_coding\n"\
                 + "ig_gene_sources            = IG_C_gene,IG_D_gene,IG_J_gene, " \
                   "IG_V_gene,IG_pseudogene\n"\
                 + "rrna_gene_sources          = Mt_rRNA,rRNA,rRNA_pseudogene\n"\
                 + "num_blat_sequences         = 10000\n"\
                 + "dna_concordant_length      = 2000\n"\
                 + "discord_read_trim          = 50\n"\
                 + "calculate_extra_annotations= no\n"\
                 + "clustering_precision       = 0.95\n"\
                 + "span_count_threshold       = 5\n"\
                 + "percent_identity_threshold = 0.90\n"\
                 + "split_min_anchor           = 4\n"\
                 + "splice_bias                = 10\n"\
                 + "positive_controls          = $(data_directory)/controls.txt\n"\
                 + "probability_threshold      = 0.50\n"\
                 + "covariance_sampling_density= 0.01\n"\
                 + "reads_per_job              = 1000000\n"\
                 + "remove_job_files           = yes\n"\
                 + "remove_job_temp_files      = yes\n"

        cmd = slurm_cmd(args.exec_dir, args.sample_dir,
                        each_sample, args.output_dir,
                        str(args.cpus_per_task))

        write_config_file(each_sample, config)

        write_sh_files(each_sample, str(args.ntasks), str(args.cpus_per_task),
                       str(args.mem), args.time, args.queue, args.account,
                       args.output_dir, args.prefix, cmd)