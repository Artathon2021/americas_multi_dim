% Want to color by
% Parameters:
% CDR3 length
% average SHM level
% copy number fraction
% clone ID (subject-level)
% time point
% IGHV gene
% IGHJ gene
% Data filters:
% use productive arrangements
% overlapping vs non-overlapping clones
% copy number (at least 10 copies per library)

full_table = readtable('IHCV2020-020.IHCV2020-020-Spikepos-Mem-B-TP1-2-4-WithtSNEXY.pooled.tsv', ...
    'FileType','text','Delimiter','\t');

edges = readmatrix('serial_edges.tsv','FileType','text','Delimiter','\t');
G = digraph( edges(:,1), edges(:,2) );

% color_column = 'time_point'; title_name = 'time point';
color_column = 'time_point_set'; title_name = 'time points at which it occurs';
% color_column = 'v_gene'; title_name = 'V-gene';
% color_column = 'j_gene'; title_name = 'J-gene';
% color_column = 'copies_per_4k'; title_name = 'copies per 4,000 sequences';
% color_column = 'avg_v_identity_pct'; title_name = 'V percent identity';
% color_column = 'cdr3_num_nts'; title_name = 'CDR3 length in NTs';

[C,ia,ic] = unique(full_table.(color_column));
num_colors = numel(C);
if ~iscell(C)
    legend_items = cell( num_colors, 1 );
    for i = 1:num_colors
        legend_items{i} = sprintf( '%u', C(i) );
    end
else
    legend_items = C;
end
my_colors = jet(num_colors);
figure('Position',[0 0 2000 1000])
colormap(my_colors)
hold on
for ci = 1:num_colors
    is_this_color = ic == ci;
    scatter( full_table.cdr3_tsne_x(is_this_color), full_table.cdr3_tsne_y(is_this_color), ...
        'MarkerFaceColor', my_colors(ci,:) )
end
plot(G,'NodeCData',ic,'XData',full_table.cdr3_tsne_x,'YData',full_table.cdr3_tsne_y)
legend([legend_items;{'t1->t2->t4'}],'Location','northeastoutside' ,'FontSize',14)
title( sprintf('tSNE plot of CDR3 clones colored by %s', title_name), 'Interpreter', 'none' )
hold off

