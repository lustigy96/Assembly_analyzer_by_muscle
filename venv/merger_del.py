import DEFINES
import ValStr
import random
import math


#valstr1,valstr2 are from ValStr class
def mergeOverlapStrings_flips(valstr1,valstr2,overlap_treshold,prob2del,sourceLen):

    letters_num1, letters_num2=0,0      #count the letters (not spaces) in each string
    badspace1, badspace2 = 0, 0         #count *middle* spaces
    tmp_space1, tmp_space2=0,0          #count spaces in the strings (in order to diffrence middle spaces from end spaces)
    flips=0
    overlap_ind_start, overlap_ind_end, ind= -1,-1,-1
    letter_ind1,letter_ind2=-1, -1
    s1,s2 =valstr1.str, valstr2.st

    for x1, x2 in zip(s1, s2):
        # count real letters (not "-"
        ind += 1
        if (x1 != '-'):
            letters_num1 += 1
            badspace1+=tmp_space1
            tmp_space1=0
            if letter_ind1<0: letter_ind1=ind
        if (x2 != '-'):
            letters_num2 += 1
            badspace2+=tmp_space2
            tmp_space2=0
            if letter_ind2<0: letter_ind2=ind
        if (x1 !='-' and x2 != '-'):
            if overlap_ind_start<0: overlap_ind_start=ind
            if x1!=x2: flips+=1

        if (x1 == '-' and overlap_ind_start >= 0): tmp_space1 +=1
        if (x2 == '-' and overlap_ind_start >= 0): tmp_space2 +=1

    overlap_ind_end = min(len(s1)-tmp_space1, len(s2)-tmp_space2)
    tot_overlap =overlap_ind_end-overlap_ind_start;

    if badspace1>math.ceil(prob2del*tot_overlap) or badspace2>math.ceil(prob2del*tot_overlap):
        return -1
    if (1.0 * tot_overlap) / min(letters_num1, letters_num1) < overlap_treshold:
        return -1.0 * tot_overlap / min(letters_num1, letters_num2)
    if flips==0:
        res=merger_over_del_only(valstr1, valstr2)
        return res
    else: #try to fix the flips

def merger_over_del_only(valstr1, valstr2):
    res = ValStr('', 0)
    i=-1
    for x1,x2 in zip(valstr1.str,valstr2.st):
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
    res = ValStr('', 0)
    s1, s2 =valstr1.st, valstr2.st
    i,j=-1,-1
    while i< len(s1) and j< len(s2) and del1<math.ceil(prob2del*len(s1)) and del2<math.ceil(prob2del*len(s2)):
        j+=1; i+=1
        if s1[i]!=s2[j] and s1[i]!='-' and s2[i]!='-':
            tmp1=s1[0:i-1]+'-'+s1[i-1:]
            tmp2=s2[0:j-1]+'-'+s1[j-1:]
            if caunt_error_val(tmp2,s2)<caunt_error_val(tmp1,s2):#del in 1
                i-=1
                del1+=1
                res.add(s2[j], [valstr2.val[j]])
            else:
                j-=1
                del2+=1
                res.add(s1[i], [valstr1.val[i]])
        else:
            if s1[i]==s2[j]: res.add(s1[i],[valstr1.val[i]+valstr2.val[j]])
            elif (s1[i] == '-'): res.add(s2[j], [valstr2.val[j]])
            elif (s2[j] == '-'): res.add(s1[i], [valstr1.val[i]])

    if del1<math.ceil(prob2del*len(s1)) or del2<math.ceil(prob2del*len(s2)):
        return -1
    else: return res


#count errors between s1, s2
def caunt_error_val(s1,s2):
    count =0;
    for x, y in zip(s1,s2):
        if x!=y and x!='-' and y!='-': count+=1
    return count
#
#
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
