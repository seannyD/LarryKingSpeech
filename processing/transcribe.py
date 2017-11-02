import os
from collections import defaultdict


def dict2Table(d):
	#[('a', 187), ('f', 3963), ('h', 374), ('l', 2047), ('n', 3011), ('s', 5583), ('w', 1211), ('v', 10987)]
	return "\n".join([",".join([str(x) for x in v]) for v in d.items()])

def loadCMU():
	o = open("../data/CMUdict/cmudict-0.7b")
	d = o.read()
	o.close()	
	
	# remove stress info
	for n in "0123456789":
		d = d.replace(n,"")
	
	d = d.split("\n")[:-1]
	d = [x for x in d if not x.startswith(";;")]
	
	dx = [(x.split("  ")[0].lower(),x.split("  ")[1]) for x in d]
	
	o = open("../data/CMUdict/cmudict-0.7b.phones")
	p = o.read()
	o.close()
	rep = [("semivowel",'w'),("vowel","v"),('stop','s'),('affricate','a'),('fricative','f'),('aspirate','h'),("liquid","l"), ("nasal",'n')]
	for r in rep:
		p = p.replace(r[0],r[1])
	
	phones = dict([x.split("\t") for x in p.split("\n")[:-1]])
	#print phones
	dx = [(x[0],"".join([phones[y] for y in x[1].split(" ")])) for x in dx]
	
	return dict(dx)
	
	
cmu = loadCMU()

#print cmu.items()[:10]

def processFile(filename):
	print filename
	o = open("../data/king_clean/"+filename)
	d = o.read()
	o.close()
	
	d = d.replace("\n"," ")
	words = [x.strip().lower() for x in d.split(" ") if len(x.strip())>0]
	
	freq = defaultdict(int)
	for word in words:
		freq[word] += 1
		
	tokens_in_cmu = sum([freq[x] for x in freq.keys() if x in cmu.keys()])
	types_in_cmu = sum([x in cmu.keys() for x in freq.keys()])

	phon = [(cmu[x],freq[x]) for x in freq.keys() if x in cmu.keys()]
	
	phonCount = defaultdict(int)
	for ps,f in phon:
		for p in ps:
			phonCount[p] += f
	
	#print phonCount.items()[:10]
	
	phonCount["word_tokens"] = len(words)
	phonCount["word_types"] = len(freq.keys())
	phonCount["tokens_in_cmu"] = tokens_in_cmu
	phonCount["types_in_cmu"] = types_in_cmu
	
	phontext = dict2Table(phonCount)
	
	o = open("../data/king_phon/"+filename, 'w')
	o.write(phontext)
	o.close()




files = os.listdir("../data/king_clean/")

#processFile(files[0])

for file in files:
	if not os.path.exists("../data/king_phon/"+file):
		processFile(file)