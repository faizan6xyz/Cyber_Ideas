import base64
import os
import random 
import string
def image_to_base64(name, folder_path="Data"):
    file_path = os.path.join(folder_path, name)
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found")
        return None
    try:
        with open(file_path, "rb") as f:
            image_b64 = base64.b64encode(f.read()).decode("utf-8")
        return image_b64
    except Exception as e:
        print(f"Error converting {name} to base64: {str(e)}")
        return None

def base64_to_image(base64_string, output_path="output/output_image.png"):
    try:
        if "," in base64_string:
            base64_string = base64_string.split(",")[1]
        image_data = base64.b64decode(base64_string)
        with open(output_path, "wb") as f:
            f.write(image_data)
        print(f" Image saved successfully to: {output_path}")
    except Exception as e:
        print(f" Error unable to covnert : {e}")

steps_for_noise = []
text_for_the_noise = []

def add_noise(text):
    text_list = list(text)
    text_L = len(text_list)
    base64_chars = string.ascii_letters + string.digits + '+/'
    x_new = 0
    if text_L == 0 :
        print("string is empty")
        return ""
    for i in range(0, text_L, 100): # start , stop , step
        x = random.randint(1, 100)     
        xx = x + x_new
        if xx >= text_L:  
            continue 
        steps_for_noise.append(xx)
        x1 = random.choice(base64_chars)
        text_for_the_noise.append(text_list[xx])
        text_list[xx] = x1
        x_new += 100
    text1 = ''.join(text_list)
    return text1

def remove_noise(text):
    text_list = list(text)
    text_L = len(text_list)
    len_step = len(steps_for_noise)
    if text_L == 0 :
        print("string is empty")
        return ""
    for i in range(0,len_step,1):
        text_list[steps_for_noise[i]] = text_for_the_noise[i]
    text1 = ''.join(text_list)
    return text1

def pipeline(image):
    b64 = image_to_base64(image)
    if b64 is None:
        return
    noised = add_noise(b64)
    restored = remove_noise(noised)
    base64_to_image(restored)
    
pipeline("h.png")