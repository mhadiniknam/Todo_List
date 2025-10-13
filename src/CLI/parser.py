import argparse

class CLI:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(description="ToDoList CLI")
        self.subparse 

        
    def create_parser(self):
        self.subparsers = self.parser.add_subparsers(dest="command", required=True)


        return self.parser