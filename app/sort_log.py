import time
import sys
import collections

file = sys.argv[1]
output_file = sys.argv[2]
timeToLines = {}
lastTimeStamp = -1

of = open(output_file, "w")
with open(file) as f:
    for line in f:
        linesplit = line.strip().split()
        timeString = linesplit[1:4]
        timeStamp = -1
        try:
            timeArray = time.strftime(timeString, "%b %d %H:%M:%S %Y")
            timeStamp = int(time.mktime(timeArray))
            lastTimeStamp = timeStamp
        except ValueError:
            if (lastTimeStamp == -1):
                print("current line can't attach to a timestamp")
                sys.exit(-1)
            else:
                timeStamp = lastTimeStamp
        if (timeStamp in timeToLines):
            timeToLines[timeStamp].append(line);
        else:
            newRecord = []
            newRecord.append(line)
            timeToLines[timeStamp] = newRecord
    od = collections.OrderedDict(sorted(timeToLines.items()))
    for k, v in od.items():
        for line in v:
            of.write(line)
of.close()
