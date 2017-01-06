scoresList = dir('*.scoresOnly.txt');
labelsList = dir('*.labelLists.txt');
inums = importdata('imgNums.txt');
%inums = 371;
N = size(scoresList);
for k = 52:52
    sfile = scoresList(k).name;
    disp(sfile);
    scores = load (sfile);
    distances = 1 - scores;
    sqM = squareform(distances);
    link_a_cheb = linkage(sqM, 'average', 'chebychev');
    coph = cophenet(link_a_cheb, distances);
    clusters = cluster(link_a_cheb, 'cutoff', 0.8375, 'criterion', 'distance');
    uq = unique(clusters);
    cnt = [uq, histc(clusters(:), uq)];
    pct = max(cnt(:,2))/sum(cnt(:,2));
    leaf_order = optimalleaforder(link_a_cheb, distances);
    lfile = labelsList(k).name;
    disp(lfile);
    labels = importdata (lfile);
    fig = figure;
    fig.OuterPosition = [76 76 1540 840];
    fig.PaperUnits = 'inches';
    fig.PaperPosition = [0 0 16 8];
    % pause;
    H = dendrogram(link_a_cheb, 0, 'reorder', leaf_order, 'ColorThreshold', 'default', 'Labels', labels);
    ax = gca;
    ax.FontSize = 16;
    ax.XTickLabelRotation = 45;
    ax.YLim = [0 1];
    hline = refline(0,.8375);
    hline.Color = [.8 .8 .8];
    hline.LineWidth = 1.5;
    set(H,'LineWidth',1.5);
    figname = strcat(num2str(inums(k)), '_dendrogram.png');
    print(fig, figname, '-dpng');
    fileID = fopen(strcat(num2str(inums(k)), '.output.txt'), 'w');
    fprintf(fileID,'%12s\n', strcat(num2str(inums(k)), '.output.txt'));
    fprintf(fileID, 'coph:\t%6.4f\n', coph);
    fprintf(fileID, '%6s\n', 'cluster count:');
    for j = 1:length(cnt(:, 1))
        fprintf(fileID, '%3i %3i\n', cnt(j,:));
    end
    fprintf(fileID, 'pct best cluster:\t%6.4f\n', pct);
    if (pct >= .75) 
        pf = 'pass'; 
        else pf = 'fail';
    end
    fprintf(fileID, '%6s\n', pf);
    fclose(fileID);
    close(fig);
end