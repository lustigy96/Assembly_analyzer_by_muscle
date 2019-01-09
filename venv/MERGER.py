import DEFINES
import random
import MuscleRunner
import math

#merge the 2-strings comes out of muscle rightly,
# return the result if the overlap is good enough, otherwise: return -1
def mergeOverlapStrings_flips(s1,s2,overlap_treshold,prob_to_flip,sourceLen):

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
                badspace1 += tmp_space1
                badspace2 += tmp_space2
                tmp_space1, tmp_space2 = 0, 0
                if tot_overlap==0: tot_overlap+=1
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
            if tot_overlap==0:
                tot_overlap+=1

    tot_overlap-=max(tmp_space1,tmp_space2)
    if DEFINES.FLIP_MOD:
        if(badspace1)>math.floor(prob_to_flip*tot_overlap) or (badspace2)>math.floor(prob_to_flip*tot_overlap):
        # if (1.0 * max(badspace1,badspace2)/sourceLen) > prob_to_flip:#DEFINES.BAD_SPACE_TRESH:
            return -1
        if (1.0 * (flips+badspace1+badspace2)/tot_overlap) > 1.5*prob_to_flip: #(1.0 * flips /tot_overlap) > 2*prob_to_flip:
            return -1-(1.0 * flips /tot_overlap)
        if (1.0 * tot_overlap) / min(letters_num1, letters_num1) >= overlap_treshold:
            result = ''.join(result)
        else:
            result = -1.0 * tot_overlap / min(letters_num1, letters_num2)
        return result  # =merged\-1 for badspace\ -2 for unmatched
    if DEFINES.DEL_MOD:
        if(badspace1)>math.floor(prob_to_flip*tot_overlap) or (badspace2)>math.floor(prob_to_flip*tot_overlap):
        # if (1.0 * max(badspace1,badspace2)/sourceLen) > prob_to_flip:#DEFINES.BAD_SPACE_TRESH:
            return -1
        if (1.0 * (flips)/tot_overlap) > 1.5*prob_to_flip: #(1.0 * flips /tot_overlap) > 2*prob_to_flip:
            return -1-(1.0 * flips /tot_overlap)
        if (1.0 * tot_overlap) / min(letters_num1, letters_num1) >= overlap_treshold:
            result = ''.join(result)
        else:
            result = -1.0 * tot_overlap / min(letters_num1, letters_num2)
        return result  # =merged\-1 for badspace\ -2 for unmatched

# unite the overlapped strings BY CALLING MUSCLE and return 2-dim array with the strings
# USES: mergeOverlapStrings_flips
def uniteStrings(substrings,constlen,sourceLen,f_strings,overlap_treshold,prob_to_flip):
    unite_array=[]
    is_united=False
    merged_str = [False] * len(substrings)
    if constlen<1:
        constlen=constlen * sourceLen
    for i in range(len(substrings) - 1):
        substr = substrings[i]
        arr2run = [substr, []]
        ind = i;
        if (len(substr) < constlen / 2):
            merged_str[i]=True
            continue
        for s in substrings[i + 1:]:
            ind += 1
            arr2run[-1] = s
            if (len(s) <= constlen / 2):
                continue
            results = MuscleRunner.muscleCall(arr2run)
            if len(results) == 2:
                # if DEFINES.FLIP_MOD: r = mergeOverlapStrings_flips(results[0], results[1],overlap_treshold,prob_to_flip,sourceLen)
                r = mergeOverlapStrings_flips(results[0], results[1],overlap_treshold,prob_to_flip,sourceLen)
                if r >= 0:
                    is_united=True
                    merged_str[i]=True
                    merged_str[ind]=True
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

    for i in range(len(substrings)):
        if not merged_str[i]:
            unite_array.append(substrings[i])

    return filterSubstring(unite_array,prob_to_flip), is_united

# filter the substrings in arr
# USES: is_substring_one2zero
def filterSubstring(arr,prob2flip):
    filter_ind=[]
    arr.sort(lambda x,y: cmp(len(x), len(y)))
    for i in range(len(arr)-1):
        sub=arr[i]
        # for st in arr[i+1:]:
        for j in range(len(arr[i + 1:])):
            st=(arr[i + 1:])[j]
            ans, s_fix = is_substring_one2zero(sub, st, prob2flip)
            if(is_substring(sub,st)):
                filter_ind.append(i)
                break
            elif(ans):
                 filter_ind.append(i)
                 arr[i + 1:][j]=s_fix
                 break
    map(lambda x: arr.pop(x), sorted(filter_ind, key=lambda x: -x))
    return arr

