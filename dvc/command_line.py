import sys
import glob
import os
import json
import dvc


def main():
    if sys.argv[1] == "commit":
        try:
            note = sys.argv[2]
        except IndexError:
            note = input("note:\n")
        dvc.commit(note)
    elif sys.argv[1] == "restore":
        dvc.restore(int(sys.argv[2]))
    elif sys.argv[1] == "ls":
        versions = glob.glob(os.path.join(dvc.versionsPath, "*.txt"))
        for vf in versions:
            v = json.loads(open(vf, 'r').read())
            vf = os.path.basename(vf).replace(".txt", "")
            print(vf, '\t', v["note"])
        v = input("restore? ([n] or version number): ")
        if v == "n":
            exit()
        try:
            dvc.restore(int(v))
        except Exception as e:
            print(e)
    elif sys.argv[1] == "init":
        dvc.init()
    elif sys.argv[1] == "clear":
        dvc.clear()
