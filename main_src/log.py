import logging
from rich import print


logging.basicConfig(filename='app1.log', 
                    filemode='a',  
                    level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
def log1(text):
    print(f"[italic red][LOG][/italic red] {text}!")
    logging.info(text)
def log2(text):
    print(f"[italic green][INFO][/italic green] {text}!")
    logging.info(text)
