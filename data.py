import sqlite3 as sqlite
from config import DATABASE_NAME
import time


def dic_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class PicSQL:

    def __init__(self):
        self.conn = sqlite.connect(DATABASE_NAME)
        self.conn.row_factory =dic_factory
        self._init_database()

    def _init_database(self):
        self.conn.execute("""
            create table if not exists pic( 
                md5         text primary key   not null,
                dir         text               not null,
                name        text               not null,
                size        int                not null,
                r18         boolean            not null,
                startime    datetime           not null,
                pubtime     datetime,
                illustor    text,
                score       int
            );
        """)
        self.conn.execute("""
            create table if not exists tag(
                md5     text    not null,
                tagname text    not null
            )
        """)
        self.conn.commit()

    def insert_pics(self, pic=None, **kwargs):
        cur = self.conn.cursor()
        fields = vars(pic) if pic else kwargs
        tags = fields.pop("tags")

        sql = "insert into pic ({0}) values ({1})".format(",".join(fields.keys()), ",".join(("?" for _ in fields)))
        try:
            cur.execute(sql, tuple(fields.values()))
            self.conn.commit()
        except Exception as e:
            print(e)
        finally:
            cur.close()

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    ps = PicSQL()
    fields = {
        'md5': '1',
        'dir': '2',
        'name': '3',
        'size': 4,
        'r18': True,
        'startime': int(time.time())
    }
    ps.insert_pics(**fields)
    for item in ps.conn.execute("select * from pic").fetchall():
        print(item)