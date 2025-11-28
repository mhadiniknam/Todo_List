from src.Task import * 
from fastapi import FastAPI
from src.CLI.parser import CLI 
from src.CLI.commands import *

"""
I structure the CLI as a ArgParser 
Which we pass what we want and it will call the correct function
for that need.

like a office which some one can redirect you to subsections

It would look like 

poetry run main.py create_task .... 
"""

def run_api():
    """Run the FastAPI server."""
    import uvicorn
    from src.api.routers  import router
    app = FastAPI(
            title="TodoList API",
            description = "Manage your task and project with API",
            version="1.0.0"
        )
    app.include_router(router, prefix="/api/v1")
    uvicorn.run(app, host="0.0.0.0", port=8000)

def main():
    """___Main___"""
    run_api()
    cli = CLI()
    cli.start()

if __name__ == "__main__":
    main()
