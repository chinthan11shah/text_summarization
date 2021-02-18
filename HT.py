import pandas as pd
import newspaper
import datetime
import sqlite3

conn = sqlite3.connect('Newspaper.db')
c = conn.cursor()
x = datetime.datetime.now()
df = pd.read_csv('C:\\Users\\HP\\PycharmProjects\\Insight_Miner\\tele_url\\tele_url\\spiders\\ht.csv')

count = 0
# c.execute("CREATE TABLE IF NOT EXISTS Hindustan_times(Headline Text,"
#           "Article Text, Summary Text, Date TEXT,Image Text,URL Text,Tag_0 Text,"
#           "Tag_1 Text,Tag_2 Text,Tag_3 Text,Tag_4 Text,Tag_5 Text,Tag_6 Text,"
#           "Tag_7 Text,Tag_8 Text,Tag_9 Text)")
# conn.commit()

for index, row in df.iterrows():
    with open('ht_d.txt') as f:
        if str(row['link'][0:9]) != '/podcasts':
            url = str(row['link'])
            url_i = newspaper.Article(url="%s" % (url), language='en')
            url_i.download()
            url_i.parse()
            url_i.nlp()
            headline = url_i.title
            c.execute('SELECT HEADLINE FROM Hindustan_Times WHERE (Headline=?)', (headline,))
            entry = c.fetchone()
            if entry is None:
                #headline = url_i.title
                article = url_i.text
                summary = url_i.summary
                date = x.strftime("%d-%B-%Y %A")
                image = url_i.top_image
                tag = ''
                try:
                    wor = url[31:]
                    for i in wor:
                        if ord(i) != 47:
                            tag = tag + i
                        else:
                            break
                except:
                    pass
                c.execute("INSERT INTO Hindustan_Times(Headline,Article,Summary,Date,Image,URL,Tag) VALUES(?,?,?,?,?,?,?)",
                          (str(headline), str(article), str(summary), str(date), str(image), str(url), str(tag)))
                conn.commit()
                count += 1
                print(count)
        if str(row['link']) not in f.read():
            pass
    f.close()

c.close()
conn.close()