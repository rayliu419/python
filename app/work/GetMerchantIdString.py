from optparse import OptionParser
import os

parser = OptionParser()
parser.add_option("-f", "--file", action="store", type="string", dest='file')
options, args = parser.parse_args()
file = options.file
with open(file) as infile:
    for line in infile:
        linesplit = line.split()
        if (len(linesplit) == 2):
            merchantId = linesplit[1]
            output = os.popen('/apollo/env/envImprovement/bin/encrypt.rb ' + merchantId)
            merchantIdEncrypt = output.read()
            merchantIdEncrypt = merchantIdEncrypt.strip()
            linesplit.append(merchantIdEncrypt)
            print("\t".join(linesplit))
        else:
            merchantId = linesplit[0]
            output = os.popen('/apollo/env/envImprovement/bin/encrypt.rb ' + merchantId)
            merchantIdEncrypt = output.read()
            merchantIdEncrypt = merchantIdEncrypt.strip()
            linesplit.append(merchantIdEncrypt)
            print("\t".join(linesplit))
