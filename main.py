import json
import requests
from bs4 import BeautifulSoup

# ---------------- Function ---------------- #

def getSubmission():
    contest = int(input("Enter contest: \n0. Newbie \n1. Expert \n"));
    Url = int(input("Enter url: \n0. C++ FULL \n1. C++ AC \n"));

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

    user_prefix = {0: ["23"], 1: ["23", "22", "21"]};

    for index in range(len(submissionList)):
        Url = "https://coder.husc.edu.vn/src/" + submissionList[index] + "/raw";
        website = requests.get(Url, cookies = {"csrftoken" : key['csrftoken'], "sessionid":key['sessionid']});
        
        if website.status_code != 200:
            print("Error 404: " + submissionList[index]);
            continue;
        
        
        if userList[index][:2] in user_prefix[contest]:
            with open(problemList[index] + "_" + userList[index] + "_" + submissionList[index] + ".cpp", "w") as f:
                f.write(website.text);
            print("Done: " + submissionList[index]);
            
    print("Done!");

def getRanking():
    print("hh");

# ---------------- Main ---------------- #

print("Select function:")

function = int(input("Enter function: \n0. Get submission \n1. Get ranking \n"));

if (function == 0):
    getSubmission();
else:
    getRanking();
    