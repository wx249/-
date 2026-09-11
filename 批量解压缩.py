import os
import sys
import zipfile


def extract_single_zip(zip_path, target_dir):
    """
    解压单个ZIP文件到指定目录，处理中文乱码。
    返回 (成功数量, 失败数量)
    """
    success_count = 0
    fail_count = 0

    # 计算该ZIP对应的子文件夹名
    zip_name = os.path.basename(zip_path)
    folder_name = os.path.splitext(zip_name)[0]
    final_target_dir = os.path.join(target_dir, folder_name)

    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for info in zip_ref.infolist():
                original_filename = info.filename

                # --- 核心：处理中文乱码 ---
                try:
                    raw_bytes = original_filename.encode('cp437')
                    try:
                        decoded_name = raw_bytes.decode('utf-8')
                    except UnicodeDecodeError:
                        try:
                            decoded_name = raw_bytes.decode('gbk')
                        except UnicodeDecodeError:
                            decoded_name = original_filename
                except UnicodeEncodeError:
                    decoded_name = original_filename

                info.filename = decoded_name

                try:
                    zip_ref.extract(info, final_target_dir)
                    success_count += 1
                except Exception as e:
                    print(f"⚠️ 警告: 解压 [{zip_name}] 中的文件失败: {e}")
                    fail_count += 1
    except Exception as e:
        print(f"❌ 错误: 无法打开或解压 {zip_name}: {e}")
        return 0, 1

    return success_count, fail_count


def batch_extract_folder(folder_path):
    """
    遍历文件夹，批量解压所有ZIP文件。
    """
    if not os.path.exists(folder_path):
        print(f"❌ 错误: 文件夹不存在 - {folder_path}")
        return

    if not os.path.isdir(folder_path):
        print(f"❌ 错误: 路径不是一个文件夹 - {folder_path}")
        return

    # 获取所有 .zip 文件
    zip_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.zip')]

    if not zip_files:
        print("ℹ️ 提示: 该文件夹下没有找到任何 .zip 文件。")
        return

    print(f"🔍 找到 {len(zip_files)} 个 ZIP 文件，开始批量处理...")
    print("-" * 40)

    total_success = 0
    total_fail = 0

    for zip_file in zip_files:
        zip_path = os.path.join(folder_path, zip_file)
        print(f"⏳ 正在处理: {zip_file} ...")

        s, f = extract_single_zip(zip_path, folder_path)
        total_success += s
        total_fail += f

        if f == 0:
            print(f"   ✅ 完成: {zip_file}")
        else:
            print(f"   ⚠️ 部分失败: {zip_file}")

    print("-" * 40)
    print(f"🎉 全部处理完毕！")
    print(f"   总成功文件数: {total_success}")
    print(f"   总失败文件数: {total_fail}")


if __name__ == '__main__':
    # 支持命令行传参，或在交互模式下手动输入
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = input("请输入包含ZIP文件的文件夹路径 (或直接拖拽文件夹到窗口): ").strip().strip('"')

    if path:
        batch_extract_folder(path)
    else:
        print("⚠️ 未提供路径，程序退出。")

    # 防止命令行窗口直接闪退
    if len(sys.argv) == 1:
        input("\n按回车键退出...")