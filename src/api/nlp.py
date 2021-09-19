import json
import csv
from .scrape import scrapeit
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os

from torch._C import Value


def search(url):
    value = scrapeit(url)
    if value == 1:
        print("WORKING")
        f = open('api/data.json',)
        data = json.load(f)

        model = SentenceTransformer('bert-base-nli-mean-tokens')
        criminal2 = []
        temp = []
        temp2 = []
        temp3 = []
        count = 1
        print('APPENDING TO JSON')
        for i in data:
            #print("TEAM",count)
            count = count + 1
            #print('\n')

            temp_title = i['projectTitle']
            temp_desc = i['projectDescription']
            temp_tech = i['techStack']
            d = i['members']

            for j in d:
                #print(j['projectDescription'])
                temp.append(temp_title)
                temp.append(j['projectTitle'])
                encoded = model.encode(temp)
                #print(temp)

                title_score_array = cosine_similarity([encoded[0]],encoded[1:])
                title_score = round(title_score_array[0][0]*100)
                
                temp2.append(temp_desc)
                temp2.append(j['projectDescription'])
                encoded2 = model.encode(temp2)
                #print(temp2)

                desc_score_array = cosine_similarity([encoded2[0]],encoded2[1:])
                desc_score = round(desc_score_array[0][0]*100)
                #print(desc_score)

                temp3.append(temp_tech)
                temp3.append(j['techStack'])
                encoded3 = model.encode(temp3)

                tech_score_array = cosine_similarity([encoded3[0]],encoded3[1:])
                tech_score = round(tech_score_array[0][0]*100)

                if title_score >= 90:
                    #print("IT IS WORKING")
                    dictionary1 = {
                        "Project Title":temp[0],
                        "Project Description":temp2[0],
                        "TechStack":temp3[0],
                        "Member":j['member'],
                        "Member's project title":temp[1],
                        "Member's project description":temp2[1],
                        "Member's project Techstack":temp3[1],
                        "Title Match Percentage(out of 100)":title_score,
                        "Description Match Percentage(out of 100)":desc_score,
                        "TechStack Match Percentage(out of 100)":tech_score 
                    }

                    '''json_object = json.dumps(dictionary1, indent = 10)

                    with open("final_data.json", "w") as outfile:
                        outfile.write(json_object)'''

                    #write_json10(dictionary1)
                    criminal2.append(dictionary1)
                    #dictionary1.clear()    

                elif desc_score >= 85:
                    #print("IT IS WORKING")
                    dictionary1 = {
                        "Project Title":temp[0],
                        "Project Description":temp2[0],
                        "TechStack":temp3[0],
                        "Member":j['member'],
                        "Member's project title":temp[1],
                        "Member's project description":temp2[1],
                        "Member's project Techstack":temp3[1],
                        "Title Match Percentage(out of 100)":title_score,
                        "Description Match Percentage(out of 100)":desc_score,
                        "TechStack Match Percentage(out of 100)":tech_score 
                    }

                    #write_json10(dictionary1)
                    criminal2.append(dictionary1)
                    #dictionary1.clear()    

                temp2.pop(1)
                temp2.pop(0)
                temp3.pop(1)
                temp3.pop(0)
                temp.pop(1)
                temp.pop(0)
                #print('\n')    
        print('APPENDING TO CSV FILE')
        print(criminal2)
        print(len(criminal2))

        if len(criminal2) != 0:
            keys = criminal2[0].keys()
            with open('final_list1.csv', 'w', newline='') as output_file:
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows(criminal2)     

        f.close()
        print('DONE')
        #os.remove("src/api/data.json")
        with open("api/data.json","r+") as v:
            v.truncate(0)   
        return 1

#https://hackbout2.devfolio.co/submissions


