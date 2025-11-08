#!/usr/bin/python 

import re
import requests
import time
import concurrent.futures
import sys 

regex = 'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
count = 0 
results = [] 

def banner(): 

    print """
  _     _             _     _               _ 
 | |__ (_)_ __   __ _| |__ | | ___  ___  __| |
 | '_ \| | '_ \ / _` | '_ \| |/ _ \/ _ \/ _` |
 | |_) | | | | | (_| | |_) | |  __/  __/ (_| |
 |_.__/|_|_| |_|\__, |_.__/|_|\___|\___|\__,_|
                |___/                         

"""

def get_domains(word, count=0): 
    
    print "[*] [DORKING] => " + word

    while count < 55:

        url = 'https://www.bing.com/search?q='+word+'&&filt=rf&first='+str(count)
        body = requests.get(url)
        content = body.content

        links = re.findall(regex, content)

        for link in links:
            if "microsoft" not in link:
                if "bing" not in link:
                    if "w3" not in link:
                        results.append(link)
                          
        count += 11  

if len(sys.argv) < 2: 
    banner()
    print "Usage: python2 bing_bleed.py <words>\n"
else: 
    banner()
    print "[*] Wait a few seconds...\n"
    time.sleep(3)
    with open(sys.argv[1]) as file:
        words = [line.rstrip() for line in file]
    with concurrent.futures.ThreadPoolExecutor(max_workers = 10) as executor:
        executor.map(get_domains, words)


sites = list(set(results))
print "\n"

for i in sites:
    print "[+] [FOUND] => "+i
    f = open("sites.txt", "a")
    f.write(i+"\n")
    f.close() 
