import DEFINES
from ValStr import ValStr
import random
import math
import MuscleRunner
import numpy as np

#valstr1,valstr2 are from ValStr class
def mergeOverlapStrings_del(valstr1,valstr2,overlap_treshold,prob2del,sourceLen):
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
    flips = max(0, np.sum(np.array(list(s1)) != np.array(list(s2))) - s1.count('-') - s2.count('-'))

    if badspace1 > math.ceil(prob2del*tot_overlap) or badspace2 > math.ceil(prob2del*tot_overlap):
        return [], -1
    if (1.0 * tot_overlap) / min(letters_num1, letters_num1) < overlap_treshold:
        return [], -1.0 * tot_overlap / min(letters_num1, letters_num2)
    if flips==0:
        return merger_over_del_only(valstr1, valstr2), 1
    else: #try to fix the flips
        res,ans = fix_dels(valstr1, valstr2, prob2del)
        if ans>=0: return res, 0
        return [], -1-1.0*flips/tot_overlap

#merge only the overlapped, from the begining
def merger_over_del_only(valstr1, valstr2):

    length= min( len(valstr1.st), len(valstr2.st) )
    st=np.array(['F'] * len(zip(valstr1.st, valstr2.st)))
    val=np.array([0]*len(zip(valstr1.st, valstr2.st)))

    arr1 = np.array(list(valstr1.st[:length]))
    arr2 = np.array(list(valstr2.st[:length]))

    st[(arr1 == arr2)] = arr1[(arr1 == arr2)]
    val[(arr1 == arr2)] = valstr1.val[:length][(arr1 == arr2)]  + valstr2.val[:length][(arr1 == arr2)]

    st[(arr1 == '-')] = arr2[(arr1 == '-')]
    val[(arr1 == '-')] = valstr2.val[:length][(arr1 == '-')]

    st[(arr2 == '-')] = arr1[(arr2 == '-')]
    val[(arr2 == '-')] = valstr1.val[:length][(arr2 == '-')]

    st[np.logical_and(st=='F', valstr1.val[:length] > valstr2.val[:length]) ] = arr1[ np.logical_and(st=='F' , valstr1.val[:length] > valstr2.val[:length] ) ]
    val[np.logical_and(st=='F', valstr1.val[:length] > valstr2.val[:length])] = valstr1.val[:length][np.logical_and(st=='F' , valstr1.val[:length] > valstr2.val[:length])]

    st[np.logical_and(st=='F' , valstr1.val[:length] < valstr2.val[:length] )] = arr2[ np.logical_and(st=='F' , valstr1.val[:length] < valstr2.val[:length]) ]
    val[np.logical_and(st=='F' , valstr1.val[:length] < valstr2.val[:length])] = valstr2.val[:length][np.logical_and(st=='F' , valstr1.val[:length] < valstr2.val[:length])]

    st[(st=='F')] = ['0']* len(st[(st=='F')])
    val[(st=='F')] = valstr2.val[:length][(st=='F')]

    # for x1,x2 in zip(valstr1.st,valstr2.st):
    #     i+=1
    #     if (x1==x2): res.cat(x1,[valstr1.val[i]+valstr2.val[i]])
    #     elif (x1=='-'): res.cat(x2, [valstr2.val[i]])
    #     elif (x2=='-'): res.cat(x1, [valstr1.val[i]])
    #     elif (valstr1.val[i] > valstr2.val[i]): res.cat(x1, [valstr1.val[i]])
    #     elif (valstr1.val[i] < valstr2.val[i]): res.cat(x2, [valstr2.val[i]])
    #     else: res.cat('0', [valstr2.val[i]])
    res=ValStr(''.join(st),val)
    return res


