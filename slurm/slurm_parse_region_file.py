import sys
import os


def slurm_read_region_file(region_file):
    # tab-separated
    # ADAMTS17  15:99971589-100342005
    # ADAMTS6   5:65148736-65481920

    try:
        file_object = open(region_file)
        gene_regions = [line.rstrip('\r\n').rsplit('\t')
                        for line in file_object if line.rstrip('\r\n')]
        file_object.close()

    except IOError:
        print('Sample file is missing.')

    return gene_regions