#!/usr/bin/env python

import os
import psycopg2
import re

conn = psycopg2.connect(os.getenv("LOCAL_DB_URL"))
cur = conn.cursor()

cur.execute(
    '''
        SELECT page_ptr_id, body, (SELECT url_path FROM wagtailcore_page w WHERE w.id=h.page_ptr_id) as url_path
        FROM home_post h
        WHERE body ~ '<embed([^>]*)/>' AND body NOT LIKE '%embedtype%';
    '''
)
print('Bad embeds: ' + str(cur.rowcount) )

regex = re.compile(r'(<embed.*)\/>')

data = []
for row in cur:
    r = {
        'id': row[0],
        'body': regex.sub(r'\1></embed>', row[1])
    }
    data.append(r)


if len(data) > 0:
    cur.executemany(
        '''
            UPDATE home_post
            SET body = %(body)s
            WHERE page_ptr_id = %(id)s
        ''', data
    )

    conn.commit()


cur.execute(
    '''
        SELECT page_ptr_id, body
        FROM home_post h
        WHERE body ~ '<embed([^>]*)/>' AND body NOT LIKE '%embedtype%';
    '''
)
print('Remaining bad embeds: ' + str(cur.rowcount) )

cur.close()
conn.close()
