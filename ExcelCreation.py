__author__ = 'sharad'

import re
import collections
import csv
import sys


def main():
    """Main
    create Inputfile list
    Check if files exists otherwise report error
    Create Output file
    Start the file by adding header
    create a list of each line to be added in the output file"""
    ipfilemidname = sys.argv[1]
    ip_files = [r"prefix_sat_{}_50_allPI.txt".format(ipfilemidname),
                r"prefix_sat_{}_50_allPI.txt".format(ipfilemidname),
                r"prefix_sat_{}_60_allPI.txt".format(ipfilemidname),
                r"prefix_sat_{}_70_allPI.txt".format(ipfilemidname),
                r"prefix_sat_{}_80_allPI.txt".format(ipfilemidname),
                r"prefix_sat_{}_90_allPI.txt".format(ipfilemidname)]
    print(ip_files)
    obj = IpParser(ip_files)
    opstring = obj.op_list_str()
    obj.write_csv(r"SarveshExcel.csv")



class IpParser():
    def __init__(self, ip_files):
        """Check if all input file exists or not otherwise raise error"""
        self.ip_files = ip_files
        for filename in self.ip_files:
            try:
                with open(filename):
                    pass
            except IOError:
                print("Input file {} doesn't exist".format(filename))

    def op_list_str(self):
        file_hand = []
        for filename in self.ip_files:
            file_hand.append(open(filename, "r"))

        self.op_string = collections.OrderedDict()
        self.op_string[r"trace cycles"] = ["unresolved values in last 5 cycles"]
        self.op_string[r"percentage"] = [r"50%", r"60%", r"70%", r"80%", r"90%"]

        num_lines = sum(1 for line in file_hand[0])

        for lineno in range(num_lines):
            for file_h in file_hand:
                line = file_h.readline()
                line = line.strip()
                #filec = file_h.read()
                #print(filec)
                words = line.split(" ")
                #key = "junk"
                lenw = len(words)
                indx = file_hand.index(file_h)
                if indx == 0:
                    continue
                if lenw == 3:
                    if indx == 1:
                        key = words[0]
                        self.op_string[key] = [words[2]]
                    else:
                        if words[0] == key:
                            self.op_string[key].append(words[2])
                        else:
                            print("Error: couldn't get {} in file {}".format(key, self.ip_files[file_hand.index(file_h)]))
                else:
                    print("line {} in file {} is improper".format(lineno+1, self.ip_files[file_hand.index(file_h)]))
        return self.op_string

    def write_csv(self, opfilename):
        """Write CSV file from the dictionary of final output created previously"""
        with open(opfilename, 'w', newline='') as f:
            cwriter = csv.writer(f)
            for key in self.op_string.keys():
                rowi=[key]
                for val in self.op_string[key]:
                    rowi.append(val)
                cwriter.writerow(rowi)

            f.close()



if __name__ == "__main__": main()