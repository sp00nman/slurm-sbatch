#!/cm/shared/apps/python/2.7.6/bin/python
# -*- coding: utf-8 -*-

import sys
import os
from slurm.slurm_header import slurm_header
from slurm.slurm_parse_sample_file import slurm_tab_sample_files
from slurm.slurm_write_sh_files import write_sh_files


def slurm_cmd(exec_dir, sample_dir, each_sample, output_dir):
        
    cmd = "perl ~/src/SOAPfuse-v1.26/SOAPfuse-RUN.pl " + " \\\n" \
          + "-c " + exec_dir + "/config_" + each_sample + ".txt" + " \\\n" \
          + "-fd " + sample_dir + " \\\n" \
          + "-l " + exec_dir + "/sample_" + each_sample + ".txt" + " \\\n" \
          + "-o " + output_dir + "/" + each_sample
    
    return cmd
    

if __name__ == "__main__":
                                             
    # command line arguments
    sample_file     = sys.argv[1]
    cpus_per_task   = sys.argv[2]
    mem             = sys.argv[3]
    time            = sys.argv[4]
    queue           = sys.argv[5]
    account         = sys.argv[6]
    output_dir      = sys.argv[7]
    prefix          = sys.argv[8]
    sample_dir      = sys.argv[9]
    ntasks          = sys.argv[10]
    exec_dir        = sys.argv[11]

    
    # defaults
    if not cpus_per_task:
        cpus_per_task = 1
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
    sample_list = slurm_tab_sample_files(sample_file)
    samples = list(set([sample[0] for sample in sample_list]))

    for each_sample in samples:
        print each_sample
        cmd = slurm_cmd(exec_dir, sample_dir, each_sample, output_dir)
        write_sh_files(each_sample, ntasks, cpus_per_task, mem, 
                       time, queue, account, 
                       output_dir, prefix, cmd)
