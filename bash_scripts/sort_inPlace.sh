for file in *.txt
do 
	sort "$file" -o "$file"
done