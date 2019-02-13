import numpy as np

class ValStr:
    def __init__(self, st, val): #create an str_val. if val is [], then val is otomated to be ones-array
        self.st = st
        if len(val)>1: self.val = val
        else: self.val = np.ones(len(st))
        # else: self.val = val

    def cat(self,cat_st,cat_val):#cat the st and val to 'self' and return self
        self.st=self.st+cat_st
        self.val=np.concatenate((self.val,cat_val))
        return self

    def edit_val_ind(self,ind,value):#edit value in specific index
        self.val[ind]=value

    def set_st(self,st_new):
        self.st=st_new

    def set_val(self,val_new):
        self.val=val_new

    def add2val(self,vec_val): #vector addition, (arr[i]=arr1[i]+arr2[i] for all i)
        self.val=self.val+vec_val

    def insert_val(self,ind, val): #insert value to the val array
        self.val=np.insert(self.val, ind, val, axis=None)

    def cut_from(self,start):#return new valStr (doesnt change SELF), from index 'start' to the end of self
        v_new=self.val[start:]
        s_new=self.st[start:]
        return ValStr(s_new,v_new)

    def cut_until(self,end):#return new valStr (doesnt change SELF), from index 0 to the index 'end'  of self
        v_new = self.val[:end]
        s_new = self.st[:end]
        return ValStr(s_new, v_new)

    def cut_from_until(self, start,end):#return new valStr (doesnt change SELF), from index 'start' to the index 'end' of self
        v_new=self.val[start,end]
        s_new=self.st[start,end]
        return ValStr(s_new,v_new)
