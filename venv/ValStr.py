import numpy as np

class ValStr:
    def __init__(self, st, val):
        self.st = st
        if len(val)>1: self.val = val
        else: self.val = np.ones(len(st))
        # else: self.val = val

    def cat(self,cat_st,cat_val):
        self.st=self.st+cat_st
        self.val=np.concatenate((self.val,cat_val))

    def edit_val_ind(self,ind,value):
        self.val[ind]=value

    def set_st(self,st_new):
        self.st=st_new

    def set_val(self,val_new):
        self.val=val_new

    def add2val(self,vec_val):
        self.val=self.val+vec_val

    def insert_val(self,ind, val):
        self.val=np.insert(self.val, ind, val, axis=None)


# p1 = Person("John", 36)
# p1.myfunc()