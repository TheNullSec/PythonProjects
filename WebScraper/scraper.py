import bs4
import requests
import re

"""
Script scrapes all the words off of www.dictionary.com, including word names, word classes, 
word class definitions and verb tense alternatives. In the code below it prints all of the 
scraped content into an easy to read command line depiction but can easily be modified to 
create a data model.
"""


url = 'https://www.dictionary.com/list/a'

req = requests.get(url).text
parsed_file = bs4.BeautifulSoup(req, "html.parser")

container = parsed_file.find_all("a", {"class":"css-1yo52wr ex77a8l2"})

url_fragments = []

[url_fragments.append(x.attrs['href']) for x in container]

for url_fragment in url_fragments:
    url_2 = f'https://www.dictionary.com{url_fragment}'
    highest_page_num = int(bs4.BeautifulSoup(requests.get(url_2).text, 
        "html.parser").find("a", string='>>').attrs["data-page"]) + 1
        
    for number in range(1, highest_page_num):
        url_3 = f'{url_2}/{number}'

        req = requests.get(url_3).text
        parsed_file = bs4.BeautifulSoup(req, "html.parser")

        container = parsed_file.find_all("a", {"class":"css-1c7x6hk-Anchor e3scdxh0"})

        word_list = []
        [word_list.append(x.attrs['href']) for x in container if "thesaurus" not in x.attrs['href']]

        for word in word_list:
            word_url = word

            req = requests.get(word_url).text
            parsed_file = bs4.BeautifulSoup(req, "html.parser")
        
            word_heading = parsed_file.h1.text

            print(f"Word: {word_heading}\n\n")
            
            word_class_containers = parsed_file.find_all("section", {"class" : "css-pnw38j e1hk9ate0"})

            word_definitions_raw = []

            word_definitions = []

            class_def_combo = []

            if len(word_class_containers) == 0:
                word_class = "N/A"
                word_definitions = "N/A"
            
            else:
                for container in word_class_containers:
                    word_class = container.find("span", {"class":"luna-pos"})
                    if word_class == None:
                        word_class = container.find("span", {"class":"luna-label italic"})
                        if word_class == None:
                            word_class = container.find("span", {"class":"pos"})
                    

                    word_class = 'N/A' if word_class == None else word_class.text
                    word_class = 'noun' if word_class == 'n.' else word_class

                    print(f"Word Class: {word_class}\n\n")

                    if "verb" in word_class and "adverb" not in word_class:
                        verb_alternative_tenses_raw = container.find_all("span", 
                            {"class":"luna-inflected-form bold"})
                        
                        verb_alternative_tenses = []

                        [verb_alternative_tenses.append(verb.text) for verb in verb_alternative_tenses_raw]

                        print("Alternative Verb Tenses: \n")
                        [print(f"{alternative}\n") for alternative in verb_alternative_tenses]
                        print("\n\n")
                    

                    print("Word Definitions: \n")


                    word_definitions_raw = container.find_all("div", {"value":re.compile("^[0-9]*$")})
                    if(len(word_definitions_raw) == 0):
                        word_definitions = 'N/A'
                        print(f"{word_definitions}\n") 
                    else:
                        word_definitions = []
                        [word_definitions.append(definition.text.capitalize()) for definition in word_definitions_raw]
                        [print(f"{definition}\n".capitalize()) for definition in word_definitions]
                    
                    

                    if "verb" in word_class and 'adverb' not in word_class:
                        word_definitions = [word_definitions, verb_alternative_tenses]
                    class_def_combo.append({word_class:word_definitions})
                
                print("\n\n---------------------------------------------\n\n")
            
            full_word_compound = {word_heading:class_def_combo}
            #print(full_word_compound)