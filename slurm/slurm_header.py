# create header for slurm job

def slurm_header(job_name, ntasks, cpus_per_task, mem,
                 time, queue, account, 
                 output_dir, prefix):

    header = "#!/bin/bash\n" \
        + "#SBATCH --job-name=" + prefix + "_" + job_name + "\n" \
        + "#SBATCH --ntasks=" + ntasks + " --cpus-per-task=" \
        + cpus_per_task + " --mem=" + mem + "\n" \
        + "#SBATCH --time=" + time + "\n" \
        + "#SBATCH --partition=" + queue + "\n" \
        + "#SBATCH --account=" + account + "\n" \
        + "#SBATCH -o " + output_dir + "/" + prefix + "_" + job_name + ".o.%j.log\n" \
        + "#SBATCH -e " + output_dir + "/" + prefix + "_" + job_name + ".e.%j.log\n\n"
                 
    return header
