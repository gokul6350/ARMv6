from rich.console import Console
from rich.prompt import Prompt
import chat
import time

console = Console()
def paser(msg):
    
 

    original_string = msg
    print(msg)

# Split the string based on "#"
    parts = original_string.split('#')
    first_part = parts[0].strip()
    second_part = parts[1].strip()
    cmd=first_part
    repp=second_part
    return [repp,cmd]
def main(objs):
    

    username = "Human"
    while True:
        message = Prompt.ask(f"[bold cyan] {username}")

        if message.lower() == 'exit':
            console.print("Goodbye!")
            break

        #console.print(f"Human: {message}", style="#af00ff")

        with console.status("[bold green]Generating Responces") as status:
            message=f"{objs}  {message}"
            response = "_pickup(battery) # Picking up the battery"#chat.gen_ai(message)
            if response[0] == "_":
                repp=paser(response)
                cmd=repp[1]
                respon=repp[0]


        
        console.print(f"Robot: {respon}", style="#00ffaf")
        if response[0] == "_":
            return cmd

def action(act):
    #with console.status("[bold green]Generating Responces") as status:
    NotImplementedError