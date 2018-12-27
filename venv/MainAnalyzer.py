#!/usr/bin/env python
import DEFINES
import ArraysBuilder
import MuscleRunner
import random

f_strings=open(DEFINES.FILES_PATH+"strings.txt","w")


def dim2_arr2file(arr,file):
    for line in arr:
        for x in line:
            file.write(str(x))
        file.write("\n")

# #string creation
# sourceString=[]
f_strings.write("source:\n")
# for x in range(DEFINES.STRING_LEN):
#     r=random.random();
#     if r>0.5:
#         sourceString.append('1')
#         f_strings.write('1')
#     else:
#         sourceString.append('0')
#         f_strings.write('0')
#
# sourceString=''.join(sourceString)

sourceString="1011001110001111101010000001011100011011000011001101011111000000101001011010010010100000110101001001"
f_strings.write(sourceString)
constlen=0.5
substrings0=ArraysBuilder.randomSample_constLen(sourceString,parts=10,constlen=constlen)
f_strings.write("\nparts-0:\n")
dim2_arr2file(substrings0,f_strings)

substrings0=ArraysBuilder.flipsOnArr_zeros(substrings0,probToFlip=0.05)
f_strings.write("\nparts-0-flipped:\n")
dim2_arr2file(substrings0,f_strings)

f_strings.write("\nparts-1:\n")
substrings1=[]
for i in range(len(substrings0)-1):
    substr=substrings0[i]
    arr2run=[substr,[]]
    ind=i;
    if(len(substr)<constlen*len(sourceString)/2):
        continue
    for s in substrings0[i+1:]:
        ind+=1
        arr2run[-1]=s
        if (len(s) <= constlen * len(sourceString) / 2):
            continue
        results=MuscleRunner.muscleCall(arr2run)
        if ind==2:
            debuf=1
        if len(results)==2:
            r=ArraysBuilder.mergeOverlapStrings(results[0],results[1])
            if r!=-1:
                f_strings.write(str(i)+":"+str(ind)+":\t"+r+"\n")
                f_strings.write(str(i)+":\t" + ''.join(results[0]) + "\n")
                f_strings.write(str(ind)+":\t" + ''.join(results[1]) + "\n\n")
                substrings1.append(r)
        if len(results)>2:
            f_strings.write("~~~~~~~~~~~~~~~~~EROR-0~~~~~~~~~~~~~~~~~~\n")


f_strings.close()