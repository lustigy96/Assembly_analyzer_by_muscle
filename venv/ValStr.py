import numpy as np

class ValStr:
    def __init__(self, st, val):
        self.st = st
        if val==0: self.val = np.ones(len(st))
        else: self.val = val


    def add(self,add_st,add_val):
        self.st=self.st+add_st
        self.val=np.concatenate((self.val,add_val))

    def edit_val(self,ind,value):
        self.val[ind]=value
#     def myfunc(abc):
#         print("Hello my name is " + abc.name)
#
# p1 = Person("John", 36)
# p1.myfunc()