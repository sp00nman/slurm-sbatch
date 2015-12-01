
#!/cm/shared/apps/python/2.7.6/bin/python
# -*- coding: utf-8 -*-

import getpass
import os
import argparse
from slurm.slurm_parse_sample_file import slurm_tab_sample_files
from slurm.slurm_write_sh_files import write_sh_files


def slurm_cmd(heap_mem, sample_path, sample_name):

    cmd = "java -%s -Djava.io.tmpdir=$TMPDIR " \
          "-jar $NGS_PICARD/SamToFastq.jar " \
          "INPUT=%s " \
          "FASTQ=%s_R1.fastq" \
          "SECOND_END_FASTQ=%s_R2.fastq " % (heap_mem,
                                             sample_path,
                                             sample_name,
                                             sample_name)
    return cmd

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Convert unmapped bam files to fastq.')
    parser.add_argument('--debug', required=False, type=int, help='Debug level')
    parser.add_argument('--sample_file', required=True, type=str,
                        help='sample file FORMAT:  SAMPLE_NAME path/to/sample/file')
    parser.add_argument('--prefix', required=False, type=str,
                        help="prefix of output file")
    parser.add_argument('--output_dir', required=False, type=str,
                        help="output_dir")
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


    samples = slurm_tab_sample_files(args.sample_file)

    for each_sample in samples:
        sample_name = each_sample[0]
        sample_path = each_sample[1]

        cmd = slurm_cmd(sample_path, sample_name)
        print sample_name
        print cmd
        write_sh_files(sample_name, str(args.ntasks), str(args.cpus_per_task),
                       str(args.mem), args.time, args.queue, args.account,
                       args.output_dir, args.prefix, cmd)
