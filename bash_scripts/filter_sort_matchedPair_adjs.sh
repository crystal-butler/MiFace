awk '{ if ($3 < 200) print ($1, $2, $3) }' adj_matchPairsScores.txt | sort -k 3 -n >> scores_under200.txt