"""
Tool for tracking behavioral actions and timestamping when those actions occur.
"""
import ConfigParser
import csv
from datetime import datetime
import sys


def main(config_file, experiment):
    fh = open("experiments.tab", "a")
    writer = csv.writer(fh, delimiter="\t")

    config_parser = ConfigParser.ConfigParser()
    config_parser.read(config_file)
    cmd_map = dict(config_parser.items("commands"))
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
            fh.flush()

            if cmd == "e":
                print "End of experiment %i" % experiment
                experiment += 1
        except EOFError:
            print "Exiting"
            break

    fh.close()


if __name__ == "__main__":
    config_file = "commands.conf"
    experiment = int(sys.argv[1])
    main(config_file, experiment)
