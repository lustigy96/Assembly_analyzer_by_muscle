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

#string creation
sourceString=[]
f_strings.write("source:\n")
for x in range(DEFINES.STRING_LEN):
    r=random.random();
    if r>0.5:
        sourceString.append('1')
        f_strings.write('1')
    else:
        sourceString.append('0')
        f_strings.write('0')

sourceString=''.join(sourceString)

prob2flip=0.1
# sourceString="10001001100110001101011011010110100100010010001001010101110000001111000001010001011000100000000100100001000001101011010000110010101110001011110100011001010100111100010101110011101110100001111111011010"
# f_strings.write("source:\n"+sourceString)
constlen=0.07
substrings0=ArraysBuilder.randomSample_constLen(sourceString,parts=250,constlen=constlen)
f_strings.write("\nlevel-0:\n")
dim2_arr2file(substrings0,f_strings)

substrings0=ArraysBuilder.flipsOnArr_zeros(substrings0,probToFlip=prob2flip)

f_strings.write("\nlevel-0-flipped:\n")
dim2_arr2file(substrings0,f_strings)

unit_by_mus=True
itr=0
while(unit_by_mus):
    itr+=1
    f_strings.write("\nlevel-"+str(itr)+":\n")
    substrings1,unit_by_mus = MERGER.uniteStrings(substrings0, constlen, len(sourceString), f_strings, DEFINES.OVERLAP_TRESHOLD_0,
                                      prob2flip);
    print len(substrings1)
    f_strings.write("\nsource:\n" + sourceString)
    f_strings.write("\nlevel-"+str(itr)+"-orgenized(len:"+str(len(substrings1))+"):\n")
    dim2_arr2file(substrings1, f_strings)
    if len(substrings1)>len(substrings0):
        # f_strings.close()
        x=1
    substrings0=substrings1
    if itr==8:
        x=1
f_strings.write("\nsource:\n"+sourceString)
res= MERGER.my_merger(substrings0,minOverlap_bits=17,prob2flip=prob2flip,sourceLen=len(sourceString),constlen=constlen) #25 for 0.3 in 200
f_strings.write("\nmy merge:\n")
for r in res: f_strings.write(r+"\n")
f_strings.close()