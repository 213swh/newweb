from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime
import re  # 添加这行导入正则表达式模块
from werkzeug.utils import secure_filename  # 新增导入

app = Flask(__name__)
CORS(app)  # 添加这行启用CORS

# 简单登录校验 (实际项目需使用session和密码哈希)
ADMIN_PASSWORD = 'your_secure_password'

# 处理模板的函数
def process_template(template):
    # 获取当前日期
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    # 使用正则表达式替换发布时间后的日期
    pattern = r'<span><i class="fa fa-calendar"></i>发布时间: \d{4}-\d{2}-\d{2}</span>'
    replacement = f'<span><i class="fa fa-calendar"></i>发布时间: {current_date}</span>'
    new_content = re.sub(pattern, replacement, template)
    
    return new_content

# 新增：文件上传配置
UPLOAD_FOLDER = os.path.join(app.root_path, 'images')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 限制16MB

# 新增：检查文件类型函数
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/publish-news', methods=['POST'])
def publish_news():
    try:
        # 添加调试日志
        print("收到发布新闻请求")
        
        # 获取表单数据
        title = request.form.get('title')
        category = request.form.get('category')
        content = request.form.get('content')
        # 强制使用当前日期
        formatted_date = datetime.now().strftime('%Y-%m-%d')

        # 移除原有的日期处理逻辑
        # 处理日期格式 - 确保为yyyy-MM-dd
        # publish_date = request.form.get('publish-date')
        # 标准化日期格式
        # if publish_date:
        #     # 移除可能的时间部分
        #     if 'T' in publish_date:
        #         publish_date = publish_date.split('T')[0]
        #     # 验证日期格式
        #     try:
        #         # 解析并重新格式化以确保正确性
        #         date_obj = datetime.strptime(publish_date, '%Y-%m-%d')
        #         formatted_date = date_obj.strftime('%Y-%m-%d')
        #     except ValueError:
        #         # 格式错误时使用当前日期
        #         formatted_date = datetime.now().strftime('%Y-%m-%d')
        # else:
        #     # 未提供日期时使用当前日期
        #     formatted_date = datetime.now().strftime('%Y-%m-%d')
        
        # 验证必要参数
        if not title or not content:
            return jsonify({'success': False, 'error': '标题和内容不能为空'})
        
        # 生成唯一新闻ID
        news_id = f"news_{int(datetime.now().timestamp())}"
        news_filename = f"news-detail-{news_id}.html"
        
        # 读取模板文件 - 使用绝对路径
        template_path = os.path.join(app.root_path, 'news-detail-industry4.html')
        try: 
            with open(template_path, 'r', encoding='utf-8') as f: 
                template = f.read() 
            print('模板文件读取成功') 
            # 调用process_template函数处理日期替换
            new_content = process_template(template)  # <-- 添加这行
        except Exception as e: 
            print(f'读取模板文件失败: {str(e)}') 
            return jsonify({'success': False, 'error': f'读取模板失败: {str(e)}'}) 

        # 替换模板内容 
        # 1. 替换所有标题相关内容 
        new_content = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', new_content)  
        new_content = re.sub(r'<h1>.*?</h1>', f'<h1>{title}</h1>', new_content)  # 替换主标题
        # 2. 替换描述meta标签
        # 修复日期替换 - 使用更通用的选择器
        # 删除原有的提取日期部分代码
        # publish_date_only = publish_date.split('T')[0] if 'T' in publish_date else publish_date
        # 直接使用 formatted_date 进行替换
        new_content = re.sub(r'<span class="news-date">.*?</span>', f'<span class="news-date">{formatted_date}</span>', new_content)

        # 添加keywords自定义支持
        keywords = request.form.get('keywords', '').strip()
        if not keywords:
            keywords = f'{title},{category}'  # 使用标题和分类作为默认关键词
        # 使用正则表达式替换整个keywords meta标签
        new_content = re.sub(r'<meta name="keywords" content=".*?">', f'<meta name="keywords" content="{keywords}">', new_content)
        new_content = new_content.replace('<h1>芦笋汁</h1>', f'<h1>{title}</h1>')
        # 使用正则表达式替换所有日期
        new_content = re.sub(r'<span class="news-date">.*?</span>', f'<span class="news-date">{formatted_date}</span>', new_content)
        # 删除此行重复替换代码
        # new_content = new_content.replace('<span class="news-date">2024-05-18</span>', f'<span class="news-date">{publish_date}</span>')
        
        # 完全替换新闻内容区域（清除模板默认内容）
        # 使用正则表达式匹配整个内容区域并替换
        # 添加HTML格式处理：将换行符转换为<br>标签，段落用<p>包裹
        formatted_content = content.replace('\n\n', '</p><p>').replace('\n', '<br>')
        formatted_content = f'<p>{formatted_content}</p>'
        new_content = re.sub(r'<div class="news-content">.*?</div>', f'<div class="news-content">{formatted_content}</div>', new_content, flags=re.DOTALL)
        
        # 保存新新闻页面
        news_path = os.path.join(app.root_path, news_filename)
        with open(news_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        # 更新新闻列表页面
        news_list_path = os.path.join(app.root_path, 'news.html')
        if not os.path.exists(news_list_path):
            return jsonify({'success': False, 'error': '新闻列表文件不存在'})
        
        with open(news_list_path, 'r', encoding='utf-8') as f:
            news_html = f.read()
        
        # 生成新闻列表项
        # 新增：处理图片上传
        news_image_url = 'images/default-news.jpg'  # 默认图片
        if 'news-image' in request.files:
            image = request.files['news-image']
            if image.filename != '' and allowed_file(image.filename):
                # 生成安全的文件名
                filename = secure_filename(image.filename)
                # 添加时间戳确保文件名唯一
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                filename = f'{timestamp}_{filename}'
                # 保存文件
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(image_path)
                # 更新图片URL
                news_image_url = f'images/{filename}'
        
        # 修改：生成带图片的新闻列表项
        news_item = f'''<div class="news-item" data-category="{category}">
    <div class="news-image">
        <img src="{news_image_url}" alt="{title}">
    </div>
    <div class="news-info">
        <span class="news-date">{formatted_date}</span>
        <h3>{title}</h3>
        <p>{content[:100]}...</p>
        <a href="{news_filename}" class="read-more">阅读更多</a>
    </div>
</div>'''
        
        # 检查插入点是否存在
        if '<!-- 新闻列表插入点 -->' not in news_html:
            return jsonify({'success': False, 'error': '新闻列表缺少插入标记'})
        
        # 插入到新闻列表中
        updated_news_html = news_html.replace('<!-- 新闻列表插入点 -->', f'{news_item}\n<!-- 新闻列表插入点 -->')
        
        with open(news_list_path, 'w', encoding='utf-8') as f:
            f.write(updated_news_html)
        
        return jsonify({
            'success': True,
            'newsUrl': news_filename
        })
    except Exception as e:
        # 捕获所有未处理的异常
        print(f"发布新闻失败: {str(e)}")
        return jsonify({'success': False, 'error': f'服务器内部错误: {str(e)}'})

# 启动服务器时指定端口（如果需要）
if __name__ == '__main__':
    app.run(port=5001, debug=True)
