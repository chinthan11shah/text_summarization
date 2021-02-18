import pandas as pd
#from sqlalchemy import create_engine
#import sqlite3
cnx = create_engine('sqlite:///News.db').connect()
conn = sqlite3.connect('Newspaper.db')
c = conn.cursor()
#telegraph = pd.read_sql_table('TELEGRAPH',cnx)
#ht = pd.read_sql_table('Hindustan_times',cnx)
#ie = pd.read_sql_table('Indian_Express',cnx)
fpj = pd.read_sql_table('Free_Press',cnx)

frames = [fpj]
df = pd.concat(frames)
for index, row in df.iterrows():
    url = row['URL']
    tag = ''
    try:
        wor = url[33:]
        for i in wor:
            if ord(i) != 47:
                tag = tag + i
            else:
                break
    except:
        pass
    headline = row['Headline']
    article = row['Article']
    summary = row['Summary']
    date = row['Date']
    image = row['Image']
    ur = row['URL']
    c.execute("INSERT INTO FPJ(Headline,Article,Summary,Date,Image,URL,Tag) VALUES(?,?,?,?,?,?,?)",
              (str(headline), str(article), str(summary), str(date), str(image), str(ur), str(tag)))
    conn.commit()
c.close()
conn.close()