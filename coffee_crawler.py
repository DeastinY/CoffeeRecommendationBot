from BeautifulSoup import BeautifulSoup
import urllib2
from bs4 import BeautifulSoup                                                   

def match_class(target):                                                        
    def do_match(tag):                                                          
        classes = tag.get('class', [])                                          
        return all(c in classes for c in target)                                
    return do_match                                                             


url = urllib2.urlopen('http://www.starbucks.com/menu/catalog/product?drink=brewed-coffee#view_control=product')

content = url.read()

soup = BeautifulSoup(content, "html.parser")
                                                    
block = soup.find_all(match_class(["blocks", "thumbs"]))
this = block.find_all("span")
print this