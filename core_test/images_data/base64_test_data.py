import base64
import os
from typing import List

def get_base64_strings() -> List[str]:
    path = "core_test/images_data/images"
    images = [f for f in os.listdir(path)]
    base64_strings = []
    for image in images:
        with open(path+'/'+image, "rb") as image_file:
            base64_string = base64.b64encode(image_file.read()).decode("utf-8")
            base64_strings.append(base64_string)
    return base64_strings