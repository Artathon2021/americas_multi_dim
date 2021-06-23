full_table = readtable('IHCV2020-020.IHCV2020-020-Spikepos-Mem-B-TP1-2-4-WithtSNEXY.pooled.tsv', ...
    'FileType','text','Delimiter','\t');
disp('comparing clone IDs...')
tic
[cloneR, cloneC] = meshgrid(full_table.clone_id,full_table.clone_id);
is_same_clone = cloneR == cloneC;
toc
disp('finding subsequent time points')
tic
[timepointR, timepointC] = meshgrid(full_table.time_point,full_table.time_point);
is_subsequent = (timepointR == 1 & timepointC == 2) | (timepointR == 2 & timepointC == 4);
toc
[source, target] = find( is_same_clone & is_subsequent );
writematrix([source, target],'serial_edges.tsv','FileType','text','Delimiter','\t')
G = digraph(source,target);
colormap(jet(max(full_table.time_point)))
plot(G,'NodeCData',full_table.time_point,'XData',full_table.cdr3_tsne_x,'YData',full_table.cdr3_tsne_y)
