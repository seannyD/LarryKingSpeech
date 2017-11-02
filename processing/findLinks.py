import re,urllib2,os


def downloadTranscript(link):
	try:
		page= urllib2.urlopen(link).read()
	except:
		return ""
	if page.count("cnnBodyText")>0:
		page = page.split("\n")
		return "\n".join([x for x in page if x.count("cnnBodyText")>0])
	else:
		if page.count("Paste story between here")>0:
			page = page.split("\n")
			pos = [i for i in range(len(page)) if page[i].count("Paste story between here")>0]
			return "\n".join(page[pos[0]:pos[1]])
		else:
			if page.count("Paste content between here")>0:
				page = page.split("\n")
				pos = [i for i in range(len(page)) if page[i].count("Paste content between here")>0]
				return "\n".join(page[pos[0]:pos[1]])						
			else:
				print link
				print akjsndkjas

o = open("../data/index.html")
d = o.read()
o.close()

#<div class="cnnTransDate">December 04, 2011</div>
#<div class="cnnSectBulletItems">
#&#149;&nbsp;<a href="/TRANSCRIPTS/1112/04/lkl.01.html">LARRY KING SPECIAL: Dinner with #the Kings</a><BR>
#</div>

links = re.findall('/TRANSCRIPTS/[0-9]+/[0-9][0-9]/lkl.[0-9][0-9].html',d)

for link in links:
	print link,
	linkPath = "../data/transcripts/"+link.replace("/","_")
	if not os.path.exists(linkPath):
		print "downloading ..."
		text = downloadTranscript("http://transcripts.cnn.com"+link)
		if len(text)>0:
			o = open(linkPath, 'w')
			o.write(text)
			o.close()
	else:
		print "done"
		
		
		
		
		
		
		
		
		
		
		