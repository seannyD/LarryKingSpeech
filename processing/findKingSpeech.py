import re,os

def findSpeakers(text):
	# remove headers
	text2 = text.replace("<br>","\n")
	text2 = "\n".join([x for x in text2.split("\n") if x.lower().count("rush transcript")==0 and x.lower().count("800-CNN-NEWS")==0])
	# remove stuff between brackets
	text2 = re.sub('\([^\)]+\)', '', text2)
	# find speaker strings
	speakers =  list(set(re.findall("([A-Z'\.]{2,}[A-Z' -,\.]*):",text2)))
	speakers2 = []
	for s in speakers:
		s = s.replace(","," ")
		for n in s.split(" "):
			# return lower first-letter capitalised
			speakers2.append(n.title())
	speakers2 = list(set(speakers2))
	return [x for x in speakers2 if len(x)>0]

def findKingSpeech(text):
	text = text.replace("<br />","<br>")
	# some breaks should be there
	text = re.sub("([A-Z ,'\.]{3,}:)","<br>\\1", text)
	# split text
	text = [x.strip() for x in text.split("<br>")]
	# remove header
	text = [x for x in text if x.lower().count("rush transcript")==0 and x.lower().count("800-cnn-news")==0]
	# remove html lines?
	text = [x for x in text if not x.startswith("<")]
	kingSpeaking = False
	out = ""
	for line in text:
		line = line.strip()
		# potential things like "KING (on camera):
		if line.count("KING")>0 or line.count("LARRY KING,")>0:
			kingSpeaking = True
		else:
			
			if line.count(":")>0:
				name = line[:line.index(":")]
				# if has lower case letters, this isn't a name line
				if not bool(re.search("[^a-z]",name)):
					# someone else is speaking
					kingSpeaking = False
		#print line[:30], kingSpeaking		
		if kingSpeaking:
			if len(line)>0:
				out += line + "\n"
			
	return out
			
def cleanText(text, speakers):
	# remove stuff between commas.
	text = re.sub('\([^\)]+\)', '', text)
	# remove capitalised things
	text = re.sub('[A-Z]{3,}:?','',text)

	# remove html tags
	tags = ["<p>","</p>","<P>","<\P>"]
	for t in tags:
		text = text.replace(t,"")

	# remove mentions of the speaker's names	
	for speaker in speakers:
		text = text.replace(speaker," ")
	text = "\n".join([x.strip() for x in text.split("\n") if len(x.strip())>0])
	return text
	
	
def processFile(filename):
	print filename
	o = open("../data/transcripts/"+filename)
	d = o.read()
	o.close()
	#speakers = findSpeakers(d)
	text = findKingSpeech(d)
	text = cleanText(text, [])
	
	o = open("../data/king_raw/"+filename.replace(".html",".txt"), 'w')
	o.write(text)
	o.close()



files = os.listdir("../data/transcripts/")

for file in files:
	processFile(file)