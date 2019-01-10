import DEFINES
from ValStr import ValStr
import random
import math
import MuscleRunner


#valstr1,valstr2 are from ValStr class
def mergeOverlapStrings_del(valstr1,valstr2,overlap_treshold,prob2del,sourceLen):

    flips=0
    s1,s2 =valstr1.st, valstr2.st

    letters_num1 = s1.count('1') + s1.count('0')
    letters_num2 = s2.count('1') + s2.count('0')

    letter_ind1_start = min(list(s1).index('0'),list(s1).index('1'))
    letter_ind2_start = min(list(s2).index('0'),list(s2).index('1'))
    overlap_ind_start = max(letter_ind1_start,letter_ind2_start)

    reverse1=list(s1); reverse1.reverse()
    reverse2=list(s2); reverse2.reverse()
    letter_ind1_end = max(len(reverse1)- 1 - reverse1.index('1'),len(reverse1)- 1 - reverse1.index('0'))
    letter_ind2_end = max(len(reverse2)- 1 - reverse2.index('1'),len(reverse2)- 1 - reverse2.index('0'))
    overlap_ind_end = min(letter_ind1_end,letter_ind2_end)

    tot_overlap =overlap_ind_end-overlap_ind_start;

    badspace1= s1[overlap_ind_start:overlap_ind_end+1].count('-')
    badspace2= s2[overlap_ind_start:overlap_ind_end+1].count('-')

    for x1, x2 in zip(s1, s2): # count flips
        if x1 != x2 and x1 != '-' and x2 !='-': flips+=1


    if badspace1>math.ceil(prob2del*tot_overlap) or badspace2>math.ceil(prob2del*tot_overlap):
        return [], -1
    if (1.0 * tot_overlap) / min(letters_num1, letters_num1) < overlap_treshold:
        return [], -1.0 * tot_overlap / min(letters_num1, letters_num2)
    if flips==0:
        res=merger_over_del_only(valstr1, valstr2)
        return res, 1
    else: #try to fix the flips
        res,ans = fix_dels(valstr1, valstr2, prob2del)
        if ans>=0: return res, -2
        return [], -1-1.0*flips/tot_overlap

def merger_over_del_only(valstr1, valstr2):
    res = ValStr('', 0)
    i=-1
    for x1,x2 in zip(valstr1.st,valstr2.st):
        i+=1
        if (x1==x2): res.add(x1,[valstr1.val[i]+valstr2.val[i]])
        elif (x1=='-'): res.add(x2, [valstr2.val[i]])
        elif (x2=='-'): res.add(x1, [valstr1.val[i]])
        elif (valstr1.val[i] > valstr2[i]): res.add(x1, [valstr1.val[i]])
        elif (valstr1.val[i] < valstr2[i]): res.add(x2, [valstr2.val[i]])
        else: res.add('0', [valstr2.val[i]])
    return res


def fix_dels(valstr1, valstr2, prob2del):
    del1,del2=0,0
    prob_tresh=prob2del*1.5;
    res = ValStr('', 0)
    s1, s2 =''.join(valstr1.st), ''.join(valstr2.st)
    errors_min=caunt_error_val(s1,s2)

    i,j=-1,-1
    while i < len(s1)-1 and j< len(s2)-1 and del1 < math.ceil(prob_tresh*len(s1)) and del2 < math.ceil(prob_tresh*len(s2)):
        j+=1; i+=1
        if s1[i]!=s2[j] and s1[i]!='-' and s2[i]!='-':
            tmp1 = s1[0:i-1] + '-' + s1[i-1:]
            tmp2 = s2[0:j-1] + '-' + s1[j-1:]
            e1 = caunt_error_val(tmp1,s2)
            e2 = caunt_error_val(tmp2,s2)
            if e1 < e2 and e1< errors_min:#del in 1
                i-=1
                del1+=1
                errors_min=e1
                res.add(s2[j], [valstr2.val[j]])
            elif e2 < errors_min:
                j-=1
                errors_min=e2
                del2+=1
                res.add(s1[i], [valstr1.val[i]])
        else:
            if s1[i]==s2[j]: res.add(s1[i],[valstr1.val[i]+valstr2.val[j]])
            elif (s1[i] == '-'): res.add(s2[j], [valstr2.val[j]])
            elif (s2[j] == '-'): res.add(s1[i], [valstr1.val[i]])

    if del1 > math.ceil(prob_tresh*len(s1)) or del2 > math.ceil(prob_tresh*len(s2)) or caunt_error_val > math.ceil(prob2del*len(s2)):
        return [], -1
    else: return res , 1


