full_table = readtable('IHCV2020-020.IHCV2020-020-Spikepos-Mem-B-TP1-2-4-WithtSNEXY.pooled.tsv', ...
    'FileType','text','Delimiter','\t');
cdr3_aa_aligned = double( cell2mat(full_table.cdr3_aa_aligned) );
D = pdist(cdr3_aa_aligned,'hamming');
histogram(D)
xlabel('Hamming distance')
ylabel('number of clone pairs')
title('distribution of Hamming distances of aligned CDR3 pairs')