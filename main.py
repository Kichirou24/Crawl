import json
import requests
from bs4 import BeautifulSoup

contest = int(input("Enter contest (0: Newbie, 1: Expert): "));
Url = int(input("Enter url (0: C++ FULL, 1: C++ AC): "));

page_number = 1;
problemList = [];
userList = [];
submissionList = [];

with open("key.json", "r") as f:
    key = json.load(f);

while True:
    Url = "";
    if (Url == 0):
        # C++ FULL  
        Url = "https://coder.husc.edu.vn/submissions/" + str(page_number) + "?language=CPP03&language=CPP11&language=CPP14&language=CPP17&language=CPP20";
    else:
        # C++ AC
        Url = "https://coder.husc.edu.vn/submissions/" + str(page_number) + "?status=AC&language=CPP03&language=CPP11&language=CPP14&language=CPP17&language=CPP20";
    website = requests.get(Url, cookies = {"csrftoken" : key['csrftoken'], "sessionid":key['sessionid']});
    
    if website.status_code != 200:
        break;

    soup = BeautifulSoup(website.content, "html.parser");
    
    for link in soup.find_all('a'):
        st = str(link.get('href'));
        if (st.startswith("/submission/")):
            submissionList.append(st[12:]);
        if (st.startswith("/problem/")):
            problemList.append(st[9:]);
        if (st.startswith("/user/")):
            userList.append(st[6:]);
    page_number += 1;

for index in range(len(submissionList)):
    Url = "https://coder.husc.edu.vn/src/" + submissionList[index] + "/raw";
    website = requests.get(Url, cookies = {"csrftoken" : key['csrftoken'], "sessionid":key['sessionid']});
    
    if website.status_code != 200:
        print("Error 404: " + submissionList[index]);
        continue;
    
    
    if (contest == 0):
        """
        Newbie Contest 
        """
        if (userList[index].startswith("23")):
            nameFile = problemList[index] + "_" + userList[index] + "_" + submissionList[index];
            savefile = open(nameFile + ".cpp", "w", encoding='utf-8');
            savefile.write(website.text);
            print("Save file " + nameFile + ".cpp")
            savefile.close();
    elif (contest == 1):
        """
        Expert Contest
        """
        if (userList[index].startswith("23") or (userList[index].startswith("22")) or (userList[index].startswith("21"))):
            nameFile = problemList[index] + "_" + userList[index] + "_" + submissionList[index];
            savefile = open(nameFile + ".cpp", "w", encoding='utf-8');
            savefile.write(website.text);
            print("Save file " + nameFile + ".cpp")
            savefile.close(); 
        
    
print("Done!");