slurm-sbatch
============

### user@cemm:~/src/slurm-batch$./slurm_defuse.py -h

```bash
usage: slurm_defuse.py [-h] [--debug DEBUG] --sample_file SAMPLE_FILE
                       [--prefix PREFIX] [--sample_dir SAMPLE_DIR]
                       [--exec_dir EXEC_DIR] [--output_dir OUTPUT_DIR]
                       [--defuse_ref DEFUSE_REF]
                       [--cpus_per_task CPUS_PER_TASK] [--ntasks NTASKS]
                       [--mem MEM] [--time TIME]
                       [--queue {shortq,mediumq,longq}] [--account ACCOUNT]

slurm_defuse.py

optional arguments:
  -h, --help            show this help message and exit
  --debug DEBUG         Debug level
  --sample_file SAMPLE_FILE
                        sample file FORMAT: UPD (unique patient ID
  --prefix PREFIX       prefix of output file
  --sample_dir SAMPLE_DIR
                        sample directory
  --exec_dir EXEC_DIR   exec_dir
  --output_dir OUTPUT_DIR
                        output_dir
  --defuse_ref DEFUSE_REF
                        reference databases for defuse
  --cpus_per_task CPUS_PER_TASK
                        number of cpus per task (default: 1)
  --ntasks NTASKS       number of tasks (default: 1)
  --mem MEM             memory usage in MB (default: 8000)
  --time TIME           FORMAT: HH:MM:SS (default: 2:00:00)
  --queue {shortq,mediumq,longq}
                        cluster queue/partition (default: mediumq)
  --account ACCOUNT     username
```

### user@cemm:~/src/slurm-batch$./slurm_rnaseq_varcall.py -h

```bash
usage: slurm_rnaseq_varcall.py [-h] [--debug DEBUG] --sample_file SAMPLE_FILE
                               [--prefix PREFIX] [--output_dir OUTPUT_DIR]
                               [--cpus_per_task CPUS_PER_TASK]
                               [--ntasks NTASKS] [--mem MEM] [--time TIME]
                               [--queue {shortq,mediumq,longq}]
                               [--account ACCOUNT] --region_file REGION_FILE
                               [--genome GENOME]
```
