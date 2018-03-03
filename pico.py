import fnmatch
import os
from pic import Pic
from data import PicSQL
import base64
import json

patterns = [
    '*.jpg',
    '*.png'
]

def coroutine(func):
    def start(*args, **kwargs):
        g = func(*args, **kwargs)
        next(g)
        return g
    return start

def find_imgs(top, patterns):
    for path, dirname, filelist in os.walk(top):
        for file in filelist:
            if any((fnmatch.fnmatch(file, pat) for pat in patterns)):
                print(path, file)
                yield os.path.join(path, file)
    

def create_pic(filenames):
    for filename in filenames:
        pic = Pic(filename)
        yield pic


def create_response(pics):
    res = []
    
    for pic in pics:
        print(pic.name)
        res.append(vars(pic))
    return json.dumps(res).join(['(', ')'])



@coroutine
def insert_into_database():
    ps = PicSQL()
    while True:
        pic = (yield)
        for field in vars(pic):
            if not getattr(pic, field):
                value = input("输入{0}\n".format(field))
                if value:
                    setattr(pic, field, value)
        ps.insert_pics(pic)


if __name__ == "__main__":
    pics_pipe = find_imgs(create_pic(insert_into_database()))
    pics_pipe.send(("/home/hakyell/Pictures", patterns))
    pics_pipe.close()

    print('pipe end')

    ps = PicSQL()
    for row in ps.conn.execute('select * from pic').fetchall():
        print(row)
