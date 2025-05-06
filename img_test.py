from PIL import Image, ImageOps

def pad_and_resize(image: Image.Image, final_size=(640, 640), min_base=320, fill_color=(255, 255, 255)):
    # 原始尺寸
    w, h = image.size
    max_dim = max(w, h, min_base)

    # 計算 padding
    delta_w = max_dim - w
    delta_h = max_dim - h
    padding = (delta_w // 2, delta_h // 2, delta_w - delta_w // 2, delta_h - delta_h // 2)

    # 使用 ImageOps 擴充邊框
    padded_image = ImageOps.expand(image, border=padding, fill=fill_color)

    # Resize 到指定尺寸
    resized_image = padded_image.resize(final_size)

    return resized_image

img = Image.open(r"C:\Users\user\Desktop\螢幕截圖\螢幕擷取畫面 2025-04-24 203704.png")
result = pad_and_resize(img)
result.show()  # 或 result.save("output.jpg")