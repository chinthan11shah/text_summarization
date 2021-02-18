import pandas as pd
import newspaper
import datetime
import sqlite3



conn = sqlite3.connect('Newspaper.db')
c = conn.cursor()

x = datetime.datetime.now()
list_to_ignore = ['https://epaper.telegraphindia.com/',
                '/about-us',
                '/contact-us',
                '/terms-of-use',
                '/privacy-policy',
                'https://www.facebook.com/thetelegraphindia',
                'https://twitter.com/ttindia',
                'https://www.instagram.com/telegraphonline/',
                'https://apps.apple.com/us/app/the-telegraph/id1438396234',
                'https://play.google.com/store/apps/details?id=com.thetelegraph',
                '/',
                '/opinion',
                '/india',
                '/states',
                '/calcutta',
                '/world',
                '/business',
                '/science-tech',
                '/health',
                '/sports',
                '/entertainment',
                '/culture',
                'https://www.anandabazar.com/?ref=footer_home-template',
                '/west-bengal',
                '/north-east',
                '/jharkhand',
                '/west-bengal/calcutta',
                '/sports/cricket',
                '/sports/football',
                '/sports/horse-racing/',
                '/culture/heritage',
                '/culture/travel',
                '/culture/style',
                '/culture/people',
                '/culture/books',
                '/culture/food',
                '/culture/arts',
                '#',
                'link'
                  ]


url_t = 'https://www.telegraphindia.com/'
df = pd.read_csv('C:\\Users\\HP\\PycharmProjects\\Insight_Miner\\tele_url\\tele_url\\spiders\\teleurl.csv')
#df2 = pd.read_csv('dump.csv')

count = 0
# c.execute("CREATE TABLE IF NOT EXISTS TELEGRAPH(Headline Text,"
#           "Article Text, Summary Text, Date TEXT,Image Text,URL Text,Tag_0 Text,"
#           "Tag_1 Text,Tag_2 Text,Tag_3 Text,Tag_4 Text,Tag_5 Text,Tag_6 Text,"
#           "Tag_7 Text,Tag_8 Text,Tag_9 Text)")
# conn.commit()



for index, row in df.iterrows():
    if row['link'] not in list_to_ignore:
        url = url_t+row['link']
        url_i = newspaper.Article(url="%s" % (url), language='en')
        url_i.download()
        url_i.parse()
        url_i.nlp()
        headline = url_i.title
        c.execute('SELECT HEADLINE FROM TELEGRAPH WHERE (Headline=?)', (headline,))
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
            c.execute("INSERT INTO Telegraph(Headline,Article,Summary,Date,Image,URL,Tag) VALUES(?,?,?,?,?,?,?)",
                      (str(headline), str(article), str(summary), str(date), str(image), str(url), str(tag)))
            conn.commit()
            count += 1
            print(count)

c.close()
conn.close()