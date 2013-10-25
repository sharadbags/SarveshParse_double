import re
import collections
import os

def main():
    inpfile = 'parse_parameters'
    obj = TxtProcessor(inpfile)
    FileNames = obj.ReadInpFile()
    obj.CreateOpFile()

class TxtProcessor():
    def __init__(self, InpFile):
        '''check if input file exists or not'''
        self.inpfile = InpFile
        try:
            with open(InpFile):
                pass
        except IOError:
            print("InputFile doesn't exists")

    def ReadInpFile(self):
        '''Read the parse parameters file and create a list of all files to read'''
        self.FileNames = []
        f = open(self.inpfile)
        for line in f:
            if line.find("#") > -1:
                continue
            word = line.split(" ")
            OpFN = "{}_{}.result".format(word[0].strip(), word[1].strip())
            if os.path.exists(OpFN):
                self.FileNames.append(OpFN)
            else:
                print("Error: File {} doesn't exists".format(OpFN))
        return self.FileNames

    def CreateOpFile(self):
        '''Read each file from list, search for required lines, save the numbers in it to
        a dictionary. Print that dictionary to output file'''
        OpFileName = "OutputParse_double.txt"
        regexes=[]
        regexes.append(re.compile("PO = (\d+)"))
        regexes.append(re.compile("NUM_VEC = (\d+)"))
        regexes.append(re.compile("COUNTER_MAX = (\d+)"))
        regexes.append(re.compile("total faults = (\d+)"))
        regexes.append(re.compile("total faults detected by original test set = (\d+)"))
        regexes.append(re.compile("total faults detected by property = (\d+)"))
        regexes.append(re.compile("Total single invariants = (\d+)"))
        regexes.append(re.compile("Total double invariants = (\d+)"))
        regexes.append(re.compile("Total properties = (\d+)"))
        regexes.append(re.compile("Single time = (\d*.\d+|\d+) sec"))
        regexes.append(re.compile("Double time = (\d*.\d+|\d+) sec"))
        regexes.append(re.compile("Total time = (\d*.\d+|\d+) sec"))
        regexes.append(re.compile("Fault simulation time = (\d*.\d+|\d+) sec"))
        regexes.append(re.compile("gate count overhead for 3 percent = (\d+)"))
        regexes.append(re.compile("num properties with 3% overhead = (\d+)"))
        regexes.append(re.compile("Faults detected with 3% overhead = (\d+)"))
        regexes.append(re.compile("gate count overhead for 5 percent = (\d+)"))
        regexes.append(re.compile("num properties with 5% overhead = (\d+)"))
        regexes.append(re.compile("Faults detected with 5% overhead = (\d+)"))
        regexes.append(re.compile("gate count overhead for 10 percent = (\d+)"))
        regexes.append(re.compile("num properties with 10% overhead = (\d+)"))
        regexes.append(re.compile("Faults detected with 10% overhead = (\d+)"))
        regexes.append(re.compile("gate count overhead for 15 percent = (\d+)"))
        regexes.append(re.compile("num properties with 15% overhead = (\d+)"))
        regexes.append(re.compile("Faults detected with 15% overhead = (\d+)"))
        regexes.append(re.compile("Optimal objective: (\d+)"))
        
        self.final = collections.OrderedDict()
        for resfile in self.FileNames:
            self.final[resfile] = []
            linebuf = self.ReadFile(resfile)
            i = 0
            for line in linebuf:
                res = regexes[i].search(line)
                if res:
                    self.final[resfile].append(res.group(1))
                    i += 1
                if i>=len(regexes):
                    break
            if i!=len(regexes):
                print("Error: couldn't get all values for file {}".format(resfile))        

        OpFileH = open(OpFileName, "w")
        OpFileH.write("PO : NUM_VEC : COUNTER_MAX : total faults : Orig det : prop det : #single : #double : #total : single time : double time : total : fault sim time : 3% gates : 3%prop : 3% fault_det : 5% gates : 5%prop : 5% fault_det : 10% gates : 10%prop : 10% fault_det : 15% gates : 15%prop : 15% fault_det : #compact :\n")
        for key in self.final:
            OpFileH.write(key)
            OpFileH.write(":  ")
            for vals in self.final[key]:
                OpFileH.write(" {}: ".format(vals))
            OpFileH.write("\n")
        OpFileH.close()
        #print(self.final)

    def ReadFile(self, FilePath):
        '''Read file line by line and return that in a buffer'''
        FileH = open(FilePath)
        FileCon = []
        for line in FileH:
            FileCon.append(line)
        FileH.close()
        return FileCon

if __name__ == "__main__": main()
