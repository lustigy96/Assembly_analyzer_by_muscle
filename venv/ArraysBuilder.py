import DEFINES
import random


#this function sample random index and put string[ind:ind+const] in arr
def randomSample_constLen(string, parts=0, constlen=0):
    arr=[]; strlen=len(string);
    constlen=int(constlen*strlen)
    for x in range(parts):
        ind=random.randint(0,strlen-1)
        arr.append(string[ind:min(ind+constlen,strlen-1)])
    return arr




#make flips on 2-dim array with probability=probToFlip
def flipsOnArr(arr,probToFlip):
    arr=list(arr)
    for x in range(len(arr)):
        for i in range(len(arr[x])):
            r=random.uniform(0,1);
            if r<probToFlip:
                if arr[x][i] == '1':
                    arr[x] = arr[x][:i] + '0' + arr[x][i + 1:]
                else:
                    arr[x] = arr[x][:i] + '1' + arr[x][i + 1:]
    # arr = ''.join(arr)
    return arr;

#make flips on 2-dim array with probability=probToFlip (ONLY ON ZEROS)
def flipsOnArr_zeros(arr,probToFlip):
    arr=list(arr)
    for x in range(len(arr)):
        for i in range(len(arr[x])):
            if arr[x][i]=='0':
                r=random.uniform(0,1);
                if r<probToFlip:
                    arr[x] = arr[x][:i] + '1' + arr[x][i + 1:]
    # arr = ''.join(arr)
    return arr;


#merge the strings comes out of muscle rightly,
# return the result if the overlap is good enough, otherwise: return -1
def mergeOverlapStrings(s1,s2):
    result=[];
    count1,count2,overlap=0,0,0 #counts the strings real letters (no -) and the overlap
    badspace1, badspace2=0,0
    for x1,x2 in zip(s1,s2):
        if (x1!='-'): count1+=1
        if(x2!='-'): count2+=1
        
        if x1==x2:
            result.append(x1)
            if x1!='-':overlap+=1
            
        elif x1=='-' and x2!='-':
            result.append(x2)
            if overlap > 1: badspace1 += 1
            
        elif x2=='-' and x1!='-':
            result.append(x1)
            if overlap > 1: badspace2 += 1
            
        else: #there is a flip, and decision should be done #the assumption is that 0 becomes 1
            result.append('0') 
    if max(0.1*badspace1/count1, 0.1*badspace2/count2)>DEFINES.BAD_SPACE_TRESH:
        return -1
    if(1.0*overlap)/min(count1,count2) >=DEFINES.OVERLAP_TRESHOLD:
        result=''.join(result)
    else: result=-1
    return result
