#!/usr/bin/env python

import os
import psycopg2

conn = psycopg2.connect(os.getenv("LOCAL_DB_URL"))
cur = conn.cursor()

cur.execute("SELECT page_ptr_id, body FROM home_post WHERE body LIKE '%linktype=\\\\\"link\\\\\"%';")
print('Bad link types: ' + str(cur.rowcount))

data = []
for row in cur:
    r = {
        'body': row[1].replace('linktype=\\"link\\"', ''),
        'id': row[0]
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

cur.execute("SELECT page_ptr_id, body FROM home_post WHERE body LIKE '%linktype=\\\\\"link\\\\\"%';")
print('Remaining bad link types: ' + str(cur.rowcount))

cur.close()
conn.close()
