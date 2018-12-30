#!/usr/bin/env python
import DEFINES
import ArraysBuilder
import MuscleRunner
import MERGER
import random

f_strings=open(DEFINES.FILES_PATH+"strings.txt","w")


def dim2_arr2file(arr,file):
    for line in arr:
        for x in line:
            file.write(str(x))
        file.write("\n")

# #string creation
# sourceString=[]
# f_strings.write("source:\n")
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

prob2flip=0.05
sourceString="1011001110001111101010000001011100011011000011001101011111000000101001011010010010100000110101001001"
f_strings.write("source:\n"+sourceString)
constlen=0.5
substrings0=ArraysBuilder.randomSample_constLen(sourceString,parts=10,constlen=constlen)
f_strings.write("\nlevel-0:\n")
dim2_arr2file(substrings0,f_strings)

substrings0=ArraysBuilder.flipsOnArr_zeros(substrings0,probToFlip=prob2flip)

f_strings.write("\nlevel-0-flipped:\n")
dim2_arr2file(substrings0,f_strings)

for i in range(6):
    f_strings.write("\nlevel-"+str(i+1)+":\n")
    substrings1 = MERGER.uniteStrings(substrings0, constlen, len(sourceString), f_strings, DEFINES.OVERLAP_TRESHOLD_0,
                                      prob2flip);
    f_strings.write("\nsource:\n" + sourceString)
    f_strings.write("\nlevel-"+str(i+1)+"-orgenized:\n")
    dim2_arr2file(substrings1, f_strings)
    substrings0=substrings1
f_strings.write("\nsource:\n"+sourceString)
