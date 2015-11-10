'''
    CMS LookUp Tool by @Sk3tchymoos3
    This tool uses whatcms.org -- be nice to them!

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


from bs4 import BeautifulSoup
import urllib3, sys, re, os.path

def HTMLGrabber(line):
    attempts = 0

    while attempts < 3:
        try:
            http = urllib3.PoolManager()
            url="http://whatcms.org/?s=" + line
            #print url
            response = http.request('GET', url)
            #content = response.read()
            soup = BeautifulSoup(response.data, "lxml")
            goodSoup=soup.find(id="wcresult")
            goodSoup = goodSoup.get_text()
            if goodSoup.startswith("Sorry"):
                goodSoup = "Unknown"
                return goodSoup
            else:
                goodSoup=goodSoup.split('C',1)[0]
                goodSoup=goodSoup.split(' ')[5]
                return goodSoup
        except urllib3.exceptions as e:
            attempts += 1
            print type(e)

totalCount = 0
goodSoupCount={}
inputFile=sys.argv[1]
if os.path.exists(inputFile):
    outputFile = open('CMSresults.txt','w')
    for line in open(inputFile):
    #for line in open('domains.txt'):
        totalCount += 1
        line=line.rstrip()
        #print line
        goodSoup = HTMLGrabber(line)
        #print line + " is using " + goodSoup
        lineToWrite = line + " is using " + goodSoup + "\n"
        outputFile.write(lineToWrite)
        if goodSoup in goodSoupCount.keys():
            goodSoupCount[goodSoup] += 1
        else:
            goodSoupCount[goodSoup] = 1
    outputFile.close()
    print "\nTotals Sites Researched: " + str(totalCount)
    for keys,values in goodSoupCount.items():
        print "\t" + keys + " -> " + str(values)
    print "Check out the CMSresults.txt file!"
else:
    print "File does not exist - check your path\spelling!"
    exit





