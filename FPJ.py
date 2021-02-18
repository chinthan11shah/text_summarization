import pandas as pd
import newspaper
import datetime
import sqlite3



conn = sqlite3.connect('Newspaper.db')
c = conn.cursor()
u = 'https://www.freepressjournal.in/'
x = datetime.datetime.now()
df = pd.read_csv('C:\\Users\\HP\\PycharmProjects\\Insight_Miner\\tele_url\\tele_url\\spiders\\fpj.csv')

count = 0
#c.execute("CREATE TABLE IF NOT EXISTS Free_Press(Headline Text,"
#          "Article Text, Summary Text, Date TEXT,Image Text,URL Text,Tag_0 Text,"
#          "Tag_1 Text,Tag_2 Text,Tag_3 Text,Tag_4 Text,Tag_5 Text,Tag_6 Text,"
#          "Tag_7 Text,Tag_8 Text,Tag_9 Text)")
#conn.commit()

for index, row in df.iterrows():
    with open('fpj_d.txt') as f:
        if row['link'] not in f.read():
            url = u + row['link']
            url_i = newspaper.Article(url="%s" % (url), language='en')
            url_i.download()
            url_i.parse()
            url_i.nlp()
            headline = url_i.title
            c.execute('SELECT HEADLINE FROM FPJ WHERE (Headline=?)', (headline,))
            entry = c.fetchone()
            if entry is None:
                #headline = url_i.title
                article = url_i.text
                summary = url_i.summary
                date = x.strftime("%d-%B-%Y %A")
                image = url_i.top_image
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
                c.execute("INSERT INTO FPJ(Headline,Article,Summary,Date,Image,URL,Tag) VALUES(?,?,?,?,?,?,?)",
                          (str(headline), str(article), str(summary), str(date), str(image), str(url), str(tag)))
                conn.commit()
                count+=1
                print(count)
    f.close()

c.close()
conn.close()