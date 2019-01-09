#!/usr/bin/env python
import DEFINES
import ArraysBuilder
import MuscleRunner
import MERGER
import plot
import MATLAB
import random
import matplotlib.pyplot as plt



def dim2_arr2file(arr,file):
    for line in arr:
        for x in line:
            file.write(str(x))
        file.write("\n")

def itterations(f_strings,substrings0,constlen, sourceString,prob2flip):
    f_strings.write("\nlevel-0-flipped:\n")
    dim2_arr2file(substrings0, f_strings)

    unit_by_mus = True
    itr = 0
    while (unit_by_mus):
        itr += 1
        f_strings.write("\nlevel-" + str(itr) + ":\n")
        substrings1, unit_by_mus = MERGER.uniteStrings(substrings0, constlen, len(sourceString), f_strings,
                                                       DEFINES.OVERLAP_TRESHOLD_0,
                                                       prob2flip);
        print len(substrings1)
        f_strings.write("\nsource:\n" + sourceString)
        f_strings.write("\nlevel-" + str(itr) + "-orgenized(len:" + str(len(substrings1)) + "):\n")
        dim2_arr2file(substrings1, f_strings)
        if len(substrings1) > len(substrings0):
            # f_strings.close()
            x=1
        substrings0 = substrings1

    f_strings.write("\nsource:\n" + sourceString)
    res = MERGER.my_merger(substrings0, minOverlap_bits=17, prob2flip=prob2flip, sourceLen=len(sourceString),
                           constlen=constlen)  # 25 for 0.3 in 200
    f_strings.write("\nmy merge:\n")
    for r in res: f_strings.write(r + "\n")

    return res


# sourceString="10001001100110001101011011010110100100010010001001010101110000001111000001010001011000100000000100100001000001101011010000110010101110001011110100011001010100111100010101110011101110100001111111011010"


if DEFINES.FLIP_MOD:
    # main
    # prob2flip=0.1
    # constlen=45
    # substrings0=ArraysBuilder.randomSample_constLen(sourceString,parts=250,constlen=constlen)
    # substrings0=ArraysBuilder.flipsOnArr_zeros(substrings0,probToFlip=prob2flip)
    # res=itterations(f_strings,substrings0,constlen, sourceString,prob2flip)

    vec_strings_len=[500,1000,2000,4000]
    vec_string_constlen=[[50,80,100],[50,100,200],[50,80,100,200],[50,100,400]]
    vec_flips_prob=[0,0.05,0.1,0.15]
    parts_step=50
    # vec_strings_len = [100]
    # vec_string_constlen = [[30]]
    # vec_flips_prob = [0.1]
    # parts_step = 50

    i=0
    for i_str_len in range(len(vec_strings_len)):
        for constlen in vec_string_constlen[i_str_len]:
            sourceString = ArraysBuilder.createString(vec_strings_len[i_str_len])
            flips_res = {"X": [], "Y": [], "Z": []}
            fullX=False
            i += 2
            for prob2flip in vec_flips_prob:
                parts=0
                flips_res["Y"].append(prob2flip)

                while parts<0.5*vec_strings_len[i_str_len]:
                    parts+=parts_step
                    if not fullX: flips_res["X"].append(parts)
                    f_strings = open(DEFINES.FILES_PATH + "strings.txt", "w")
                    f_strings.write("source:\n" + sourceString + "\n")
                    substrings0=ArraysBuilder.randomSample_constLen(sourceString,parts=parts,constlen=constlen)
                    substrings0=ArraysBuilder.flipsOnArr_zeros(substrings0,probToFlip=prob2flip)
                    res=itterations(f_strings,substrings0,constlen, sourceString,prob2flip)
                    error=0
                    for r in res: error+= (MuscleRunner.calc_err_bestfit(sourceString,r))[0]
                    flips_res["Z"].append(1.0*error/len(sourceString))
                    f_strings.close()
                fullX=True
            plot.py_plotAll(flips_res,i,"flips", "parts", "error prob", "errors",1,1)
            MATLAB.makeMATLAB("flips_"+str(vec_strings_len[i_str_len])+"_constlen_"+str(constlen), flips_res, parts_step, parts, 0, 0.15, "parts", "error prob", "error prob", gapX=parts_step, gapY=0.05)
    print flips_res["Z"]
    plt.show()

# sourceString="10001001100110001101011011010110100100010010001001010101110000001111000001010001011000100000000100100001000001101011010000110010101110001011110100011001010100111100010101110011101110100001111111011010"
# f_strings = open(DEFINES.FILES_PATH + "strings.txt", "w")
# prob2del=0.05
# constlen=50
# substrings0=ArraysBuilder.randomSample_constLen(sourceString,parts=50,constlen=constlen)
# f_strings.write("\nlevel-0:\n")
# dim2_arr2file(substrings0,f_strings)
#
# substrings0=ArraysBuilder.delOnArr(substrings0, probToDel=prob2del)
# f_strings.write("\nlevel-0-dels:\n")
# dim2_arr2file(substrings0,f_strings)
#
#
# #iteraions
# dim2_arr2file(substrings0, f_strings)
#
# unit_by_mus = True
# itr = 0
# while (unit_by_mus):
#     itr += 1
#     f_strings.write("\nlevel-" + str(itr) + ":\n")
#     substrings1, unit_by_mus = MERGER.uniteStrings(substrings0, constlen, len(sourceString), f_strings,
#                                                    DEFINES.OVERLAP_TRESHOLD_0,
#                                                    prob2del);
#     print len(substrings1)
#     f_strings.write("\nsource:\n" + sourceString)
#     f_strings.write("\nlevel-" + str(itr) + "-orgenized(len:" + str(len(substrings1)) + "):\n")
#     dim2_arr2file(substrings1, f_strings)
#     if len(substrings1) > len(substrings0):
#         # f_strings.close()
#         x = 1
#     substrings0 = substrings1
#
# f_strings.write("\nsource:\n" + sourceString)
# res = MERGER.my_merger(substrings0, minOverlap_bits=17, prob2flip=prob2del, sourceLen=len(sourceString),
#                        constlen=constlen)  # 25 for 0.3 in 200
# f_strings.write("\nmy merge:\n")
# for r in res: f_strings.write(r + "\n")
