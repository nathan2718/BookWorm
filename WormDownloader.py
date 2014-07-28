#!python3

#This script downloads each chapter of the Worm ebook, and uses its next chapter link to download the next one.
#Import Statements
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import shutil
import os

#Returns true if the tag is a next link
def is_a_next_link(tag):
	return (tag.has_attr('href') and tag.text.strip() == "Next Chapter")

#Recursive Function, downloads each page then calls itself on the next one
def downloadPage(url):
	global chap_count
	print("Starting " + str(chap_count))
	#Save the url to a file
	file_name = str(chap_count) + ".html"
	with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
		shutil.copyfileobj(response, out_file)
	#Open the file with Beautiful Soup
	soup = BeautifulSoup(open(file_name, encoding="utf8"))
	#Store the url to the next chapter
	if soup.find(is_a_next_link) is not None:
		nextLnk = urllib.parse.quote_plus(soup.find(is_a_next_link)["href"], safe='/:')
	else:
		nextLnk = ''
	#Get rid of the pesky Next Chapter Links
	if soup.find_all("a", text="Next Chapter") != None:
		for i in soup.find_all("a", text="Next Chapter"):
			i.decompose()
	#Get rid of the pesky Last Chapter Links
	if soup.find_all("a", text="Last Chapter") != None:
		for i in soup.find_all("a", text="Last Chapter"):
			i.decompose()
	#Get rid of the end link
	if soup.find_all("a", text="End") != None:
		for i in soup.find_all("a", text="End")
			i.decompose()
	#Get rid of the pesky share stuff
	if soup.find_all("div", id="jp-post-flair") != None:
		for i in soup.find_all("div", id="jp-post-flair"):
			i.decompose()
	#Append each chapter to the output file
	with open("Worm.html", 'a', encoding="utf8") as output:
		#Write chapter title
		output.write(soup.find("h1", "entry-title").prettify(formatter="html"))
		#Write chapter content
		output.write(soup.find("div", "entry-content").prettify(formatter="html"))
	#Delete chapter file
	os.remove(file_name)
	#Increment Chapter count
	chap_count += 1
	#Calls the function on the next chapter url
	if nextLnk != '':
		downloadPage(nextLnk)

chap_count = 0
#Write the html opening
with open("Worm.html", 'a', encoding="utf8") as output:
	output.write("<html><head><title>Worm</title></head><body>")
#Call the function on the first chapter
downloadPage("http://parahumans.wordpress.com/category/stories-arcs-1-10/arc-1-gestation/1-01/")
#Write the html closing
with open("Worm.html", 'a', encoding="utf8") as output:
	output.write("</body></html>")