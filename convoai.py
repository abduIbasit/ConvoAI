import argparse
from core import ConvoAI

convoai = ConvoAI()

def start_cli():
    parser = argparse.ArgumentParser(description="ConvoAI CLI")
    subparsers = parser.add_subparsers(title="command", description="Valid commands", help="Available commands", dest="command")

    start_parser = subparsers.add_parser('start', help='Start the chatbot CLI')
    # Add more parsers as needed for other commands

    args = parser.parse_args()

    if args.command == "start":
        convoai.main()
    else:
        parser.print_help()

if __name__ == "__main__":
    start_cli()