from art import text2art
from utils.rich_console import r_console

def clear_cli():
    import os
    import subprocess
    subprocess.call("clear" if os.name == "posix" else "cls", shell=True)

def header():
    header_art = text2art("HTTPHA", font="small", chr_ignore=True)
    r_console.print(f"{header_art}", style="red")