# return true only if sub is a substing og st EXACTLY
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

#return true and the fixed string: if sub is a substring of st WITH SOME FLIPS
def is_substring_one2zero(sub, st,prob2flip):
    ans=False
    count_err=0
    if len(sub)>len(st): return False, -1
    for i in range(len(st) - len(sub)+1):
        booli=True
        for s, r in zip(st[i:], sub):
            if s != r:
                if count_err>math.ceil(2*prob2flip*len(sub)):
                    booli=False
                    count_err=0
                    break
                count_err+=1

        if booli:
            s= catStrings_one2zero(st[i:], sub, 0)
            return True,s
    return False,-1

#count errors between s1, s2
def caunt_error_val(s1,s2):
    count =0;
    for x, y in zip(s1,s2):
        if x!=y: count+=1
    return count

#cat 2 strings -> min error and max overlap (priority to min errors)
def my_cat_2string(first,second,minOverlap_bits,prob2flip,sourceLen):
    min_err_ind=-1
    minOverlap_bits=int(math.floor(0.25*min(len(first),len(second))))
    min_count_err=max(len(first),len(second))
    for i in range(len(first)-minOverlap_bits):
        tmp=(caunt_error_val(first[i:], second))
        if tmp<math.ceil(1.5*prob2flip*min(len(first)-i,len(second)))and tmp<min_count_err:
            min_err_ind, min_count_err=i, tmp
    if min_err_ind==-1:
        return min_err_ind, max(first,second)
    return min_err_ind,tmp

#try to merge all the strings in substrings, and return the all final fregments results
# USES: my_cat_2string
def my_merger(substrings,minOverlap_bits,prob2flip,sourceLen,constlen):
    # # filter the strings with constLen - MAYBE FROM SOME SPESIFIC LEN AND UNDER IT
    # substrings = [k for k in substrings if len(k)>constlen*sourceLen]

    res=substrings[0];
    other=substrings[1:]
    booli=True
    all_final=[]

    while len(other)>0:
        if not booli: #cant append anything to res
            all_final.append(res)
            res=other[0]
            if len(other)==1:other=[]
            else: other=other[1:]
        booli=False

        for i in range(len(other)): #try to append substring to res
            ind1, error1 = my_cat_2string(res, other[i], minOverlap_bits,prob2flip,sourceLen)
            ind2, error2 = my_cat_2string(other[i], res, minOverlap_bits,prob2flip,sourceLen)
            if ind1 > 0 or ind2 > 0:
                if error1 < error2:
                    print ind1
                    print res
                    print other[i]
                    res = catStrings_one2zero(res,other[i],ind1)#res[0:ind1] + other[i]  # fix flips
                else:
                    print ind2
                    print other[i]
                    print res
                    res = catStrings_one2zero(other[i],res,ind2)# other[i][0:ind2] + res  # fix flips
                if len(other) == 1: other = []
                else: other=other[0:i]+other[i+1:]
                booli=True
                break
    all_final.append(res)
    return all_final

#put arr in muscle and merge the output
# USES: merge_mus_all_output
def mus_all(arr,f_strings):
    results=MuscleRunner.muscleCall(arr)
    f_strings.write("final by muscle:\n")
    res_all=merge_mus_all_output(results)
    res_all=''.join(res_all)
    f_strings.write(res_all+"\n\n")
    for r in results: f_strings.write(''.join(r)+"\n")

#used to merge the output of muscle - for a lot of strings
def merge_mus_all_output(arr):#calc the final string out of samples in arr, fix: 1 to 0
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

        if count0>0:
            res.append("0")
        elif count1> 0: res.append("1")
    return res

#concat the string from indx to the end, but fix 1 to 0 if flipped
def catStrings_one2zero(s1,s2,indx):
    res=s1[0:indx]
    for c1,c2 in zip(s1[indx:],s2):
        if c1==c2: res+=c1
        else: res+='0'
    if len(s2)>len(s1[indx:]):
        res+=s2[len(s1[indx:]):]
    elif len(s1[indx:])>len(s2):
        res += s1[len( s1[indx+len(s2):] ):]
    return res

