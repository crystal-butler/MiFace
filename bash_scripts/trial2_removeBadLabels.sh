for file in *.txt; do awk '{if ($1 !~ /heavyhearted/ && $1 !~ /fake-happy/ && $1 !~ /close-lipped/ && $1 !~ /awe-struck/ && $1 !~ /refulgent/ && $1 !~ /unaccepting/ && $1 !~ /dissatisfy/ && $1 !~ /ireful/ && $1 !~ /horror-stricken/ && $1 !~ /dumfounded/ && $1 !~ /unforthcoming/ && $1 !~ /unaroused/ && $1 !~ /stuporous/ && $1 !~ /tongue-tied/ && $1 !~ /fed-up/ && $1 !~ /faultfinding/) print $1;}' $file > tmp; mv tmp $file; done