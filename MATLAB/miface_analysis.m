scores_dir = '/Users/body_LAB/Documents/MiFace/NLP/Kyi_Oster_Data/Analysis/Scores/Score_Lists/';
labels_dir = '/Users/body_LAB/Documents/MiFace/NLP/Kyi_Oster_Data/Analysis/Scores/Label_Lists/';
output_pass_dir = '/Users/body_LAB/Documents/MiFace/NLP/Kyi_Oster_Data/Analysis/Scores/MATLAB/Output/Pass/';
dendro_pass_dir = '/Users/body_LAB/Documents/MiFace/NLP/Kyi_Oster_Data/Analysis/Scores/MATLAB/Dendrograms/Pass/';
output_fail_dir = '/Users/body_LAB/Documents/MiFace/NLP/Kyi_Oster_Data/Analysis/Scores/MATLAB/Output/Fail/';
dendro_fail_dir = '/Users/body_LAB/Documents/MiFace/NLP/Kyi_Oster_Data/Analysis/Scores/MATLAB/Dendrograms/Fail/';

scoresList = dir([scores_dir '*_scores.txt']);
labelsList = dir([labels_dir '*_labels.txt']);
inums = importdata('/Users/body_LAB/Documents/MiFace/NLP/Kyi_Oster_Data/Analysis/Scores/ID_list.txt');

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
    clusters = cluster(link_a_cheb, 'cutoff', 0.8375, 'criterion', 'distance');
    uq = unique(clusters);
    cnt = [uq, histc(clusters(:), uq)];
    pct = max(cnt(:,2))/sum(cnt(:,2));
    leaf_order = optimalleaforder(link_a_cheb, distances);
    lfile = [labels_dir labelsList(k).name];
    disp(lfile);
    labels = importdata (lfile);
    
    % Build the dendrogram figure.
    fig = figure;
    fig.OuterPosition = [76 76 1540 840];
    fig.PaperUnits = 'inches';
    fig.PaperPosition = [0 0 16 8];
    % Uncomment the next line to wait for user input before proceeding.
    %pause;
    H = dendrogram(link_a_cheb, 0, 'reorder', leaf_order, 'ColorThreshold', 'default', 'Labels', labels);
    ax = gca;
    ax.FontSize = 16;
    ax.XTickLabelRotation = 45;
    ax.YLim = [0 1];
    hline = refline(0,.8375);
    hline.Color = [.8 .8 .8];
    hline.LineWidth = 1.5;
    set(H,'LineWidth',1.5);
    
    % Save dendrogram and output files, with directory based on pass/fail status.
    if (pct >= .75) 
        od = output_pass_dir;
        dd = dendro_pass_dir;
    else
        od = output_fail_dir;
        dd = dendro_fail_dir;
    end
    figname = strcat(dd, num2str(inums(k)), '_dendrogram.png');
    print(fig, figname, '-dpng');
    fileID = fopen(strcat(od, num2str(inums(k)), '_output.txt'), 'w');
    fprintf(fileID,'%12s\n', strcat(num2str(inums(k)), '_output.txt'));
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
    
    % Close the output file and dendrogram figure.
    fclose(fileID);
    close(fig);
end