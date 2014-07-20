#!python3

#This script downloads each chapter of the Worm ebook, and uses its next chapter link to download the next one.
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import shutil
import os
import re

def is_a_next_link(tag):
	return (tag.has_attr('href') and tag.text.strip() == "Next Chapter")

def downloadPage(url):
	global chap_count
	print("Starting " + str(chap_count))
	file_name = str(chap_count) + ".html"
	with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
		shutil.copyfileobj(response, out_file)
	soup = BeautifulSoup(open(file_name, encoding="utf8"))
	if soup.find(is_a_next_link) is not None:
		nextLnk = urllib.parse.quote_plus(soup.find(is_a_next_link)["href"], safe='/:')
	if soup.find_all("a", text="Next Chapter") != None:
		for i in soup.find_all("a", text="Next Chapter"):
			i.decompose()
	if soup.find_all("a", text="Last Chapter") != None:
		for i in soup.find_all("a", text="Last Chapter"):
			i.decompose()
	if soup.find_all("div", id="jp-post-flair") != None:
		for i in soup.find_all("div", id="jp-post-flair"):
			i.decompose()
	with open("test.html", 'a', encoding="utf8") as output:
		output.write(soup.find("h1", "entry-title").prettify(formatter="html"))
		output.write(soup.find("div", "entry-content").prettify(formatter="html"))
	os.remove(file_name)
	chap_count += 1
	if nextLnk != None:
		downloadPage(nextLnk)

chap_count = 0

with open("test.html", 'a', encoding="utf8") as output:
	output.write("<html><head><title>Worm</title></head><body>")

downloadPage("http://parahumans.wordpress.com/category/stories-arcs-1-10/arc-1-gestation/1-01/")

with open("test.html", 'a', encoding="utf8") as output:
	output.write("</body></html>")