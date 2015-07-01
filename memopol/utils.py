import sys

def progress_bar(n, total):
    progress = float(n) / total
    sys.stdout.write("\r[{0:30s}] ({1}/{2}) {3}%".format('#' * int(progress * 30), n, total, int(progress * 100)))
