import argparse

def build_parser() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(
        description="Automated HTTP Security & Header Auditing Tool",
        add_help=False
    )

    parser.add_argument(
        "--url",
        "-u",
        type=str,
        help="The URL of the website to audit (e.g., https://example.com)"
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Output file to save results"
    )
    parser.add_argument(
        "-h", "--help",
        action="store_true",
        help="Show this help message and exit",
    )

    return parser

def helper(parser: argparse.ArgumentParser):
    print(parser.format_help())