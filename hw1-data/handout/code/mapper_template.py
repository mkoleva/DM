#!/local/anaconda/bin/python
# IMPORTANT: leave the above line as is.

import numpy as np
import sys

if __name__ == "__main__":
    # VERY IMPORTANT:
    # Make sure that each machine is using the
    # same seed when generating random numbers for the hash functions.
    np.random.seed(seed=42)
    primeN = 20011

    numberOfHash = 8
    numberOfBands = 4
    bandIndex = 1

    rowsInBand = numberOfHash/numberOfBands

    aVector = np.random.randint(low=0, high =500, size=rowsInBand)
    b = np.random.randint(low=0, high=500, size=1)
    nBuckets = 20011

    hashParams = np.random.randint(low=0, high=1000, size=(numberOfHash,2))
    scores = set([])

    count = 0

    # for line in sys.stdin:
    for line in file("../data/training.txt"):
        # count+=1
        video_id = int(line[6:15])
        

        shingles = np.fromstring(line[16:], sep=" ", dtype=int)

        #convert to a binary feature vector
        featureV = np.zeros(20000)
        featureV[shingles] = 1

        # build signature matrix
        minIndex = float("inf")
        singVector = np.zeros(numberOfHash)
        singVector[:] = 30000

        # fiterate over the shingles, as those indexes will be the 1s in the vector:
        for index in shingles:
    		for indexOfHash, (a,b) in enumerate(hashParams):
    			val = (a*index + b) % primeN
    			singVector[indexOfHash] = min(val, singVector[indexOfHash])

                #if we found a minhash index 0, stop looking for a lower one
                # if not val:
                #     break;

        chunkSize= rowsInBand
        bandIndex=1

        for i in xrange(0, len(singVector), chunkSize):
            #value for each vector in a band

            band = singVector[i:i+chunkSize]
            score = (np.dot(band, aVector) + b ) % nBuckets
            
            print "\t".join([str(score), str(bandIndex), str(video_id), line[16:].strip()])
            scores.union([bandIndex, score])
            bandIndex+=1


        
