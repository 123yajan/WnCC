import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
url = 'https://itc.gymkhana.iitb.ac.in/wncc/soc/'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
project_list = []
a_tags = soup.find_all('a', href=True)
href_list = [tag.get('href') for tag in a_tags]
# print('https://itc.gymkhana.iitb.ac.in/'+href_list[17])
i=0
for href in href_list[12:-4]:
    response = requests.get('https://itc.gymkhana.iitb.ac.in/'+href)
    soup = BeautifulSoup(response.content, 'html.parser')
    l=[]
    A=[]
    for project in soup.find('h2', class_="display1 m-3 p-3 text-center project-title"):
        name=project.text.strip()
        l.append(name)
    if soup.find('p',class_="display3 project-desc"):
     for project in soup.find_all('p',class_="display3 project-desc"):
        description=project.text.strip()
        l.append(description)
        # print(project)
    elif soup.find('div', class_='project-desc'):
     div = soup.find('div', class_='project-desc')
     span = div.find('p', class_='display3')
     if span:
        description=span.text.strip()
        i=i+1
        l.append(description)
        # print(description)
    else:
       span = soup.find('p', class_='display3')
       if span:
        description=span.text.strip()
        i=i+1
        l.append(description)
        # print(description)
    #  p= div.find('p',class_=" display3")
    #  description=p.text
    #  l.append(description)
    #  print(description)
    s=[]
    k=[]
    s.append(l[0])
    st=""
    for i in range(1,len(l)):        
        st+=l[i]
    s.append(st)
    # print(s) 
    for project in soup.find_all('p',class_='lead')[1]:
        mentor=project.text
        k.append(mentor)
    for project in soup.find_all('p',class_='lead')[2]:
        mentor=project.text
        if re.search(r"\d+-\d+", mentor):
          mentor.replace(mentor,"")
        elif re.search(r"\d+", mentor):
            mentor.replace(mentor,"")
        else:
            k.append(mentor)
    A.append(s[0])
    A.append(s[1])
    A.append(k)
    project_list.append(A)
# for c in range(len(project_list)):
# #  print(project_list[i],end="\n")
#   i=i+1
# for i in range(len(project_list)):
#   for i in range
df = pd.DataFrame(project_list, columns=['Project Name','Description','Mentors'])
# print(i)
# df.drop_duplicates(inplace=True)
# df.dropna(inplace=True)
df.to_csv('soc_project_database.csv', index=False)
# Read CSV file into a DataFrame
df = pd.read_csv('soc_project_database.csv')

# Filter DataFrame to remove rows with empty values in a column
df = df.dropna(subset=['Description'])

# Write the updated DataFrame back to a CSV file
df.to_csv('my_file.csv', index=False)
