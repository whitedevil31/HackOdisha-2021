import requests
from bs4 import BeautifulSoup
from selenium import webdriver
#from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException,WebDriverException
import time
import json
#D:\My Projects\Hackathons\Hack the mountains\MLH--HACK-THE-MOUNTAIN\src\api\
options = Options()
def scrapeit(url):
    print("yes")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    #driver = webdriver.Chrome(ChromeDriverManager().install())
    driver = webdriver.Chrome("D:/My Projects/Hackathons/Hack the mountains/MLH--HACK-THE-MOUNTAIN/src/api/driver/chromedriver.exe")
    delay =10
    URL =url

    def scroll_to_bottom(driver):

        old_position = 0
        new_position = None

        while new_position != old_position:
            # Get old scroll position
            old_position = driver.execute_script(
                    ("return (window.pageYOffset !== undefined) ?"
                    " window.pageYOffset : (document.documentElement ||"
                    " document.body.parentNode || document.body);"))
            # Sleep and Scroll
            time.sleep(3)
            driver.execute_script((
                    "var scrollingElement = (document.scrollingElement ||"
                    " document.body);scrollingElement.scrollTop ="
                    " scrollingElement.scrollHeight;"))
            # Get new position
            new_position = driver.execute_script(
                    ("return (window.pageYOffset !== undefined) ?"
                    " window.pageYOffset : (document.documentElement ||"
                    " document.body.parentNode || document.body);"))
    driver.get(URL)
    data =[]
    try:
        scroll_to_bottom(driver)
        #print("Page ready! ")
        soup = BeautifulSoup(driver.page_source,"html.parser")
        submissionList = soup.find_all('div',class_='SubmissionCard___StyledDiv-o16r9i-1 bOztJB')
        #print(len(submissionList))
        for submission in submissionList:
            list = submission.select('span')
            title = list[0].text
            # print("SUBMISSION TITLE  : " + title)
            description = list[1].text
            #print("SUBMISSION DESCRIPTION : " + description)
            footer = submission.find('div',class_='style__CardFooter-cbqkf4-5 keeugF')
            teamName = footer.select_one('h3').text
            # print("TEAM NAME : " + teamName)
            membersList = footer.select('a')
            # print("Members List : ")
            members=[]
            subStack=[]
            count=0
            for member in membersList:
                driver.get(member['href'])
                soup=BeautifulSoup(driver.page_source,'html.parser')
                name = soup.find('h1',class_='sc-fzozJi eUcieQ').text
                # print("Name : " + name)
                # print("Past projects List : ")
                projectList = soup.find_all('div',class_='Project__ProjectItem-sc-1ccwhbq-0 grCxUy')
                for project in projectList:
                    projectTitle = project.find('h2',class_='sc-fzoLsD eOEjif').text
                    
                    if (projectTitle!=title):
                        # print("Project Name : " + projectTitle)
                        projectDescription= project.find('span',class_='sc-AxmLO gxNQuK').text
                        techStack = project.find('span',class_='sc-AxmLO ixGBAz').text
                        techStackArray = techStack.replace(","," ")
                        #print(techStackArray)
                        # print(projectDescription)
                        # print(techStackArray)
                        pastSubmissions={"projectTitle":projectTitle,"projectDescription":projectDescription,"techStack":techStackArray,'member':name}
                        members.append(pastSubmissions)
                    elif((projectTitle==title ) and (count==0)):
                        submissionStack = project.find('span',class_='sc-AxmLO ixGBAz').text
                        
                        subStack= submissionStack.replace(',',' ')
                        #print(subStack)
                        count==1

                    

            finalObject={'teamName':teamName,'projectTitle':title,'projectDescription':description,'techStack':subStack,'members':members}
            data.append(finalObject)

        #print(data)



        jsonData = json.dumps(data)
        driver.close()
        #return jsonData
        file = open('api/data.json',"w")
        file.write(jsonData)
        file.close()

        #driver.close()


        #print(data)
        return 1
    except WebDriverException as e:
        print(e)




