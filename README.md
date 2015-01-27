slurm-sbatch
============

### ./slurm_rnaseq_varcall.py -h

```bash
usage: slurm_rnaseq_varcall.py [-h] [--debug DEBUG] --sample_file SAMPLE_FILE
                               [--prefix PREFIX] [--output_dir OUTPUT_DIR]
                               [--cpus_per_task CPUS_PER_TASK]
                               [--ntasks NTASKS] [--mem MEM] [--time TIME]
                               [--queue {shortq,mediumq,longq}]
                               [--account ACCOUNT] --region_file REGION_FILE
                               [--genome GENOME]

slurm_rnaseq_varcall.py

optional arguments:
  -h, --help            show this help message and exit
  --debug DEBUG         Debug level
  --sample_file SAMPLE_FILE
                        sample file FORMAT: path/to/sample/file
  --prefix PREFIX       prefix of output file
  --output_dir OUTPUT_DIR
                        output_dir
  --cpus_per_task CPUS_PER_TASK
                        number of cpus per task (default: 1)
  --ntasks NTASKS       number of tasks (default: 1)
  --mem MEM             memory usage in MB (default: 8000)
  --time TIME           FORMAT: HH:MM:SS (default: 2:00:00)
  --queue {shortq,mediumq,longq}
                        cluster queue/partition (default: mediumq)
  --account ACCOUNT     username
  --region_file REGION_FILE
                        region file gene chr:start-end
  --genome GENOME       path to genome version
```


### ./slurm_defuse.py -h

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

### ./slurm_gt_screens_rk-lab.py -h

```bash
usage: slurm_gt_screens_rk-lab.py [-h] [--debug DEBUG] --sample_file
                                  SAMPLE_FILE [--prefix PREFIX]
                                  [--output_dir OUTPUT_DIR]
                                  [--cpus_per_task CPUS_PER_TASK]
                                  [--ntasks NTASKS] [--mem MEM] [--time TIME]
                                  [--queue {shortq,mediumq,longq}]
                                  [--account ACCOUNT]

slurm_gt_screens_rk-lab.py

optional arguments:
  -h, --help            show this help message and exit
  --debug DEBUG         Debug level
  --sample_file SAMPLE_FILE
                        sample file FORMAT:
  --prefix PREFIX       prefix of output file
  --output_dir OUTPUT_DIR
                        output_dir
  --cpus_per_task CPUS_PER_TASK
                        number of cpus per task (default: 4 1)
  --ntasks NTASKS       number of tasks (default: 1 1)
  --mem MEM             memory usage in MB (default: 6000)
  --time TIME           FORMAT: HH:MM:SS (default: 10:00:00)
  --queue {shortq,mediumq,longq}
                        cluster queue/partition (default: mediumq)
  --account ACCOUNT     username
```
