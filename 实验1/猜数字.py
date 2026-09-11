import random
def guess_number():
    number = random.randint(1, 100)
    attempts = 7
    print("欢迎来到猜数字游戏！")
    print("我已经想了一个1到100之间的数字，你有7次机会来猜。")
    for attempt in range(1, attempts + 1):
        try:
            guess = int(input(f"\n第{attempt}次尝试，请输入你的猜测: "))
        except ValueError:
            print("请输入一个有效的整数！")
            continue
        if guess < number:
            print("太小了！")
        elif guess > number:
            print("太大了！")
        else:
            print(f"恭喜你！你在第{attempt}次猜对了！")
            break
    else:
        print(f"\n很遗憾，你没有猜对。正确答案是: {number}")
guess_number()
import random
def guess_number():
    number = random.randint(1, 100)
    attempts = 7
    print("欢迎来到猜数字游戏！")
    print("我已经想了一个1到100之间的数字，你有7次机会来猜。")
    for attempt in range(1, attempts + 1):
        try:
            guess = int(input(f"\n第{attempt}次尝试，请输入你的猜测: "))
        except ValueError:
            print("请输入一个有效的整数！")
            continue
        if guess < number:
            print("太小了！")
        elif guess > number:
            print("太大了！")
        else:
            print(f"恭喜你！你在第{attempt}次猜对了！")
            break
    else:
        print(f"\n很遗憾，你没有猜对。正确答案是: {number}")
guess_number()
