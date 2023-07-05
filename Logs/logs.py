import os
from datetime import datetime


def println(e):

    print(e)
    f = open(os.path.join("Logs", "logs"), "a+")
    f.write(f"{datetime.now().strftime('[%Y-%m-%d] %H:%M:%S')} - {e}\n")
    f.close()