scores_dir = '/Users/body_LAB/Documents/MiFace/Conferences_Applications/APA_TMS_2019/Shaver_Comparison/Analysis/Scores/Score_Lists/';
labels_dir = '/Users/body_LAB/Documents/MiFace/Conferences_Applications/APA_TMS_2019/Shaver_Comparison/Analysis/Scores/Label_Lists/';
output_pass_dir = '/Users/body_LAB/Documents/MiFace/Conferences_Applications/APA_TMS_2019/Shaver_Comparison/Analysis/MATLAB/Output/Pass/';
dendro_pass_dir = '/Users/body_LAB/Documents/MiFace/Conferences_Applications/APA_TMS_2019/Shaver_Comparison/Analysis/MATLAB/Dendrograms/Pass/';
output_fail_dir = '/Users/body_LAB/Documents/MiFace/Conferences_Applications/APA_TMS_2019/Shaver_Comparison/Analysis/MATLAB/Output/Fail/';
dendro_fail_dir = '/Users/body_LAB/Documents/Conferences_Applications/APA_TMS_2019/Shaver_Comparison/Analysis/MATLAB/Dendrograms/Fail/';

scoresList = dir([scores_dir '*_scores.txt']);
labelsList = dir([labels_dir '*_labels.txt']);
inums = importdata('/Users/body_LAB/Documents/MiFace//Conferences_Applications/APA_TMS_2019/Shaver_Comparison/Analysis/Scores/ID_list_sorted.txt');

N = size(scoresList);
for k = 1:N
    % Perform clustering.
    sfile = [scores_dir scoresList(k).name];
    disp(sfile);
    scores = load (sfile);
    distances = 1 - scores;
    sqM = squareform(distances);
    link_a_cheb = linkage(sqM, 'average', 'chebychev');
    coph = cophenet(link_a_cheb, distances);
    clusters = cluster(link_a_cheb, 'cutoff', 0.685, 'criterion', 'distance');
    uq = unique(clusters);
    cnt = [uq, histc(clusters(:), uq)];
    pct = max(cnt(:,2))/sum(cnt(:,2));
    leaf_order = optimalleaforder(link_a_cheb, distances);
    lfile = [labels_dir labelsList(k).name];
    disp(lfile);
    labels = importdata (lfile);
    
    % Build the dendrogram figure.
    fig = figure;
    fig.Position = [76 76 2400 1980];
    fig.PaperUnits = 'inches';
    fig.PaperSize = [24 14];
    fig.PaperPosition = [0 0 54 14];
    fig.Renderer = 'painters';    
    
    [H, T, outperm] = dendrogram(link_a_cheb, 40, 'reorder', leaf_order, 'ColorThreshold', (0.73*max(link_a_cheb(:,3))), 'Labels', labels);
    ax = gca;
    ax.FontSize = 14;
    ax.XTickLabelRotation = 90;
    ax.XLim = [0 40];
    ax.YLim = [0 1];
    ax.YTick = [0.0 0.05 0.10 0.15 0.20 0.25 0.30 0.35 0.40 0.45 0.50 0.55 0.60 0.65 0.70 0.75 0.80 0.85 0.90 0.95 1.0];
    
    hline = refline(0,.685);
    hline.Color = [.8 .8 .8];
    hline.LineWidth = 1.5;
    set(H,'LineWidth',1.5);
    figure(fig);
    % Uncomment the next line to wait for user input before proceeding.
    pause;
    
    % Save dendrogram and output files, with directory based on pass/fail status.
    if (pct >= .17)
        od = output_pass_dir;
        dd = dendro_pass_dir;
    else
        od = output_fail_dir;
        dd = dendro_fail_dir;
    end
    outperm_file = fopen(strcat(od, num2str(inums(k)), '_outperms.txt'), 'w');
    fprintf(outperm_file, '%d\n', outperm);
    fclose(outperm_file);
    T_file = fopen(strcat(od, num2str(inums(k)), '_T.txt'), 'w');
    fprintf(T_file, '%d\n', T);
    fclose(T_file);
    fileID = fopen(strcat(od, num2str(inums(k)), '_output.txt'), 'w');
    fprintf(fileID,'%12s\n', strcat(num2str(inums(k)), '_output.txt'));
    fprintf(fileID, 'coph:\t%6.4f\n', coph);
    fprintf(fileID, '%6s\n', 'cluster count:');
    for j = 1:length(cnt(:, 1))
        fprintf(fileID, '%3i %3i\n', cnt(j,:));
    end
    fprintf(fileID, 'pct best cluster:\t%6.4f\n', pct);
    if (pct >= .17) 
        pf = 'pass'; 
        else pf = 'fail';
    end
    fprintf(fileID, '%6s\n', pf);
    figname = strcat(dd, num2str(inums(k)), '_dendrogram');
    print(fig, figname, '-depsc');
    
    % Close the output file and dendrogram figure.
    fclose(fileID);
    close(fig);
end