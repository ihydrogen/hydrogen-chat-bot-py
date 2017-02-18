from console import bot_console

def main(c):
    console = bot_console.Console()
    console.run("longpool stop")
    console.run("longpool start")