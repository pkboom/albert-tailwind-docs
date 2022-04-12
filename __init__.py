from albert import *
from os import path
import mysql.connector

__title__ = "Tailwind docs"
__version__ = "0.4.0"
__triggers__ = "ta "
__authors__ = "pkboom"

icon = "{}/icon.png".format(path.dirname(__file__))

def handleQuery(query):
    if not query.isTriggered or not query.isValid:
        return
        
    items = []

    if query.string.strip():
        sql="""
select page, heading, body, id from tailwind_docs 
where heading like '%{search}%'
or body like '%{search}%'
order by 
    CASE 
        WHEN heading LIKE '%{search}%' THEN 0 
        ELSE 1 
    END ASC
limit 10
"""
        mydb = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='docs')
        mycursor = mydb.cursor()
        mycursor.execute(sql.format(search = query.string))
        results = mycursor.fetchall()
        mydb.close()

        for result in results:
            url = 'https://tailwindcss.com/docs/{page}'.format(page = result[0])

            excerpt = ''

            print(result[1])
            print(result[2])

            items.append(Item(
                id=str(result[3]),
                icon=icon,
                text = result[1],
                subtext= result[2],
                actions=[UrlAction(
                    text="This action opens tailwind docs.", 
                    url=url
                )],
            ))

    else:
        items.append(Item(
            icon=icon,
            text="Open Docs",
            subtext="Open tailwindcss.com/docs",
            actions=[UrlAction(
                text="This action opens tailwind docs.", 
                url="https://tailwindcss.com/docs"
            )],
        ))

    return items
