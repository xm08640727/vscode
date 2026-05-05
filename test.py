import os
from PIL import Image, ImageDraw, ImageFont

# ================= 配置区 =================
# 1. 定义列的顺序（文件夹名称），注意把你自己的模型放在 GT 前面
columns = ['RGB', 'T', 'CSRNet', 'LSNET', 'MIDD', 'OSRNet', 'ECFFNet', 'SwinNet', 'OURS', 'GT']

# 2. 定义你想展示的图片文件名（按照你希望在图中从上到下显示的顺序）
# 确保这些文件在上述每个文件夹中都存在且同名
image_filenames = [
    '030.png', 
    '031.png',
    '032.png',
    '033.png',
    '034.png',
    '035.png',
    '036.png',
    '037.png',
    '038.png'
    # ... 在这里填入你挑选的所有图片名
]

# 3. 设置排版参数
img_width = 256      # 每张小图统一缩放到的宽度
img_height = 192     # 每张小图统一缩放到的高度
padding = 4          # 图片之间的间距（黑色缝隙）
header_height = 80   # 顶部文字区域的高度
bg_color = (255, 255, 255)  # 背景颜色，通常学术论文用白色 (255,255,255)

# ================= 执行区 =================
# 计算整张大图的尺寸
total_width = len(columns) * img_width + (len(columns) - 1) * padding
total_height = header_height + len(image_filenames) * img_height + (len(image_filenames) - 1) * padding

# 创建空白画布
canvas = Image.new('RGB', (total_width, total_height), bg_color)
draw = ImageDraw.Draw(canvas)

# 尝试加载字体，如果找不到系统字体则使用默认字体
try:
    # Windows 11 下的 Arial 粗体路径，字号 48
    font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 48) 
except IOError:
    font = ImageFont.load_default()
    print("⚠️ 警告：找不到指定的 Windows 字体，使用了默认字体，文字可能非常小！")

# 绘制列标题（方法名）
for col_idx, col_name in enumerate(columns):
    # 计算文字的居中位置
    text_bbox = draw.textbbox((0, 0), col_name, font=font)
    text_w = text_bbox[2] - text_bbox[0]
    text_h = text_bbox[3] - text_bbox[1]
    
    x_text = col_idx * (img_width + padding) + (img_width - text_w) // 2
    y_text = (header_height - text_h) // 2
    draw.text((x_text, y_text), col_name, font=font, fill=(0, 0, 0))

# 循环读取并粘贴图片
for row_idx, filename in enumerate(image_filenames):
    for col_idx, col_name in enumerate(columns):
        img_path = os.path.join(col_name, filename)
        
        if not os.path.exists(img_path):
            print(f"警告: 找不到图片 {img_path}，将填充空白。")
            img = Image.new('RGB', (img_width, img_height), (200, 200, 200))
        else:
            img = Image.open(img_path).convert('RGB')
            # 统一缩放尺寸，防止原始输入大小不一导致错位
            img = img.resize((img_width, img_height), Image.Resampling.LANCZOS)
        
        # 计算粘贴坐标
        x = col_idx * (img_width + padding)
        y = header_height + row_idx * (img_height + padding)
        
        canvas.paste(img, (x, y))

# 保存最终的高清对比图
output_path = 'VT1000_result.jpg'
canvas.save(output_path, quality=100, dpi=(300, 300))
print(f"拼接完成！已保存至 {output_path}")