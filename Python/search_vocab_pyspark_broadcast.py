#!/share/apps/python/2.7.11/bin/python
from __future__ import print_function

import sys

from pyspark import SparkContext

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: spark-submit vocab_search_pyspark_broadcast.py <local_vocabfile> <hdfs_searchfile> <hdfs_outputfile>", file=sys.stderr)
        exit(-1)

    sc = SparkContext(appName="cc_filter_vocab_broadcast")

    vocab_path = sys.argv[1]
    with open(vocab_path, 'r') as v:
        vocab = v.read().splitlines()
    broadcast_vocab = sc.broadcast(vocab)
    lines = sc.textFile(sys.argv[2])
    matches = lines.filter(lambda x: any(word in x.split() for word in broadcast_vocab.value))
    matches.saveAsTextFile(sys.argv[3])

    sc.stop()
