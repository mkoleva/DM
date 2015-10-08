d = {}

for line in file("test1.txt"):
	bucket, band, id = line.split("\t")
	if (bucket, band) in d:
		d[(bucket, band)].append(id)
	else:
		d[(bucket, band)] = [id]

for k, v in d.iteritems():
	if len(v)>1:
		print k, v