# logging is important for tracking the events that happen when applicaton runs
import logging
import os
# Python ka os module operating system ke sath interact karne ke liye use hota hai. Is code mein os module mainly file paths aur directories handle karne ke liye use ho raha hai.
from datetime import datetime
LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
# Yeh ek dynamic log file ka naam banata hai, jo current date aur time ke basis pe change hota rahega.
# Har baar jab tum script run karoge, ek naya log file generate hoga, jo overwrite nahi hoga.
logs_path=os.path.join(os.getcwd(),"logs")
# is line mein humne current working directry ie mera pehla project mein loga naam ke folder ka path logs_path
# mein store kar diya, abhi sirf bana hai logs naam ka folder nhi bana
os.makedirs(logs_path,exist_ok=True)
# Yeh line logs folder create karne ka kaam karti hai agar woh exist nahi karta. Agar pehle se exist karta hai, toh koi bhi issue nahi hoga.
# logs_path ek variable hai jo ki logs folder ka path rakhta hai
LOG_FILE_PATH=os.path.join(logs_path,LOG_FILE)
# isme humne logs-path folder mein log_file ko store kar diya
logging.basicConfig(
filename=LOG_FILE_PATH,
format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s-%(message)s",
level=logging.INFO
)
