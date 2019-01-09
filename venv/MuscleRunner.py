import DEFINES
import subprocess


def arr2FASTA(arr): #take an array and poot in fasta format
    fasta_file=open(DEFINES.FILES_PATH + DEFINES.MUSCLE_IN_FILE,'w')
    str_form=">gi|"
    i=1
    for line in arr:
        fasta_file.write(str_form)
        fasta_file.write(str(i)+"\n")
    	l=''.join(line)
    	l=(l.replace('0', DEFINES.ZERO)).replace('1', DEFINES.ONE)
        fasta_file.write(l+"\n");
        i+=1
    fasta_file.close()

def FASTA2arr(fasta_file,output_file): #take fasta file, change it to an 2dim-array and save the output on a file

    arr=[]
    lines=fasta_file.readlines()
    for line in lines:
        if line[0] != ">":
            for x in line:
                if x==DEFINES.ZERO: arr[-1].append("0")
                if x==DEFINES.ONE: arr[-1].append("1")
                if x=='-': arr[-1].append("-")
        else:
            if line[0]==">":
                arr.append([])
    for line in arr:#write to file
        for x in line:
            output_file.write(str(x)+" ")
        output_file.write("\n")
    return arr


#call muscle and return an array with the results
def muscleCall(arr):
    arr2FASTA(arr)  # put arr in "in.txt" file
    subprocess.call([r"/home/ubu/Yael/muscle3.8.31_i86linux64", "-in", DEFINES.FILES_PATH + DEFINES.MUSCLE_IN_FILE, "-out", DEFINES.FILES_PATH + DEFINES.MUSCLE_OUT_FILE])
    #subprocess.call([r"C:\\Users\moshab\Desktop\final project\muscle\muscle3.8.31_i86win32.exe", "-in", DEFINES.MUSCLE_PATH + DEFINES.MUSCLE_IN_FILE, "-out", DEFINES.MUSCLE_PATH + DEFINES.MUSCLE_OUT_FILE])
    #subprocess.call([r"C:\Users\boris7\Desktop\final project\muscle\muscle3.8.31_i86win32.exe", "-in", DEFINES.MUSCLE_PATH + DEFINES.MUSCLE_IN_FILE, "-out", DEFINES.MUSCLE_PATH + DEFINES.MUSCLE_OUT_FILE])
    #subprocess.call([r"C:\Users\boris10\Desktop\projectCSE\muscle\muscle3.8.31_i86win32.exe", "-in", DEFINES.MUSCLE_PATH + DEFINES.MUSCLE_IN_FILE, "-out", DEFINES.MUSCLE_PATH + DEFINES.MUSCLE_OUT_FILE])

    fasta_file = open(DEFINES.FILES_PATH + DEFINES.MUSCLE_OUT_FILE, 'r')  # read the output of mussle
    output_file = open(DEFINES.MUSCLE_PATH + 'mussle_norm_output.txt', 'w')
    fasta_res = FASTA2arr(fasta_file, output_file)
    output_file.close()
    fasta_file.close()
    return fasta_res

#now, calc only flips
def calc_err_bestfit(source, st):
    min_count=len(source)
    min_ind=-1
    for i in range(len(source)-len(st)+1):
        sub_source=source[i:]
        flips = 0

        for s,r in zip(sub_source,st):
            if s!=r: flips+=1

        if flips<min_count:
            min_count, min_ind = flips,i
    return min_count, min_ind























############from mucle:


#return the error preecent. #COUNT_SPACE_MISS=True -> calc "-" as an error
def statisticsFromMuscle(sourceString, binaryAfterMajorityString):
    counter = {"Flips": 0, "Space": 0}
    sourceLen =len(sourceString)
    AfterMajorityLen= len(binaryAfterMajorityString)
    if AfterMajorityLen!=sourceLen:
        print("sourceString and binaryAfterMajorityString are in diffrent sizes")
        #return
    for s,m in zip(sourceString,binaryAfterMajorityString):
        if s!=m:
            if m =='-':
                if DEFINES.COUNT_SPACE_MISS:
                    counter['Space']+=1
            else: counter['Flips']+=1
    return ((1.0*(counter['Space']+counter['Flips']))/sourceLen) # resultForGraph['Z'].append((counter['Space']+counter['Flips'])/strLen)


#return the error preecent.
#this function supose to be smarter and caculate the possible error probebility
def statisticsFromMuscle_OverSpace(sourceString, binaryAfterMajorityString):
    counter = {"Flips": 0, "Space": 0}
    sourceLen =len(sourceString)
    AfterMajorityLen= (binaryAfterMajorityString)
    if AfterMajorityLen!=sourceLen:
        print("sourceString and binaryAfterMajorityString are in diffrent sizes")
    print "before stat - overcome space reasults:"
    st=''.join(binaryAfterMajorityString)
    print sourceString
    print st; print

    j=0; k=0;c=0;
    for i in range(len(binaryAfterMajorityString)):
        if j<(len(sourceString)-1) and k< (len(binaryAfterMajorityString)-1):
            if binaryAfterMajorityString[k]!=sourceString[j]:
                if binaryAfterMajorityString[k] =="-":
                    c+=1
                    if(flip_counter(sourceString[j:],(binaryAfterMajorityString[k+1:]))<flip_counter(sourceString[j:],binaryAfterMajorityString[k:])):
                          binaryAfterMajorityString=binaryAfterMajorityString[:k]+binaryAfterMajorityString[k+1:]
                          print "without: "+str(k)
                          print str(sourceString[j+1:(j+1 + 30)])
                          st = ''.join(binaryAfterMajorityString[k:(k + 30)])
                          print st
                          j-=1
                          k-=1 # because we cat the binaryAfterMajorityString
                    else:
                        print "good: " +str(k)
                        print str(sourceString[j:(j+30)])
                        st=''.join(binaryAfterMajorityString[k:(k+30)])
                        print st
                else:
                    counter['Flips']+=1
        j+=1; k+=1;
    print "after stat - overcome space reasults:"
    st=''.join(binaryAfterMajorityString)
    print sourceString
    print st
    print "error: "+ format(((1.0*(counter['Space']+counter['Flips']))/sourceLen),".4f") +"\n"
    return ((1.0*(counter['Space']+counter['Flips']))/sourceLen) # resultForGraph['Z'].append((counter['Space']+counter['Flips'])/strLen)

#count only the flips between 2 string, until there is "-" (after some "0101...")
# this function is used in statisticsFromMuscle_OverSpace
def flip_counter(sourceString,binaryAfterMajorityString):
    flips=0; first=True
    for s,m in zip(sourceString,binaryAfterMajorityString):
        if m=="-":
            if not first: return flips
        else: first=False
        if (m=="0" and s=="1") or (s=="0" and m=="1"):
            flips+=1
    return flips

def calc_str_majority(arr):#calc the final string out of the majority of the samples
    length=[]; res=[]; i=-1
    for line in arr: length.append(len(line))
    if length==[]:
        print "error in fasta arr:\n arr:"
        print arr
    while(i<max(length)-1):
        count1=0; count0=0; i+=1; countSpace=0;
        for line in arr:
            if i<len(line):
                if line[i]=="1": count1+=1
                elif line[i]=="0": count0+=1
                elif line[i]=="-": countSpace+=1

        if countSpace>max(count0,count1):
            res.append("-")
            print str(countSpace) +" : "+str(i)+" (1: "+str(count1)+",0:"+str(count0)+")"
        elif count1> max(count0,countSpace): res.append("1")
        elif count0>= max(count1,countSpace): res.append("0")
    return res

