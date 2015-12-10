import requests
from bs4 import BeautifulSoup
import sys
import codecs
import time

count = 1
the_last_word_idx = 100000

file_name = r"d:\stardicfile" + str(count) + ".txt"
fo = codecs.open(file_name, "a", "utf-8")
#fo = codecs.open(r"C:\Users\Kang\Documents\stardicfile.txt", "a", "utf-8")

def merge_title_from_content( titles ):
        word_header = ""
        first_word_idx = 0
        for content_text in titles:
                main_title = content_text.get_text().replace("-", " ")
                #if (first_word_idx == 0):
                #        fo.write(main_title + "\t")
                word_header += main_title
                word_header += " | "
                first_word_idx = first_word_idx + 1

        return word_header[0:-2]

def merge_word_definition( definitions ):
        """ To extract 'div' section from content

        """
        # word_def = ""
        word_def = definitions.find_all("span")
        for w in word_def:
                #print("class = " + w['class'][0])
                if (w['class'][0] == 'NumRG'):
                        fo.write("<br><font color=\"blue\"><b>" + w.get_text() +
                              "</b></font><br>")
                elif (w['class'][0] == 'NumNO' and w.get_text().rstrip() != ""):
                        fo.write("<br><b>" + w.get_text() + "</b><br>")
                elif(w['class'][0] != 'Use_icon'):
                        if(w['class'][0][0:3] == "Use"):
                                fo.write("<font color=\"green\"><b>[예문♨] : </b></font>" + w.get_text() + "<br>")
                        elif(w['class'][0][0:10] == "Definition"):
                                fo.write("<font color=\"green\"><b>[뜻☞] : </b></font>" + w.get_text() + "<br>")
        

def parse_html_content( absolute_url ):
    """ Parsing print_area content for extract word data

    All the word content are included in print_area id.
    Todo List : Need to parse image files
    """
    r = requests.get(absolute_url)
    while (r.status_code != 200):
            time.sleep(5)
            r = requests.get(absolute_url)            
            
    soup = BeautifulSoup(r.text, "html.parser")

    word_content = soup.select("#print_area")
    
    img_content = soup.find_all("img")
    
    for line_content in word_content:
        font_faces = line_content.find("td", class_="pb10")
        titles = font_faces.find_all("font")
        
        word_title = font_faces.find("span").get_text()
        stripped_word = word_title.replace("\n", "")
        stripped_word = stripped_word.replace(" ", "")
        stripped_word = stripped_word.replace("\t", "")
        #print("|" + stripped_word + "|")        
        fo.write(stripped_word + "\t")
        
        main_title = merge_title_from_content( titles )
        fo.write("<i>" + main_title + "</i><br>")        
        
        # There may be more "div" tags
        # word_definition = line_content.find("div", class_="list")
        word_definition = line_content.find_all("div")

        for definition in word_definition:
            #print(definition)
            merge_word_definition( definition )
        fo.write("\n")
        
## Image parsing
## Need to download images from the links later
"""
    for img_txt in img_content:
        if (img_txt["src"].find("http") != -1):
            print(img_txt["src"])
"""
                    
main_url = 'http://stdweb2.korean.go.kr/search/View.jsp?idx='
hangul_section_links = []
# 555 multiple definition sample
# 1235 image included sample


while (count < the_last_word_idx):
	absolute_link_to_hangul_details = main_url + str(count)
	parse_html_content( absolute_link_to_hangul_details )
	count = count + 1
	print("====================   " + str(count))
	# print(absolute_link_to_hangul_details)

fo.close()
