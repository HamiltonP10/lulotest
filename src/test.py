# -*- coding: utf-8 -*-
"""
Created on Sun Jul 17 16:00:10 2022

@author: Hamilton.Pacanchique
"""

##Library import

import requests  
import json
import pandas as pd
import sqlite3
from datetime import datetime
from datetime import timedelta
from pandas_profiling import ProfileReport



##filter dates definition
print("Insert the search´s parameters: ")
Start_Date = input("Start Date (format('yyyy-mm-dd')):")
End_Date =  input("End Date: (format('yyyy-mm-dd'))")


Start_Date = (datetime.strptime(Start_Date, '%Y-%m-%d')).date()
End_date = (datetime.strptime(End_Date, '%Y-%m-%d')).date()
difference = (End_date-Start_Date).days
df=pd.DataFrame()


##Extracting cycle 

for i in range(0,difference+1) :
 
    Date= (Start_Date + timedelta(days=i))                                                       
    print("Extracting information from the source for the day: "+str(Date))
    print("wait....") 
    URL = 'http://api.tvmaze.com/schedule/web?date='+str(Date) 
    data = requests.get(URL) 
    ## json´s file export
    text = json.dumps(data.json(),sort_keys=True, indent=4)
    f = open("../json/"+str(Date)+" data.json", "wt")
    f.write(text)
    
     ## dataframe append
    dt= pd.DataFrame.from_dict(data.json())
    df=df.append(dt)
    
                                                                   ##---------df.to_excel("output.xlsx")   
 ## profile report file export
print("generating Profile Report file....")
df.drop(['_embedded','_links','rating','image'], axis = 'columns', inplace=True)   
profile = ProfileReport(df)   
profile.to_file(output_file='../profiling/profiling_report.html') 
con = sqlite3.connect('../db/tvmazedb.db')
df.to_sql('schedule', con, if_exists='replace', index=False)
con.close()



print(" ¡process completed successfully!")
