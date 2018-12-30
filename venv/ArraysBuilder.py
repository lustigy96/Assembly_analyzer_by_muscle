import DEFINES
import random
import MuscleRunner

#this function sample random index and put string[ind:ind+const] in arr
def randomSample_constLen(string, parts=0, constlen=0):
    arr=[]; strlen=len(string);
    constlen=int(constlen*strlen)/2;
    for x in range(parts):
        ind=random.randint(0,strlen-1)
        tmp=string[max(ind-constlen,0):ind] + string[ind:min(ind+constlen,strlen-1)]
        arr.append(tmp)
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

