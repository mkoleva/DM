#!/local/anaconda/bin/python
# IMPORTANT: leave the above line as is.

import numpy as np
import sys

if __name__ == "__main__":
    # VERY IMPORTANT:
    # Make sure that each machine is using the
    # same seed when generating random numbers for the hash functions.
    np.random.seed(seed=42)

    # Prime number used for initial set of hashing
    primeN = 20011

    numberOfHash = 8
    numberOfBands = 4
    bandIndex = 1

    # Generate as many As and Bs as needed for the initial hash functions
    hashParams = np.random.randint(low=0, high=1000, size=(numberOfHash,2))


    rowsInBand = numberOfHash/numberOfBands

    # Generate a random vector and random b for the band hashing
    aVector = np.random.randint(low=0, high =500, size=rowsInBand)
    b = np.random.randint(low=0, high=500, size=1)

    # another prime, which also determines the number of buckets
    nBuckets = 997

    for line in sys.stdin:
    # for line in file("../data/training.txt"):
        video_id = int(line[6:15])
        
        shingles = np.fromstring(line[16:], sep=" ", dtype=int)

        #convert to a binary feature vector
        featureV = np.zeros(20000)
        featureV[shingles] = 1

        # build signature matrix and set to a big number
        minIndex = float("inf")
        singVector = np.zeros(numberOfHash)
        singVector[:] = 30000

        # fiterate over the shingles, as those indexes will be the 1s in the vector:
        for index in shingles:
    		for indexOfHash, (a,b) in enumerate(hashParams):
    			val = (a*index + b) % primeN
    			singVector[indexOfHash] = min(val, singVector[indexOfHash])

        chunkSize= rowsInBand
        bandIndex=1

        # band part
        for i in xrange(0, len(singVector), chunkSize):
            #value for each vector in a band

            band = singVector[i:i+chunkSize]
            score = (np.dot(band, aVector) + b ) % nBuckets
            
            print "\t".join([str(score), str(bandIndex), str(video_id), line[16:].strip()])
            bandIndex+=1


        
