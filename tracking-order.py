#!/usr/bin/env python
# coding: utf-8

# In[1]:


# !pip3 install beautifulsoup4
# !pip3 install pandas
# !pip3 install requests
# !pip3 install more-itertools


# In[2]:


from bs4 import BeautifulSoup
import requests
import pandas as pd 
from more_itertools import grouper
import itertools
from datetime import datetime
import os


# In[3]:


# CLASS BY Daniel Ellis, FROM:
# https://betterprogramming.pub/custom-system-notifications-from-python-mac-5ff42e71214 

from os import system
import time

class Alerts:

  def sound(self, noise = '/System/Library/Sounds/Submarine.aiff'):
    system(f'afplay {noise}')

  
  def repeat(self, times = 4, delay = 1, noise =  '/System/Library/Sounds/Submarine.aiff'):
           for i in range(times):
                sound(noise)
                time.sleep(delay)
  
  def announce(self, text = 'The program has finished'):
           system(f'say "{text}" &')
 
  def notification(self, message='Notification from Python', app = 'Terminal'):
           system(f'osascript -e \'tell application "{app}" to display alert "{message}"\'&')

  #speak and notification    
  def notify(self, message='Finished',app='Terminal'): 
      system(f'say "{message}"& osascript -e \'tell application "{app}" to display alert "{message}"\'&')

  
  @property
  def beep(self):
    self.repeat(10,1)
      
  end = property(notify)


# In[4]:


headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
numero_da_remessa = '20220012695943'
r = requests.get(f'https://corporativo.directlog.com.br/track_individual/index.asp?numtracking={numero_da_remessa}',
                headers=headers,
                timeout=5)

soup = BeautifulSoup(r.content, 'html.parser')
tables = soup.find_all("table")
table = tables[7] # for directlog tracking there's no other way to identify the table :(


# In[6]:


data = []
for column_number, column in enumerate(table.find_all('td')):
    if column_number== 0:
         # this is an empty line idk what's doin' there
        continue

    for row_number,row in enumerate(table.find('tr')): 
        content = str(column.find('b'))
        content = content.replace("<b>","").replace("</b>","").replace("<br/>","")
        data.append(content)
   

print(f'data: ',data)
list_of_lists = list(grouper(data, 5, fillvalue=None))

if not os.path.exists(os.getcwd()+'//last_number_of_lines.txt'): # se arquivo de linhas, nao existir, é porque script ainda nao rodou
    with open('last_number_of_lines.txt','w', encoding='utf-8') as text_file: 
        text_file.write(str(1))
        print("\n\nDON'T DELETE THE last_number_of_lines.txt FILE, IT'S THE CONTROL SO WE KNOW IF WE HAD ANY UPDATES ON THE ORDER TRACKING TABLE")

with open('last_number_of_lines.txt','r', encoding='utf-8') as text_file:
    n_linhas = int(text_file.read())

if len(list_of_lists) > n_linhas: # length 1 is always the header, if len is 2 it means we have at least 1 line with real data of the order tracking update
                                     # IMPROVEMENT POINT: datetime concat + comparison with current datetime instead of amount of table rows
    print('\n\nOK, we got some update on your tracking')
    info = Alerts()
    info.notify(message ='THERE WAS AN UPDATE ON YOUR PACK! check where your order is! it might be arriving! ',app = 'System Preferences')
    with open('last_number_of_lines.txt','w', encoding='utf-8') as text_file: 
        text_file.write(str(len(list_of_lists)))
    print(f'updating row control txt: current amount of rows on table: {len(list_of_lists)} \nexporting now CSV with current tracking state stolen on website\n\n')
    df = pd.DataFrame(list_of_lists)
    print(df)
    datestamp = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
    filename = f'./a-{datestamp}.csv'
    df.to_csv(filename, header=False)
    print('exported csv!')

else:
    print('\n\n sorry, no updates on your table!')