#count errors between s1, s2
def caunt_error_val(s1,s2):
    count =0;
    for x, y in zip(s1,s2):
        if x!=y and x!='-' and y!='-': count+=1
    return count




def uniteStrings(substrings_val,constlen,sourceLen,f_strings,overlap_treshold,prob_to_del):
    unite_array=[]
    is_united=False
    merged_str = [False] * len(substrings_val)
    if constlen<1:
        constlen=constlen * sourceLen
    for i in range(len(substrings_val) - 1):
        substr = substrings_val[i].st
        arr2run = [substr, []]
        ind = i;
        if (len(substr) < constlen / 2):
            merged_str[i]=True
            continue
        for s_val in substrings_val[i + 1:]:
            s=s_val.st
            ind += 1
            arr2run[-1] = s
            if (len(s) <= constlen / 2):
                continue
            results = MuscleRunner.muscleCall(arr2run)
            if len(results) == 2:
                res1=fit_val(substrings_val[i],results[0])
                res2=fit_val(s_val,results[1])

                # if DEFINES.FLIP_MOD: r = mergeOverlapStrings_flips(results[0], results[1],overlap_treshold,prob_to_flip,sourceLen)
                r,ans = mergeOverlapStrings_del(res1, res2,overlap_treshold,prob_to_del,sourceLen)
                if  ans >= 0:
                    is_united=True
                    merged_str[i]=True
                    merged_str[ind]=True
                    f_strings.write(str(i) + ":" + str(ind) + ":\t" + (r.st) + "\n")
                    f_strings.write(str(i) + ":\t" + ''.join(results[0]) + "\n")
                    f_strings.write(str(ind) + ":\t" + ''.join(results[1]) + "\n\n")
                    unite_array.append(r)
                else: #print the anacceptable
                    f_strings.write(str(i) + ":" + str(ind) + ":\tXXX:"+str(ans)+"\n")
                    f_strings.write(str(i)+":\t" + ''.join(results[0]) + "\n")
                    f_strings.write(str(ind)+":\t" + ''.join(results[1]) + "\n\n")
            if len(results) > 2:
                f_strings.write("~~~~~~~~~~~~~~~~~EROR-0~~~~~~~~~~~~~~~~~~\n")

    for i in range(len(substrings_val)):
        if not merged_str[i]:
            unite_array.append(substrings_val[i])

    # return filterSubstring(unite_array,prob_to_del), is_united
    return unite_array, is_united

def fit_val(str_val,st):
    ind_val=0;
    res=ValStr(st,0)
    for i in range(len(st)):
        if st[i]!='-':
            res.edit_val(i, str_val.val[ind_val])
            ind_val+=1
    return res

# def filterSubstring(arr,prob_to_del):
#     filter_ind=[]
#     arr.sort(lambda x,y: cmp(len(x), len(y)))
#     for i in range(len(arr)-1):
#         sub=arr[i]
#         # for st in arr[i+1:]:
#         for j in range(len(arr[i + 1:])):
#             st=(arr[i + 1:])[j]
#             ans, s_fix = is_substring_one2zero(sub, st, prob2flip)
#             if(is_substring(sub,st)):
#                 filter_ind.append(i)
#                 break
#             elif(ans):
#                  filter_ind.append(i)
#                  arr[i + 1:][j]=s_fix
#                  break
#     map(lambda x: arr.pop(x), sorted(filter_ind, key=lambda x: -x))
#     return arr


