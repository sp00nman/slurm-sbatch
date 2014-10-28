#!/usr/bin/python
"""
Created on 27.5.2013

@author: Fiorella Schischlik

automated workflow for defuse
Created by Fiorella Schischlik on 2013-05-27
Copyright (c) 2013 Fiorella Schischlik. All rights reserved.
Just testing git
"""

import sys
import getopt
import re

def usage():
	print 'create_scripts4_defuse.py -i sample_filename -p path2_sample_dir -o output-path'



#if__name__ is only included in order to debug with ipython, keeps variables in memory
if __name__ == '__main__':    
	
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hi:p:o:",
			["sample_filename=","path2_sample_dir=","output_path="])
	except getopt.GetoptError:
		print usage()
		sys.exit(2)

	sample_filename = None #default values ?
	path2_sample_dir = None
	output_path = None

	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()
			sys.exit()
		elif opt in ("-i", "--sample-filename"):
         		sample_filename = arg
      		elif opt in ("-p", "--path2-sample-dir"):
         		path2_sample_dir = arg
		elif opt in ("-o", "--output-path"):
                        output_path = arg
	
	print 'Sample annotation file name is', sample_filename
	print 'Path to sample directory is', path2_sample_dir
	print 'Path to output directory', output_path
	
	#path
	path2defuse = "/home/illumina/src/defuse-0.6.1"
	defuse_reference = "/home/illumina/Fiorella/reference_defuse"
	
	#TODO: check if file exists
	filename = open(sample_filename)
	list_input_files = filename.readlines()
	filename.close()
	
	#pair samples	
	pairs = [(list_input_files[i-1],list_input_files[i]) for i in xrange(1,len(list_input_files),2)]
	
	for (f,r) in pairs:
		split_name = re.split('\.', f) #before "_"
		sample_name = split_name[0]
		#sample_name = split_name[0] + "_" + split_name[1] + "_" +  split_name[2] 

		#write config file
		config = [
			"ensembl_version                             = 69\n",
			"ensembl_genome_version                      = GRCh37\n",
			"ucsc_genome_version                         = hg19\n",
			"source_directory                            = " + path2defuse + "\n",
			"dataset_directory                           = " + defuse_reference + "\n",
			"gene_models                                 = $(dataset_directory)/Homo_sapiens.$(ensembl_genome_version).$(ensembl_version).gtf\n",
			"genome_fasta                                = $(dataset_directory)/Homo_sapiens.$(ensembl_genome_version).$(ensembl_version).dna.chromosomes.fa\n",
			"repeats_filename                            = $(dataset_directory)/repeats.txt\n",
			"est_fasta                                   = $(dataset_directory)/est.fa\n",
			"est_alignments                              = $(dataset_directory)/intronEst.txt\n",
			"unigene_fasta                               = $(dataset_directory)/Hs.seq.uniq\n",
			"samtools_bin                                = /home/illumina/src/samtools-0.1.19/samtools\n",
			"bowtie_bin                                  = /home/illumina/src/bowtie-1.0.0/bowtie\n",
			"bowtie_build_bin                            = /home/illumina/src/bowtie-1.0.0/bowtie-build\n",
			"blat_bin                                    = /home/illumina/src/blat_v0.35/blat\n",
			"fatotwobit_bin                              = /home/illumina/src/blat_v0.35/faToTwoBit\n",
			"r_bin                                       = /usr/bin/R\n",
			"rscript_bin                                 = /usr/bin/Rscript\n",
			"gmap_bin                                    = /usr/local/bin/gmap\n",
			"gmap_setup_bin                              = /home/illumina/src/gmap-2013-03-31/util/gmap_setup\n",
			"gmap_index_directory                        = $(dataset_directory)/gmap\n",
			"dataset_prefix                              = $(dataset_directory)/defuse\n",
			"chromosome_prefix                           = $(dataset_prefix).dna.chromosomes\n",
			"exons_fasta                                 = $(dataset_prefix).exons.fa\n",
			"cds_fasta                                   = $(dataset_prefix).cds.fa\n",
			"cdna_regions                                = $(dataset_prefix).cdna.regions\n",
			"cdna_fasta                                  = $(dataset_prefix).cdna.fa\n",
			"reference_fasta                             = $(dataset_prefix).reference.fa\n",
			"rrna_fasta                                  = $(dataset_prefix).rrna.fa\n",
			"ig_gene_list                                = $(dataset_prefix).ig.gene.list\n",
			"repeats_regions                             = $(dataset_directory)/repeats.regions\n",
			"est_split_fasta1                            = $(dataset_directory)/est.1.fa\n",
			"est_split_fasta2                            = $(dataset_directory)/est.2.fa\n",
			"est_split_fasta3                            = $(dataset_directory)/est.3.fa\n",
			"est_split_fasta4                            = $(dataset_directory)/est.4.fa\n",
			"est_split_fasta5                            = $(dataset_directory)/est.5.fa\n",
			"est_split_fasta6                            = $(dataset_directory)/est.6.fa\n",
			"est_split_fasta7                            = $(dataset_directory)/est.7.fa\n",
			"est_split_fasta8                            = $(dataset_directory)/est.8.fa\n",
			"est_split_fasta9                            = $(dataset_directory)/est.9.fa\n",
			"prefilter1                                  = $(unigene_fasta)\n",
			"scripts_directory                           = $(source_directory)/scripts\n",
			"tools_directory                             = $(source_directory)/tools\n",
			"data_directory                              = $(source_directory)/data\n",
			"bowtie_threads                              = 15\n",
			"bowtie_quals                                = --phred33-quals\n",
			"max_insert_size                             = 500\n",
			"chromosomes                                 = 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,X,Y,MT\n",
			"mt_chromosome                               = MT\n",
			"gene_sources                                = IG_C_gene,IG_D_gene,IG_J_gene,IG_V_gene,processed_transcript,protein_coding\n",
			"ig_gene_sources                             = IG_C_gene,IG_D_gene,IG_J_gene,IG_V_gene,IG_pseudogene\n",
			"rrna_gene_sources                           = Mt_rRNA,rRNA,rRNA_pseudogene\n",
			"num_blat_sequences                          = 10000\n",
			"dna_concordant_length                       = 2000\n",
			"discord_read_trim                           = 50\n",
			"calculate_extra_annotations                 = no\n",
			"clustering_precision                        = 0.95\n",
			"span_count_threshold                        = 5\n",
			"percent_identity_threshold                  = 0.90\n",
			"split_min_anchor                            = 4\n",
			"splice_bias                                 = 10\n",
			"positive_controls                           = $(data_directory)/controls.txt\n",
			"probability_threshold                       = 0.50\n",
			"covariance_sampling_density                 = 0.01\n",
			"reads_per_job                               = 1000000\n",
			"mailto                                      = fiorella123@gmail.com\n",
			"remove_job_files                            = yes\n",
			"remove_job_temp_files                       = yes\n",
			]
		
		processed_file = open(sample_name + "_config.txt", 'wb')
		processed_file.writelines( config )
		processed_file.close()

		#strip paired files 
		f = f.strip()
		r = r.strip()

		#write run fileq
		run_command = [
				"#!/bin/bash\n",
				"/home/illumina/src/defuse-0.6.1/scripts/defuse.pl \\\n",
				"-c " + output_path + "/" + sample_name + "_config.txt \\\n",
				"-1 " + path2_sample_dir + "/" + sample_name + "/" + f + " \\\n",
				"-2 " + path2_sample_dir + "/" + sample_name + "/" + r + " \\\n",
				"-o " + output_path + "/" + sample_name + "/ \\\n",
				"-p 15"
				]
		write_run_file = open(sample_name + "_run.sh", 'wb')
		write_run_file.writelines(run_command)
		write_run_file.close()
