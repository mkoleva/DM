#!/local/anaconda/bin/python
# IMPORTANT: leave the above line as is.

import numpy as np
import sys


def print_duplicates(videos):
    # unique = np.unique(videos)
    # print videos
    videos = sorted(videos, key = lambda x: int(x[0]))
    for i in xrange(len(videos)):
        for j in xrange(i + 1, len(videos)):
            videoId1, video1 = videos[i]
            videoId2, video2 = videos[j]

            intersection = len(np.intersect1d(video1, video2)) # A n B
            union = len(np.union1d(video1, video2))
            # print "stats", intersection, union
            jac = np.true_divide(intersection,union)
            # print "sim", np.true_divide(intersection,union)
            if jac>0.9:
                print "\t".join([videoId1, videoId2])

last_bucket = None
duplicates = []
m = {}

# for line in sys.stdin:
for line in file("mapper-out.txt"):
    line = line.strip()
    if not line:
        raise ValueError("Why is the line empty")
        continue

    s = line.strip().split("\t")
    bucket, band, videoId, video = s
    video = np.fromstring(video, sep=" ", dtype=int)

    if last_bucket is None:
        # first bucket ever
        last_bucket = bucket

    if bucket == last_bucket:
        if band in m:
            m[band].append((videoId, video))
        else:
            m[band] = [(videoId, video)]
    else:
        # Band changed (previous line was k=x, this line is k=y)
        for band, duplicates in m.iteritems():
            if len(duplicates)>1:
                # if more than one item in a bucket, try to compare them 
                print_duplicates(duplicates)

        # new dict to store buckets
        m = {}
        m[band] = [(videoId, video)]
        last_bucket = bucket

# check if any duplicates in the final dict
for band, duplicates in m.iteritems():
    if len(duplicates)>1:
        print_duplicates(duplicates)
