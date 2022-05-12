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
        sql = """
select page, anchor, heading, body, id, page_heading from tailwind_docs 
where heading like '%{search}%'
or match (body) against ('{search}' in natural language mode) 
"""
        mydb = mysql.connector.connect(
            user='root', password='', host='127.0.0.1', database='docs')
        mycursor = mydb.cursor()
        mycursor.execute(sql.format(search=query.string))
        results = mycursor.fetchall()
        mydb.close()

        for result in results:
            url = 'https://tailwindcss.com/docs/{page}{anchor}'.format(
                page=result[0], anchor='#'+result[1] if result[1] else '')

            excerpt = ''

            print('================================================')
            print(result[2])
            print(result[3])
            print(result[4])
            print(result[5])

            if (query.string.lower() not in result[2].lower() and len(result[3]) > 0 and query.string.lower() not in result[3].lower()):
                continue

            if query.string.lower() in result[3].lower() if result[3] else '':
                start = result[3].lower().find(query.string.lower())
                bodyLength = len(result[3])

                find = result[3][
                    0 if start < 40 else start - 40: bodyLength if start + len(query.string) + 40 > bodyLength else start + len(query.string) + 40
                ]
                excerpt = (result[5]+'...' if result[5] else '') + \
                    find + \
                    ('' if start + len(query.string) + 40 > bodyLength else '...')

            items.append(Item(
                id=str(result[4]),
                icon=icon,
                text=result[2],
                subtext=excerpt if excerpt else '',
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
