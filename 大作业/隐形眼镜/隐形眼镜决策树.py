# -*- coding: UTF-8 -*-
import pandas as pd
from sklearn import tree
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt

if __name__ == '__main__':
    # ================= 1. 数据读取与处理=================
    with open('lenses.txt', 'r') as fr:
        lenses = [inst.strip().split('\t') for inst in fr.readlines()]

    lenses_target = [each[-1] for each in lenses]
    lensesLabels = ['age', 'prescript', 'astigmatic', 'tearRate']

    lenses_list = [dict(zip(lensesLabels, each)) for each in lenses]
    lenses_temp = pd.DataFrame(lenses_list)

    # 实例化 LabelEncoder，将字符串转换为数字
    le = LabelEncoder()
    lenses_encoded = lenses_temp.copy()

    for col in lenses_temp.columns:
        lenses_encoded[col] = le.fit_transform(lenses_temp[col])

    # 转换目标变量
    lenses_target_encoded = le.fit_transform(lenses_target)

    # ================= 2. 训练模型 =================
    # 使用 C4.5 算法 (criterion='entropy')
    clf = tree.DecisionTreeClassifier(criterion='entropy')
    clf = clf.fit(lenses_encoded.values, lenses_target_encoded)

    # ================= 3. 画出决策树（可视化） =================
    plt.figure(figsize=(12, 8))
    tree.plot_tree(clf,
                   feature_names=lensesLabels,
                   class_names=le.classes_, # 显示分类名称
                   filled=True,
                   rounded=True)
    plt.title("Lenses Decision Tree")
    plt.show()

    # =================  输入数据并预测结果=================
    print("\n--- 隐形眼镜预测系统 ---")
    print("请根据以下提示输入您的情况：")

    # 定义一个函数来获取用户输入并转换
    def get_input_and_predict(feature_name, encoder):
        print(f"\n可选的 {feature_name} 包括: {list(encoder.classes_)}")
        val = input(f"请输入您的 {feature_name}: ")
        # 检查输入是否合法
        if val not in encoder.classes_:
            print(f"错误：输入无效。请从 {list(encoder.classes_)} 中选择。")
            return None

        # 转换输入为数字
        val_encoded = encoder.transform([val])[0]
        return val_encoded

    # 循环进行预测，直到用户选择退出
    while True:
        input_data = []
        valid_input = True

        # 依次获取 4 个特征的输入
        for col in lensesLabels:
            # 注意：我们需要为每一列单独创建一个 LabelEncoder 来确保映射一致
            # 或者更简单的做法：利用之前训练好的逻辑
            # 这里为了代码简单，我们重新 fit 一下每一列的 encoder
            col_le = LabelEncoder()
            col_le.fit(lenses_temp[col])

            val = get_input_and_predict(col, col_le)
            if val is None:
                valid_input = False
                break
            input_data.append(val)

        if not valid_input:
            continue

        # 将输入转换为 numpy 数组并预测
        prediction_encoded = clf.predict([input_data])
        prediction_label = le.inverse_transform(prediction_encoded)

        print("-" * 30)
        print(f"预测结果：您适合佩戴 -> 【 {prediction_label[0]} 】")
        print("-" * 30)

        # 询问是否继续
        again = input("\n是否继续预测？(输入 n 退出，回车继续): ")
        if again.lower() == 'n':
            print("程序结束。")
            break