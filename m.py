a = 1234
count = 0


def tr():
    global count
    b = int(input())
    if b == a:
        print("b")
        tr()
    else:
        if count == 3:
            print("break")
            quit()
        count += 1
        print("e")
        tr()


if __name__ == '__main__':
    tr()
