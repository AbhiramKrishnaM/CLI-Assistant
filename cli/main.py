import typer

app = typer.Typer(help="AI-powered CLI assistant for developers")

@app.command()
def hello():
    """Simple command to test the CLI assistant for developers"""
    print("Hello! AI CLI Assistant is ready to help you.")

if __name__ == "__main__":
    app()