def uniteStrings(substrings_val,constlen,sourceLen,f_strings,overlap_treshold,prob_to_del):
    unite_array=[]
    is_united=False
    merged_str = [False] * len(substrings_val)
    if constlen<1:
        constlen= int(constlen * sourceLen)
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
            if (len(s) <= constlen / 2): continue
            results = MuscleRunner.muscleCall(arr2run)
            if len(results) == 2:
                res1=fit_val(substrings_val[i],results[0])
                res2=fit_val(s_val,results[1])
                r,ans = mergeOverlapStrings_del(res1, res2,overlap_treshold,prob_to_del,sourceLen)
                if  ans >= 0:
                    is_united=True
                    merged_str[i]=True
                    merged_str[ind]=True
                    f_strings.write(str(i) + ":" + str(ind) + ":---\t---" + str(ans) + "\n")
                    f_strings.write(str(i) + ":" + str(ind) + ":\t" + (r.st) + "\n")
                    f_strings.write(str(i) + ":\t" + ''.join(results[0]) + "\n")
                    f_strings.write(str(ind) + ":\t" + ''.join(results[1]) + "\n\n")
                    unite_array.append(r)

                # else: #print the anacceptable
                    # f_strings.write(str(i) + ":" + str(ind) + ":\tXXX:"+str(ans)+"\n")
                    # f_strings.write(str(i)+":\t" + ''.join(results[0]) + "\n")
                    # f_strings.write(str(ind)+":\t" + ''.join(results[1]) + "\n\n")
            if len(results) > 2:
                f_strings.write("~~~~~~~~~~~~~~~~~EROR-0~~~~~~~~~~~~~~~~~~\n")

    sval_np=np.array(substrings_val)
    unite_array.extend(sval_np[ np.logical_not(merged_str)].tolist())
    return filterSubstring(unite_array,prob_to_del), is_united

#if st has new spaces, it fits the val to the right numbers, and not "-"
def fit_val(str_val_original,st_new):
    inds = np.array(np.array(list(st_new)) != '-')
    val_new = np.ones(len(inds))
    val_new[inds] = str_val_original.val

    return ValStr(st_new,val_new)

# filter the substrings in arr
def filterSubstring(arr,prob2del):
    filter_ind=[]
    arr.sort(lambda x,y: cmp(len(x.st), len(y.st)))
    for i in range(len(arr)-1):
        sub=arr[i].st
        for j in range(len(arr[i + 1:])):
            st=(arr[i + 1:])[j].st
            ans_p,ind = is_substring(sub,st)
            res, ans_np = is_substring_over_del(arr[i], arr[i + 1:][j], prob2del)
            # res, ans_np = fix_dels(arr[i], arr[i + 1:][j], prob2del)
            if ans_p:
                vec_val= np.concatenate( (np.array([0]* ind), arr[i].val, np.array([0]*(len(st)-len(sub)-ind))), axis=None)
                arr[i+1:][j].add2val(vec_val)
                filter_ind.append(i)
                break
            elif(ans_np==1):
                arr[i + 1:][j]=res
                filter_ind.append(i)
                break
    map(lambda x: arr.pop(x), sorted(filter_ind, key=lambda x: -x))
    return arr


#fix the deletions if it is under the error probability
def fix_dels(val_s1, val_s2, prob2del):
    prob_tresh=prob2del*1.5;
    i,j=-1,-1
    s1=''.join(val_s1.st)
    s2=''.join(val_s2.st)

    val1_new = val_s1.val
    val2_new = val_s2.val

    #calculate del1 and del 2 at the beggining
    letter_ind1_start = min(list(s1).index('0'),list(s1).index('1'))
    letter_ind2_start = min(list(s2).index('0'),list(s2).index('1'))
    overlap_ind_start = max(letter_ind1_start,letter_ind2_start)

    reverse1=list(s1); reverse1.reverse()
    reverse2=list(s2); reverse2.reverse()
    letter_ind1_end = max(len(reverse1)- 1 - reverse1.index('1'),len(reverse1)- 1 - reverse1.index('0'))
    letter_ind2_end = max(len(reverse2)- 1 - reverse2.index('1'),len(reverse2)- 1 - reverse2.index('0'))
    overlap_ind_end = min(letter_ind1_end,letter_ind2_end)

    del1= s1[overlap_ind_start:overlap_ind_end+1].count('-')
    del2= s2[overlap_ind_start:overlap_ind_end+1].count('-')


    while i < len(s1)-1 and j< len(s2)-1 and del1 < math.ceil(prob_tresh*len(s1)) and del2 < math.ceil(prob_tresh*len(s2)):
        j+=1; i+=1
        if s1[i]!=s2[j] and s1[i] != '-' and s2[j] != '-':
            tmp1 = s1[0:i] + '-' + s1[i:]
            tmp2 = s2[0:j] + '-' + s2[j:]
            e1 = caunt_error_val(tmp1[max(i-4,0):min(i+3,len(s1))] , s2[max(j-4,0):min(j+3,len(s2))])
            e2 = caunt_error_val(tmp2[max(j-4,0):min(j+3,len(s2))] , s1[max(i-4,0):min(i+3,len(s1))])
            e1_8 = caunt_error_val(tmp1[max(i - 4, 0):min(i + 8, len(s1))] , s2[max(j-4,0):min(j + 8, len(s2))])
            e2_8 = caunt_error_val(tmp2[max(j - 4, 0):min(j + 8, len(s2))] , s1[max(i-4,0):min(i + 8, len(s1))])
            if (e1 ==0 and e2>0) or (e2==e1 and e1==0 and e1_8<e2_8):#del in 1
                del1+=1
                s1=tmp1
                val1_new=np.insert(val1_new,i,0)
            elif (e2 ==0 and e1>0) or (e2==e1 and e1==0 and e1_8>e2_8):#del in 2
                s2=tmp2
                del2+=1
                val2_new=np.insert(val2_new, j, 0)
    errors_min = caunt_error_val(s1, s2)

    # if del1 > math.ceil(prob_tresh*len(s1)) or del2 > math.ceil(prob_tresh*len(s2)) or errors_min > 2:#math.ceil(prob2del*len(s2)):
    if del1 > math.ceil(len(s1)) or del2 > math.ceil(len(s2)) or errors_min > 2*prob2del:#math.ceil(prob2del*len(s2)):
        return [], -1
    else:
        strv1_new=ValStr(s1,val1_new)
        strv2_new=ValStr(s2,val2_new)
        res=merger_over_del_only(strv1_new, strv2_new)
        return res, errors_min + del1+del2

