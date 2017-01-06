awk '{if ($0 !~ /heavyhearted/) print $0;}' 6.cosine.txt > temp.txt;
mv temp.txt 6.cosine.txt 