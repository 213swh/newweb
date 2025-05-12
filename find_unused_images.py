import os

# 获取 images 目录下所有图片文件名
img_dir = './images'
img_files = set(os.listdir(img_dir))

# 需要检查的文件类型
check_exts = ('.html', '.css', '.js')

# 收集所有代码文件内容
all_text = ''
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith(check_exts):
            with open(os.path.join(root, file), 'r', encoding='utf-8', errors='ignore') as f:
                all_text += f.read()

# 检查哪些图片未被引用，并删除
unused = []
for img in img_files:
    if img not in all_text:
        unused.append(img)
        try:
            os.remove(os.path.join(img_dir, img))
            print(f"已删除未被引用的图片: {img}")
        except Exception as e:
            print(f"删除 {img} 时出错: {e}")

print('未被引用的图片已全部删除。')

def get_image_sizes(directory):
    """
    获取指定目录下所有图片的大小并打印。

    :param directory: 图片所在的目录路径
    """
    print(f"\n--- {directory} 目录下图片大小 ---")
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path): # 确保是文件而不是子目录
            try:
                size_bytes = os.path.getsize(item_path)
                size_kb = size_bytes / 1024
                size_mb = size_kb / 1024
                if size_mb >= 1:
                    print(f"{item}: {size_mb:.2f} MB")
                elif size_kb >= 1:
                    print(f"{item}: {size_kb:.2f} KB")
                else:
                    print(f"{item}: {size_bytes} Bytes")
            except OSError as e:
                print(f"无法获取 {item} 的大小: {e}")

if __name__ == "__main__":
    # 例如，可以先执行删除未使用图片的操作，然后再显示图片大小

    # 调用新添加的方法来显示图片大小
    image_directory = './images'
    get_image_sizes(image_directory)