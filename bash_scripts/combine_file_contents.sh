# combine contents of all files in a directory into a single file
# echo adds a line break at the end of each file
for file in *.labelLists.txt; do (cat "${file}"; echo) >> Trial2_allLabels.txt; done