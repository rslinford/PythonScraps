import random


def binary_search(n, number_list):
    length = len(number_list)
    a = 0
    b = length
    while a != b:
        index = ((b - a) // 2) + a
        if number_list[index] == n:
            return True
        elif n < number_list[index]:
            if b == index:
                break
            b = index
        else:
            if a == index:
                break
            a = index
    return False


order_list_size = 500
random_list = []
for i in range(order_list_size):
    random_list.append(random.randint(0, 1000))
random_list.sort()
while True:
    print(random_list)
    target = int(input("Number to search for? "))
    if binary_search(target, random_list):
        print("found!")
    else:
        print("not found.")
