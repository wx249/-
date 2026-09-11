def calculator():
    print("简易计算器")
    print("支持的操作: +, -, *, /")

    while True:
        try:
            num1 = float(input("请输入第一个数字: "))
            operator = input("请输入运算符 (+, -, *, /): ")
            num2 = float(input("请输入第二个数字: "))

            if operator == '+':
                result = num1 + num2
            elif operator == '-':
                result = num1 - num2
            elif operator == '*':
                result = num1 * num2
            elif operator == '/':
                if num2 == 0:
                    print("错误：除数不能为零！")
                    continue
                result = num1 / num2
            else:
                print("不支持的运算符！")
                continue
            print(f"结果: {num1} {operator} {num2} = {result}")
        except ValueError:
            print("请输入有效的数字！")
        again = input("\n是否继续计算？(y/n): ").lower()
        if again != 'y':
            print("感谢使用计算器！")
            break


calculator()