#check if s_val1 is  in s_val2
def is_substring_over_del(val_s1,val_s2,prob2del):
    for i in range(len(val_s2.st)-len(val_s1.st)+1):
        tmp=ValStr(val_s2.st[i:], val_s2.val[i:])
        res, ans_np = fix_dels(val_s1, tmp, prob2del)
        if ans_np!=-1:
            return res, 1
    return [],-1

# return true only if sub is a substing og st EXACTLY
def is_substring(sub, st):
    ind= st.find(sub)
    return (ind>=0), ind

#count errors between s1, s2
def caunt_error_val(s1,s2):
    return sum(1 for s, r in zip(s1,s2) if (s != r and s!='-' and r!='-'))


def my_cat_2string(first_vs,second_vs,prob2del):
    min_err_ind=-1
    len1, len2=len(first_vs.st), len(second_vs.st)
    minOverlap_bits = int(math.floor(0.25*min(len1,len2)))
    min_count_err = max(len1,len2)

    for i in range(len1-minOverlap_bits):
        res_t, tmp=(fix_dels(first_vs.cut_from(i), second_vs.cut_until(min(len1-i,len2)),prob2del))
        if tmp<math.ceil(2*prob2del*min(len(first_vs.st)-i,len(second_vs.st)))and tmp<min_count_err and tmp!=-1:
            min_err_ind, min_count_err=i, tmp
            res=res_t

    if min_err_ind==-1:
        return [], -1
    res=((first_vs.cut_until(min_err_ind)).cat(res.st, res.val))
    print "ind "+ str(min_err_ind)
    if len1-min_err_ind < len2:
        p=second_vs.cut_from(len1-min_err_ind)
        res = res.cat(p.st, p.val)

    return res,min_count_err

def my_merge(arr,prob2del):
    if len(arr) == 0: return []
    res = arr[0];
    other = arr[1:]
    booli = True
    all_final = []
    count=0
    print "---------line " + str(count) + "----------------"
    while len(other) > 0:
        if not booli:  # cant append anything to res
            all_final.append(res)
            res = other[0]
            if len(other) == 1: other = []
            else: other = other[1:]
            count += 1
            print "---------line " + str(count) + "----------------"
        booli = False

        for i in range(len(other)):  # try to append substring to res
            res1, error1 = my_cat_2string(res, other[i], prob2del*1.2)
            res2, error2 = my_cat_2string(other[i], res, prob2del*1.2)
            if error1 != -1 or error2 !=-1:
                print "i: " +str(i)
                if (error1 < error2 and error1!=-1) or error2==-1: res = res1
                elif (error2 < error1 and error2 !=-1) or error1==-1: res = res2

                if len(other) == 1: other = []
                else: other = other[0:i] + other[i + 1:]

                booli = True
                break
    all_final.append(res)
    return all_final

def check ():
    x=1
    