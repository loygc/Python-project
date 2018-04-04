_author_ = "susmote"

import time
def timer(func):
    def deco(*args,**kwargs):
        start_time = time.time()
        func(*args,**kwargs)
        end_time = time.time()
        print("The func run time is %s" %(end_time - start_time))
    return deco

def test1():
    time.sleep(1)
    print("run in the test1")

def test2(name ,age):
    print("test2:",name,age)


test1()
test2("susmote",8)


