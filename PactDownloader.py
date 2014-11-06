#!python3

#This script downloads each chapter of the Worm ebook, and uses its next chapter link to download the next one.
#Import Statements
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import shutil
import os
import os.path
import time

pageTitle = "Pact"
outFile = "Pact.html"
firstLnk = "http://pactwebserial.wordpress.com/2013/12/17/bonds-1-1/"

#Returns true if the tag is a next link
def is_a_next_link(tag):
        return (tag.has_attr('href') and tag.text.strip() == "Next Chapter")

#Recursive Function, downloads each page then calls itself on the next one
def downloadPage(url, chap_count):
        # global chap_count

        downTime = time.time()
        #Save the url to a file
        file_name = str(chap_count) + ".html"
        with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)
        totalDownTime = str(time.time() - downTime)

        procTime = time.time()
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
        #Get rid of the pesky share stuff
        if soup.find_all("div", id="jp-post-flair") != None:
                for i in soup.find_all("div", id="jp-post-flair"):
                        i.decompose()
        #Get rid of the end link
        if soup.find_all("a", text="End") != None:
                for i in soup.find_all("a", text="End"):
                        i.decompose()
        #Append each chapter to the output file
        with open(outFile, 'a', encoding="utf8") as output:
                #Write chapter title
                output.write(soup.find("h1", "entry-title").prettify(formatter="html"))
                #Write chapter content
                output.write(soup.find("div", "entry-content").prettify(formatter="html"))
        #Delete chapter file
        os.remove(file_name)
        #Increment Chapter count
        chap_count += 1
        chap_title = soup.find("h1", "entry-title").get_text().encode('ascii', 'replace').decode('utf8', "ignore")
        print("{: 3} {: >35} {:.5} sec. {:.5} sec.".format(chap_count, chap_title, str(totalDownTime), str(time.time() - procTime)))

        #Calls the function on the next chapter url
        if nextLnk is not '':
                downloadPage(nextLnk, chap_count)


if os.path.isfile(outFile):
        os.remove(outFile)

#Write the html opening
with open(outFile, 'a', encoding="utf8") as output:
        output.write("<html><head><title>" + pageTitle + "</title></head><body>")
#Call the function on the first chapter
downloadPage(firstLnk, 0)
#Write the html closing
with open(outFile, 'a', encoding="utf8") as output:
        output.write("</body></html>")
