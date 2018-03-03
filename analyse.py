import re


from config import SITES

analyse = {}
reg = {
    SITES['pixiv']: re.compile(r'\d+_p\d+'),
    SITES['danbooru']: re.compile(r'')
}


def register_analyse(funcname):
    def analyse_func(func):
        analyse[funcname] = func
        return func

    return analyse_func


@register_analyse(SITES['pixiv'])
def analyse_pixiv(name):
    pid, pindex = name.split('_')



@register_analyse(SITES['danbooru'])
def analyse_danbooru(name):
    pass