def slurm_dir_sample_files(sample_file):
    # /path/to/sample/file
    # /path/to/nextsample/file

    try:
        file_handle = open(sample_file)
        samples = [line.rstrip('\r\n').rsplit('/',1) \
                    for line in file_handle if line.rstrip('\r\n')]
        file_handle.close()

    except IOError:
        print('Sample file is missing.')
        
    return samples


def slurm_tab_sample_files(sample_file):
    # tab separated
    # AF_H2O2_run1 afauster hg19 /path/to/sample/file

    try:
        file_handle = open(sample_file)
        samples = [line.rstrip('\r\n').split('\t') \
                    for line in file_handle if line.rstrip('\r\n')]
        file_handle.close()

    except IOError:
        print('Sample file is missing.')
        
    return samples


def slurm_id_sample_files(sample_file):
    # UPD1 (unique patient id eg. H_0001B)
    # UPD2 ...

    try:
        file_handle = open(sample_file)
        samples = [line.rstrip('\r\n') \
                   for line in file_handle if line.rstrip('\r\n')]
        file_handle.close()

    except IOError:
        print('Sample file is missing.')

    return samples


def slurm_paired_sample_files(sample_file):
    # paired samples (R1 & R2)
    # UPD1_R1.fastq
    # UPD1_R2.fastq ...
    # legacy code
        #for (f,r) in sample_pairs:
            #split_name = re.split('\.', f) #before "_"
            #sample_name = split_name[0]

    try:
        file_handle = open(sample_file)
        lines = file_handle.readlines()
        sample_pairs = [(lines[i-1], lines[i])
                        for i in xrange(1, len(lines), 2)]

        file_handle.close()

    except IOError:
        print('Sample file is missing.')

    return sample_pairs