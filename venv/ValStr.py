class ValStr:
    def __init__(self, st, val):
        self.str = st
        if val==0: self.val = ones(len(st))
        else: self.val = val


    def add(self,add_st,add_val):
        self.st=self.st+add_st
        self.val=self.val.append(add_val)

#     def myfunc(abc):
#         print("Hello my name is " + abc.name)
#
# p1 = Person("John", 36)
# p1.myfunc()