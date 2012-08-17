"""
Tool for tracking behavioral actions and timestamping when those actions occur.
"""
import ConfigParser
import csv
from datetime import datetime
import sys

LINE_TERMINATOR="\n"
DELIMITER="\t"

def main(experiment_file, config_file):
    # Read in the last experiment number from the given file to determine where
    # to start counting.
    try:
        fh = open(experiment_file, "r")
        reader = csv.reader(fh, delimiter=DELIMITER, lineterminator=LINE_TERMINATOR)
        last_experiment = 0
        for row in reader:
            if int(row[0]) > last_experiment:
                last_experiment = int(row[0])

        experiment = last_experiment + 1
        fh.close()
    except IOError:
        # Default to experiment 1 if the experiments file isn't readable.
        experiment = 1

    print "Starting with experiment %i" % experiment

    fh = open(experiment_file, "a")
    writer = csv.writer(fh, delimiter=DELIMITER, lineterminator=LINE_TERMINATOR)

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

            # Let the user know what happened by writing to stdout, write the
            # official record to the experiments file, and flush the file handle
            # I/O to prevent any data from being lost if the program should
            # crash during an experiment.
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
    if len(sys.argv) != 3:
        usage = """Usage: %(command)s <experiments file> <commands configuration>

For example: %(command)s experiments.tab commands.conf
"""
        sys.stderr.write(usage % {"command": sys.argv[0]})
        sys.exit(1)

    experiment_file = sys.argv[1]
    config_file = sys.argv[2]
    main(experiment_file, config_file)
