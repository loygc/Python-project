__author__ = "susmote"

class Cat():
    def __init__(self):
        print("类被初始化")
    def __del__(self):
        print("类被释放")

dog = Cat()
cat = Cat()
del dog
print("**"*30)
del cat
print("hello world")