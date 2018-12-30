import DEFINES
import random
import MuscleRunner

#merge the strings comes out of muscle rightly,
# return the result if the overlap is good enough, otherwise: return -1
def mergeOverlapStrings(s1,s2,overlap_treshold,prob_to_flip):

    letters_num1, letters_num2=0,0      #count the letters (not spaces) in each string
    badspace1, badspace2 = 0, 0         #count *middle* spaces
    tmp_space1, tmp_space2=0,0          #count spaces in the strings (in order to diffrence middle spaces from end spaces)
    tot_overlap, correct= 0,0           #count the correct overlap and the total overlap
    flips=0

    result = [];
    for x1, x2 in zip(s1, s2):
        # count real letters (not "-"
        if (x1 != '-'): letters_num1 += 1
        if (x2 != '-'): letters_num2 += 1
        if tot_overlap > 0: tot_overlap += 1

        # count overlap and spaces
        if x1 == x2:
            result.append(x1)
            if x1 != '-':
                correct += 1
                tot_overlap+=1
                badspace1 += tmp_space1
                badspace2 += tmp_space2
                tmp_space1, tmp_space2 = 0, 0
            elif tot_overlap > 0:
                tmp_space1 += 1; tmp_space2 += 1;

        elif x1 == '-' and x2 != '-':
            result.append(x2)
            badspace2 += tmp_space2
            tmp_space2 = 0
            if tot_overlap > 0: tmp_space1 += 1

        elif x2 == '-' and x1 != '-':
            result.append(x1)
            badspace1 += tmp_space1
            tmp_space1 = 0
            if tot_overlap > 0: tmp_space2 += 1

        else:  # there was a flip and decision should be made
            result.append('0')
            flips += 1
            badspace1 += tmp_space1
            badspace2 += tmp_space2
            tmp_space1, tmp_space2=0,0

    tot_overlap-=max(tmp_space1,tmp_space2)
    if (1.0 * max(badspace1,badspace2)/tot_overlap) > prob_to_flip:#DEFINES.BAD_SPACE_TRESH:
        return -1
    if (1.0 * flips /tot_overlap) > 2*prob_to_flip:
        return -1-(1.0 * flips /tot_overlap)
    if (1.0 * tot_overlap) / min(letters_num1, letters_num1) > overlap_treshold:
        result = ''.join(result)
    else:
        result = -1.0 * tot_overlap / min(letters_num1, letters_num1)
    return result  # =merged\-1 for badspace\ -2 for unmatched


#unite the overlapped strings and return 2-dim array with the strings
def uniteStrings(substrings,constlen,sourceLen,f_strings,overlap_treshold,prob_to_flip):
    unite_array=[]
    for i in range(len(substrings) - 1):
        substr = substrings[i]
        arr2run = [substr, []]
        ind = i;
        if (len(substr) < constlen * sourceLen / 2):
            continue
        for s in substrings[i + 1:]:
            ind += 1
            arr2run[-1] = s
            if (len(s) <= constlen * sourceLen / 2):
                continue
            results = MuscleRunner.muscleCall(arr2run)
            if len(results) == 2:
                r = mergeOverlapStrings(results[0], results[1],overlap_treshold,prob_to_flip)
                if r >= 0:
                    f_strings.write(str(i) + ":" + str(ind) + ":\t" + r + "\n")
                    f_strings.write(str(i) + ":\t" + ''.join(results[0]) + "\n")
                    f_strings.write(str(ind) + ":\t" + ''.join(results[1]) + "\n\n")
                    unite_array.append(r)
                else: #print the anacceptable
                    f_strings.write(str(i) + ":" + str(ind) + ":\tXXX:"+str(r)+"\n")
                    f_strings.write(str(i)+":\t" + ''.join(results[0]) + "\n")
                    f_strings.write(str(ind)+":\t" + ''.join(results[1]) + "\n\n")
            if len(results) > 2:
                f_strings.write("~~~~~~~~~~~~~~~~~EROR-0~~~~~~~~~~~~~~~~~~\n")

    return filterSubstring(unite_array)

def filterSubstring(arr):
    filter_ind=[]
    arr.sort(lambda x,y: cmp(len(x), len(y)))
    for i in range(len(arr)-1):
        sub=arr[i]
        for st in arr[i+1:]:
            if(is_substring(sub,st)):
                filter_ind.append(i)
                break
    map(lambda x: arr.pop(x), sorted(filter_ind, key=lambda x: -x))
    return arr

def is_substring(sub, st):
    ans=False
    if len(sub)>len(st):
        return False
    for i in range(len(st) - len(sub)+1):
        booli=True
        for s, r in zip(st[i:], sub):
            if s != r:
                booli=False
                break
        if booli:
            ans=True
    return ans