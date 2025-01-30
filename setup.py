# it helps us to serve our project as a package
from setuptools import find_packages,setup
# 1️⃣ setuptools → Python की एक लाइब्रेरी है, जो Python पैकेज बनाने और इंस्टॉल करने में मदद करती है।
# 2️⃣ find_packages() → यह अपने आप प्रोजेक्ट में मौजूद सारे पैकेज (folders जिनमें __init__.py हो) को ढूंढता है।
# 3️⃣ setup() → यह Python पैकेज की जानकारी सेट करता है (जैसे पैकेज का नाम, वर्ज़न, ज़रूरी लाइब्रेरी आदि)।
from typing import List
# Python में List को वैसे ही इस्तेमाल कर सकते हैं, लेकिन टाइप हिंटिंग (Type Hinting) को आसान बनाने के लिए हम typing लाइब्रेरी से List इम्पोर्ट करते हैं।
# 🔹 बिना टाइप हिंटिंग (Normal Python List ie without typing list)
# def add_numbers(numbers):
#     return sum(numbers)
# यह काम करेगा, लेकिन इसमें यह नहीं बताया गया कि numbers में Integer होंगे या कुछ और।

#  typing.List के साथ (Type Hinting वाला Python List)
# from typing import List

# def add_numbers(numbers: List[int]) -> int:
#     return sum(numbers)
#  अब यह साफ है कि numbers की लिस्ट में सिर्फ Integer होंगे और फंक्शन Integer ही लौटाएगा।
def requirements_yaha_se(file_path:str)->List[str]:
    requirements=[]
    with open(file_path) as file_obj:
# open(file_path) → यह file_path नाम की फ़ाइल को ओपन (खोलता) करता है।
# as file_obj → इस फ़ाइल को file_obj नाम की वेरिएबल में स्टोर करता है ताकि हम इसे आसानी से इस्तेमाल कर सकें।
# with का उपयोग → यह फ़ाइल को ऑटोमेटिकली बंद कर देता है जब उसका काम पूरा हो जाता है, इसलिए file.close() लिखने की जरूरत नहीं होती।
        requirements=file_obj.readlines()
        requirements=[req.replace("\n","") for req in requirements]
    return requirements

setup(
    name="fault_detection",
    version="0.0.1", # version kuch bhi de do
    author="Vibhanshu",
    author_mail='vibhanshugupta875@gmail.com',
    install_requirements=requirements_yaha_se("requirements.txt"),# humne saari requirement pehle hi requirements file mein likh li thi
    packages=find_packages()
)