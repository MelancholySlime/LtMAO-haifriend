import os
import os.path
from os.path import (
    join as join,
    abspath as abs,
    relpath as rel,
    getsize as getsize,
    exists as exists,
    expanduser as expanduser
)


def ext(path, old, new):
    return path.removesuffix(old) + new

def walk(path, fitler_func, topdown=True):
    res = []
    for root, dirs, files in os.walk(path, topdown):
        for file in files:
            if fitler_func(file):
                res.append(join(root, file))
    return res
