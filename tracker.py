"""
Tool for tracking behavioral actions and timestamping when those actions occur.
"""
import csv
from datetime import datetime
import sys


def main(experiment):
    fh = open("experiments.tab", "a")
    writer = csv.writer(fh, delimiter="\t")

    cmd_map = {
        "e": "end",
        "s": "start",
        "w": "wall",
        "n": "snowberry",
        "a": "apple"
    }

    help = "\n".join(["%s: %s" % (key, value)
                      for key, value in cmd_map.items()])

    while True:
        try:
            print help
            cmd = raw_input("> ")
            action = cmd_map.get(cmd)

            if action is None:
                continue

            now = datetime.now()
            print action, now
            writer.writerow((str(experiment), cmd_map[cmd], now))

            if cmd == "e":
                experiment += 1
        except EOFError:
            print "Exiting"
            break

    fh.close()


if __name__ == "__main__":
    experiment = int(sys.argv[1])
    main(experiment)
