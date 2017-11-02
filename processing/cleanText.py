import os,re

	
def findNames(text):
	names = re.findall(" ([A-Z][a-z]+)",text)
	initials = re.findall(" ([A-Z]\.)",text)
	return list(set(names+initials))

def cleanText2(text):	

	tags = ["<p>","</p>","<P>","<\P>","< P>"]
	for tag in tags:
		text = text.replace(tag," ")

	# remove days of week	
	daysOfWeek = ["Monday","Tuesday","Wednesday","Thursday","Friday"]
	for day in daysOfWeek:
		text = text.replace(day, " ")
	# remove numbers
	for num in "0123456789":
		text = text.replace(num, " ")
	# remove months of the year
	months = ["January","February","March","April","May","June","July","August","September","October","November","December"]
	for month in months:
		text = text.replace(month, "")
	
	# remove punctuation etc.
	punct = ".:,;/"
	for punc in punct:
		text = text.replace(punc," ")
		
	# remove double spaces
	text = re.sub(" +"," ",text)
	return text
		
def processFile(filename):
	print filename
	o = open("../data/king_raw/"+filename)
	d = o.read()
	o.close()

	names = findNames(d)	
	text = cleanText2(d)

	for name in names:
		text = text.replace(name," ")
	
	o = open("../data/king_clean/"+filename, 'w')
	o.write(text)
	o.close()



files = os.listdir("../data/king_raw/")

for file in files:
	if not file.startswith("."):
		processFile(file)