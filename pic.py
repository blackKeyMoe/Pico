import time
import utils
import os
from analyse import reg, analyse

from config import MAX_IMG_SIZE, AI_R18_JUDGE


class Pic(object):

    def __init__(self, file=None, **kwargs):
        if file:
            self.dir = os.path.dirname(file)
            self.name = os.path.basename(file)
            self.size = os.path.getsize(file)
            if MAX_IMG_SIZE < self.size:
                raise Exception("Too Large Image To Process")
            with open(file, 'rb') as img:
                self.md5 = utils.get_md5_of(img)
            self.r18 = self._r18_judge()
            self.startime = int(os.path.getctime(file))
            self.pubtime = None
            self.illustor = None
            self.score = None
            self.tags = None
        else:
            for k, v in kwargs:
                setattr(self, k, v)

    def _ai_r18_judge(self):
        pass

    def _ai_tag_judge(self):
        pass

    def _r18_judge(self):
        if AI_R18_JUDGE:
            return self._ai_r18_judge()
        return True

    def set_score(self, score):
        self.score = score

    def set_tags(self, tags):
        pass

    def set_r18(self, r18):
        self.r18 = r18

    def set_illustor(self, illustor):
        self.illustor = illustor


    def _info_analyse(self):
        img_name = self.name.rsplit('.',1)[0]
        for k in reg:
            if reg[k].match(img_name):
                break
        else:
            return None, None, None
        return analyse[k](img_name)