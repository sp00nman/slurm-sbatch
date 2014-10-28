#!/cm/shared/apps/python/2.7.6/bin/python
# -*- coding: utf-8 -*-

import sys
import os
from slurm.slurm_header import slurm_header
from slurm.slurm_parse_sample_file import slurm_sample_files
from slurm.slurm_write_sh_files import write_sh_files

if __name__ == "__main__":

    def slurm_cmd(sample_dir, sample_name):
        
        cmd = "bam_stat.py -i " + sample_dir + "/" + sample_name + "\n"
        return cmd
    
                                                
    # command line arguments
    sample_file = sys.argv[1]
    cpus = sys.argv[2]
    mem = sys.argv[3]
    time = sys.argv[4]
    queue = sys.argv[5]
    account = sys.argv[6]
    output_dir = sys.argv[7]
    prefix = sys.argv[8]
    
    # defaults
    if not cpus:
        cpus = 1
    if not mem:
        mem = 8000
    if not time:
        time = "2:0:0"
    if not queue:
        queue = mediumq
    if not account:
        account = fschischlik
    if not output_dir:
        output_dir = os.getcwd()
    
    #run
    samples = slurm_sample_files(sample_file)

    for each_sample in samples:
        job_name = each_sample[1].rsplit("_",4)[0] #stripped down
        cmd = slurm_cmd(each_sample[0], each_sample[1])
        write_sh_files(job_name, cpus, mem, 
                       time, queue, account,
                       output_dir, prefix, cmd)
