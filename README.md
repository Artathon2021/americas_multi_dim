# americas_multi_dim

MATLAB:
The MATLAB code and data files needed to make the tSNE plots seen in the presentation.
Written for MATLAB 2020b.
Run scripts in this order:
cdr3tsne.m:
Reads in input data files IHCV2020-020.IHCV2020-020-Spikepos-Mem-B-1TP.pooled.tsv, IHCV2020-020.IHCV2020-020-Spikepos-Mem-B-2TP.pooled.tsv, IHCV2020-020.IHCV2020-020-Spikepos-Mem-B-4TP.pooled.tsv
Outputs IHCV2020-020.IHCV2020-020-Spikepos-Mem-B-TP1-2-4-WithtSNEXY.pooled.tsv (rows from all three input files plus columns for the time point, multi-aligned CDR3 AA sequences, tSNE x and y coordinates, and a few other columns calculated from these.)
cdr3timeedges.m:
Reads in IHCV2020-020.IHCV2020-020-Spikepos-Mem-B-TP1-2-4-WithtSNEXY.pooled.tsv
Outputs serial_edges.tsv (pairs of row indices, A B, from the table such that A and B have the same clone and either A is at time 1 and B at time 2 or A is at time 2 and B is at time 4.)
cdr3ddisthist.m or cdr3clonecompare.m in either order.
cdr3clonecompare.m: 
Reads in IHCV2020-020.IHCV2020-020-Spikepos-Mem-B-TP1-2-4-WithtSNEXY.pooled.tsv
Generates a histogram of Hamming distances between pairs of multi-aligned CDR3s.
cdr3clonecompare.m:
Reads in IHCV2020-020.IHCV2020-020-Spikepos-Mem-B-TP1-2-4-WithtSNEXY.pooled.tsv and serial_edges.tsv
generates MATLAB figures.
See the saved PNGs that are not histograms.