# def fit_and_val(valstr1,valstr2,prob2del):
#     mistakes=0
#     i, j = -1, -1;
#     s1_zero,s1_ones=zero_one_array(list(avalstr1.st))
#     s2_zero,s2_ones=zero_one_array(lins(avalstr2.st))
#     while j < (min(len(s2_ones), len(s2_zero)) - 2) and mistakes < math.ceil(prob2del * (len(valstr1))):
#         j += 1;
#         i += 1;
#
#         if(s1_zero[i]==s2_zero[j]): res.add(''.join(['0']*s1_zero[i]), [1] * s1_zero[i]) #sucess0
#         elif(s1_ones[i]==s2_ones[j]): res.add(''.join(['1']*s1_ones[i]), [1] * s1_ones[i]) #succsees1
#
#         elif()
#
#
# def fitandval(valstr1,valstr2,prob2del): # mistakes calculations
#     i ,j = -1, -1;
#     mistakes, flip=0
#     gues_Zeros,gues_Ones=zero_one_array(avalstr1.st)
#     org_Zeros,org_Ones=zero_one_array(avalstr2.st)
#     res= ValStr('',0)
#     # for j in range(min(len(gues_Ones),len(gues_Zeros))-1):
#     while j < (min(len(gues_Ones), len(gues_Zeros)) - 2) and mistakes < math.ceil(prob2del*(len(valstr1))):
#         j += 1;
#         i += 1;
#         if i < (min(len(org_Ones), len(org_Ones)) - 3):
#             if gues_Ones[j] > 0:
#
#                 if org_Ones[i] == gues_Ones[j]:  # success
#                     print "success 1"
#                     res.add(''.join(['1']*org_Ones[i]),[1]*org_Ones[i])
#                     continue;
#
#                 if org_Ones[i] == 0:  # shift or flip-begin
#
#                     if org_Ones[i + 1] + org_Zeros[i] == gues_Ones[j]:
#                         print "0 to 1 flip" #decide on 0, low valued
#                         flip += org_Zeros[i]
#                         res.add(''.join(['0']*org_Zeros[i]),[0] * org_Zeros[i])
#                         res.add(join(['1']*org_Ones[i+1]), [1] * org_Ones[i+1])
#                         mistakes += org_Zeros[i]
#                         i += 1
#                         continue;
#
#                     elif i <= 1:  # shift
#                         print"shift - 1 section cont"
#                         j -= 1;
#                         shift += org_Zeros[i];
#                         mistakes += org_Zeros[i];
#                         continue;
#                     print "nothing"
#                 else:
#                     if (org_Ones[i] + org_Zeros[i + 1] == gues_Ones[j] + gues_Zeros[j + 1]):  # flip end
#                         print "flip end"
#                         newkey_ones.extend((org_Ones[i], 0))
#                         newkey_zeros.extend((0, org_Zeros[i + 1]))
#                         flip += abs(org_Ones[i] - gues_Ones[j])
#                         mistakes += abs(org_Ones[i] - gues_Ones[j])
#                         i += 1;
#                         j += 1;
#                         continue;
#                     if (i + 2 < min(len(org_Zeros), len(org_Ones)) and org_Ones[i] + org_Ones[i + 2] == gues_Ones[j] and
#                             gues_Zeros[j + 1] == org_Zeros[i + 3]):  # deleted middle
#                         print "delete 0"
#                         miss0 += gues_Zeros[i + 1]
#                         i += 2;
#                         continue;
#                     if (org_Ones[i] - gues_Ones[j] == 1):  # deleted
#                         newkey_ones.append(org_Ones[i])
#                         newkey_zeros.append(0)
#                         print "miss 1"
#                         miss1 += 1;
#                         mistakes += 1;
#                         continue;
#                     if (gues_Ones[j] - org_Ones[i] == 1):  # added
#                         newkey_ones.append(org_Ones[i])
#                         newkey_zeros.append(0)
#                         print "add 1"
#                         add1 += 1;
#                         mistakes += 1;
#                         continue;
#                     if gues_Ones[j] - org_Ones[i] > 1:
#                         t = i;
#                         currlen = 0;
#                         while (t < min(len(gues_Ones), len(gues_Zeros)) and currlen < gues_Ones[j]):
#                             currlen += (org_Zeros[t] + org_Ones[t])
#                             newkey_zeros.append(org_Zeros[t]);
#                             newkey_ones.append(org_Ones[t]);
#                             t += 1;
#                         if currlen == gues_Ones[j]:  # flip
#                             print "flip 0 to 1"
#                             flip += (sum(org_Zeros[i:t - 1]))
#                         else:  # deleted
#                             print"delete 0"
#                             miss0 += (sum(org_Zeros[i:t - 1]))
#                         mistakes += (sum(org_Ones[i:t - 1]))
#                         i = t - 1
#                         continue;
#                     print "nothing"
#         # zeros:
#         if gues_Zeros[j] > 0:
#             if org_Zeros[i] == gues_Zeros[j]:  # success
#                 newkey_zeros.append(org_Zeros[i])
#                 print "success 0"
#                 newkey_ones.append(0)
#                 continue;
#             if org_Zeros[i] == 0:  # shift or flip-begin
#                 if org_Zeros[i + 1] + org_Ones[i] == gues_Zeros[j]:
#                     print "flip 1 to 0"
#                     flip = flip + org_Ones[i]
#                     newkey_ones.extend([org_Ones[i], 0])
#                     newkey_zeros.extend([0, org_Zeros[i + 1]])
#                     mistakes += org_Ones[i]
#                     i += 1
#                     continue;
#                 elif i <= 1:  # shift
#                     print"shift - 0 section cont"
#                     j = j - 1
#                     shift += org_Ones[i];
#                     mistakes += org_Ones[i]
#                     continue;
#                 print "nothing"
#             else:
#                 if (org_Zeros[i] + org_Ones[i + 1] == gues_Zeros[j] + gues_Ones[j + 1]):  # flip end
#                     print "flip end"
#                     newkey_zeros.extend((org_Zeros[i], 0))
#                     newkey_ones.extend((0, org_Ones[i + 1]))
#                     flip += abs(org_Zeros[i] - gues_Zeros[j]);
#                     mistakes += abs(org_Zeros[i] - gues_Zeros[j]);
#                     i += 1;
#                     j += 1;
#                     continue;
#                 if (i + 2 < min(len(org_Zeros), len(org_Ones)) and org_Zeros[i] + org_Zeros[i + 2] == gues_Zeros[j] and
#                         gues_Ones[j + 1] == gues_Ones[i + 3]):  # deleted middle
#                     print "delete 1"
#                     miss1 += gues_Ones[i + 1]
#                     i += 2;
#                     continue;
#                 if (org_Zeros[i] - gues_Zeros[j] == 1):  # deleted
#                     print "deleted 0"
#                     newkey_zeros.append(org_Zeros[i])
#                     newkey_ones.append(0)
#                     miss0 += 1;
#                     mistakes += 1;
#                     continue;
#                 if (gues_Zeros[j] - org_Zeros[i] == 1):  # added
#                     print "add 0"
#                     newkey_zeros.append(org_Zeros[i])
#                     newkey_ones.append(0)
#                     add0 += 1;
#                     mistakes += 1
#                     continue;
#                 if gues_Zeros[j] - org_Zeros[i] > 1:
#                     t = i;
#                     currlen = 0;
#                     while (t < min(len(gues_Ones), len(gues_Zeros)) and currlen < gues_Zeros[j]):
#                         currlen += (org_Zeros[t] + org_Ones[t])
#                         newkey_zeros.append(org_Zeros[t]);
#                         newkey_ones.append(org_Ones[t]);
#                         t += 1;
#                     if currlen == gues_Zeros[j]:  # flip
#                         print "flip 1 to 0"
#                         flip += (sum(org_Ones[i:t - 1]))
#                     else:  # deleted
#                         print"delete 1"
#                         miss1 += (sum(org_Ones[i:t - 1]))
#                     mistakes += (sum(org_Ones[i:t - 1]))
#                     i = t - 1
#                     continue;
#                 print "nothing"
