import logging
from rich import print
import threading
logger = logging.getLogger(__name__)

logging.basicConfig(filename='app1.log',level=logging.INFO)
def log(text):
    #threading.Thread(target=logging.info,args=(text))
    logger.info(text)
def log1(text):
    #print(f"[italic red][LOG][/italic red] {text}!")
    log(text)
def log2(text):
    #print(f"[italic green][INFO][/italic green] {text}!")
    log(text)

def log3(text):
   # print(f"[italic green][TIME][/italic green] {text}!")
    log(text)

log3("STARTING")