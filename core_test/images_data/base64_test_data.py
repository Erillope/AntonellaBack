import base64
import os
import random

def get_base64_string() -> str:
    path = "core_test/images_data/images"
    image = random.choice(os.listdir(path))
    with open(path+'/'+image, "rb") as image_file:
        base64_string = base64.b64encode(image_file.read()).decode("utf-8")
        return base64_string