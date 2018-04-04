_Author_= "Susmote"

product_list = [
    ('Iphone',5800),
    ('Mac Pro',9800),
    ('Bike',800),
    ('Watch',10600),
    ('Coffee',31),
    ('Alex Python',120)
]
shopping_list = []
salary = input("Input your salary:")
if salary.isdigit():
    salary = int(salary)
    while True:
        for index,item in enumerate(product_list):
            print(index,item)
        user_choice = input("选择要买吗？>>>:")
        if user_choice.isdigit():
            user_choice = int(user_choice)
            if user_choice < len(product_list) and user_choice >= 0:
                p_item = product_list[user_choice]
                if  p_item[1] <= salary:
                    shopping_list.append(p_item)
                    salary -= p_item[1]
                    print("Added %s into shopping cart,your current balance is \033[31;1m%s\033[0m"%(p_item,salary))
                else:
                    print("\033[41;1m你的余额只剩[%s]啦，还买个毛线\033[0m" %salary)
            else:
                print("None this option")
        elif user_choice == "q":
            print("---------Shopping List----------")
            for p in shopping_list:
                print(p)
            print("Your current balance: ",salary)
            exit()

        else:
            print("invalid option")