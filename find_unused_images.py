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