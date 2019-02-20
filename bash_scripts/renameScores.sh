for file in *scores
do
	mv "$file" "${file%.txt.out.txt scores}.scores.txt"
done
