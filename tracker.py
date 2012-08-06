"""
Tool for tracking behavioral actions and timestamping when those actions occur.
"""
import csv
from datetime import datetime


def main():
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
            now = datetime.now()
        except EOFError:
            print "Exiting"
            break

        print cmd_map[cmd], now
        writer.writerow((cmd_map[cmd], now))

    fh.close()


if __name__ == "__main__":
    main()
