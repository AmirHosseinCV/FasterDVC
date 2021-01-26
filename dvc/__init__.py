import glob
import os
import shutil
import json


_dvcPath = ".dvc"
_backupPath = os.path.join(_dvcPath, "files")
versionsPath = os.path.join(_dvcPath, "versions")
try:
    custom_ignores = open("dvc.ignore", "r").read().replace("\r", "").split("\n")
except FileNotFoundError:
    custom_ignores = []
_ignores = ['.dvc', '.idea', '.git'] + [x for x in custom_ignores if x != ""]
version = len(glob.glob(os.path.join(versionsPath, "*.txt")))
__version__ = "0.3.0"


def init():
    if os.path.isdir(_dvcPath):
        a = input("dvc has been initiated, do you wan't to remove the previous? (y/[n])")
        # a = 'n'
        if a == 'y':
            shutil.rmtree(_dvcPath)
            os.mkdir(_dvcPath)
        else:
            # pass
            exit()
    else:
        os.mkdir(_dvcPath)
        os.mkdir(_backupPath)
        os.mkdir(versionsPath)


def commit(note):
    global version
    data = {"note": note, "files": []}

    for x in os.walk("."):
        p, ds, fs = x
        if check_ignore(p):
            continue
        cp = remove_local_sign(p)
        target_p = os.path.join(_backupPath, cp)
        if not os.path.exists(target_p):
            os.mkdir(target_p)

        for f in fs:
            file_path = os.path.join(p, f)
            if check_ignore(file_path):
                continue
            target_file = os.path.join(target_p, f)
            if not match_files(file_path, last_file(target_file)):
                target_file += '.' + str(version)
                shutil.copy(file_path, target_file)
            data["files"].append((file_path, target_file))
    json_data = json.dumps(data)
    open(os.path.join(versionsPath, str(version) + ".txt"), 'w').write(json_data)
    version += 1


def restore(vn):
    version_data = open(os.path.join(versionsPath, str(vn) + ".txt"), 'r').read()
    version_data = json.loads(version_data)
    for f in os.listdir("."):
        if check_ignore(f):
            continue
        if os.path.isfile(f):
            os.remove(f)
        elif os.path.isdir(f):
            shutil.rmtree(f)
    for f in version_data["files"]:
        try:
            d = os.path.dirname(f[0])
            if not os.path.exists(d):
                os.makedirs(d)
            shutil.copy(f[1], f[0])
        except Exception as e:
            pass
            # print(e)
            # print(f[1])


def check_ignore(f):
    f = os.path.normpath(f)
    f = remove_local_sign(f)
    for i in _ignores:
        i = remove_local_sign(i)
        i = os.path.normpath(i)
        if os.path.isdir(i):
            if f.startswith(i + os.path.sep) or f == i:
                return True
        elif os.path.isfile(i):
            if f == i:
                return True
    return False


def last_file(path):
    f = glob.glob(path + "*")
    f = sorted(f)
    return f[-1] if len(f) > 0 else path


def match_files(a, b):
    if not os.path.exists(a) or not os.path.exists(b):
        return False
    a_size = os.stat(a).st_size
    b_size = os.stat(b).st_size
    if a_size != b_size:
        return False
    else:
        return True


def remove_local_sign(path):
    if path == ".":
        return ""
    if path[:2] == "./" or path[:2] == ".\\":
        path = path[2:]
    return path


def clear():
    if input("are you sure? (y / [n]): ") == "y":
        shutil.rmtree(_dvcPath)
        print("Done!")
