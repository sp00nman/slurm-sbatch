#!/cm/shared/apps/python/2.7.6/bin/python
# -*- coding: utf-8 -*-

import sys
import os
from slurm.slurm_header import slurm_header
from slurm.slurm_parse_sample_file import slurm_tab_sample_files
from slurm.slurm_write_sh_files import write_sh_files

if __name__ == "__main__":

    def slurm_cmd(sample_dir, sample_name, screen_name, ref_genome):
        
        cmd = "BaF3_screen_workflow.sh " + "\\\n" \
            + "-i " + sample_dir + "/" + sample_name + " \\\n" \
            + "-s " + screen_name + " \\\n" \
            + "-g " + ref_genome + "\n"

        return cmd
                                                
    # command line arguments
    sample_file = sys.argv[1]
    ntasks = sys.argv[2]
    cpus_per_task = sys.argv[3]
    mem = sys.argv[4]
    time = sys.argv[5]
    queue = sys.argv[6]
    account = sys.argv[7]
    output_dir = sys.argv[8]
    prefix = sys.argv[9]
    
    # defaults
    if not cpus_per_task:
        cpus_per_task = 4
    if not mem:
        mem = 6000
    if not time:
        time = "10:0:0"
    if not queue:
        queue = mediumq
    if not account:
        account = fschischlik
    if not output_dir:
        output_dir = os.getcwd()
    
    #run
    samples = slurm_tab_sample_files(sample_file)

    for each_sample in samples:
        job_name = each_sample[0]
        sample_dir = each_sample[3].rsplit("/",1)[0]
        sample_name = each_sample[3].rsplit("/",1)[1]
        cmd = slurm_cmd(sample_dir, sample_name, 
            screen_name=each_sample[0], ref_genome=each_sample[2])
        print job_name
        print cmd
        write_sh_files(job_name, ntasks, cpus_per_task, mem, 
                       time, queue, account,
                       output_dir, prefix, cmd)
