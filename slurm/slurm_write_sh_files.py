import os
from slurm_header import slurm_header

def write_sh_files(job_name, ntasks, cpus_per_task, mem, 
                   time, queue, account, 
                   output_dir, prefix, cmd):
        
    header = slurm_header(job_name, ntasks, cpus_per_task, mem, time,
                          queue, account, output_dir, prefix)
    commands_filename = os.path.join(prefix + "_" + job_name + ".sh")
    commands_file = open(commands_filename, "w")
    commands_file.write(header + cmd)
    commands_file.close()

    
