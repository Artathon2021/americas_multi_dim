% Compute tSNE dimensionality reduction for cdr3 regions.
% We first use multialign to align the AA sequences,
% then use tSNE with hamming distance on the aligned sequences.
% Adam Craig
% 2021-06-22

disp('loading files...')
tic
timepoints = [1 2 4];
num_timepoints = numel(timepoints);
table_cell = cell(num_timepoints,1);
for ti = 1:num_timepoints
    t = timepoints(ti);
    file_name = sprintf('IHCV2020-020.IHCV2020-020-Spikepos-Mem-B-%uTP.pooled.tsv',t);
    timepoint_table = readtable(file_name,'FileType','text','Delimiter','\t');
    timepoint_table.time_point = repmat( t, height(timepoint_table), 1 );
    table_cell{ti} = timepoint_table;
end
full_table = vertcat(table_cell{:});
toc
disp('aligning CDR3 amino acid sequences...')
tic
cdr3_aa_aligned = multialign( full_table.cdr3_aa, 'UseParallel', true );
full_table.cdr3_aa_aligned = mat2cell(cdr3_aa_aligned, ones(size(cdr3_aa_aligned,1),1), size(cdr3_aa_aligned,2) );
toc
disp('computing tSNE coordinates...')
tic
Y = tsne( double( cdr3_aa_aligned ), 'Distance', 'hamming', 'Options', struct('MaxIter',10000) );
full_table.cdr3_tsne_x = Y(:,1);
full_table.cdr3_tsne_y = Y(:,2);
toc

disp('computing additional items...')
tic
full_table.copies_per_4k = round( 4000*full_table.copies/sum(full_table.copies) );
full_table.avg_v_identity_pct = round( 100*full_table.avg_v_identity );
u_clones = unique(full_table.clone_id);
time_point_set = cell( height(full_table), 1 );
for iclone = 1:numel(u_clones)
    clone = u_clones(iclone);
    is_clone = full_table.clone_id == clone;
    tps = unique( full_table.time_point(is_clone) );
    tps_string = num2str( reshape(tps,1,[]) );
    time_point_set(is_clone) = cellstr(tps_string);
end
full_table.time_point_set = time_point_set;
figure
histogram( categorical(time_point_set) )
xlabel('time points at which it occurs')
ylabel('number of clones')
title('overlap of clones across timepoints')
toc

writetable(full_table,'IHCV2020-020.IHCV2020-020-Spikepos-Mem-B-TP1-2-4-WithtSNEXY.pooled.tsv','FileType','text','Delimiter','\t')

figure
scatter(full_table.cdr3_tsne_x,full_table.cdr3_tsne_y)
% disp('making graph...')
% colormap( jet(num_timepoints) )
% figure
