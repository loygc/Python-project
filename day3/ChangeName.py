_author_ = "susmote"

f = open("name","r",encoding="utf-8")
f_new = open("name_update","w",encoding="utf-8")


for line in f:
    if  "lisite" in line:
        line = line.replace("lisite","susmote")
    f_new.write(line)
f.close()
f_new.close()