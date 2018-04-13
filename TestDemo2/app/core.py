__author__ = "susmote"

for i in range(2, 10):
    for n in range(2, i):
        if i % n == 0:
            print(i, "不是一个质数")
            break
    else:
        print(i, "是一个质数")