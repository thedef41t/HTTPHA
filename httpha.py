from cli.header import header, clear_cli
from cli.parser import build_parser, helper
from mapper.verifier import verify_web

def main(argv=None) -> int:

    parser = build_parser()
    args = parser.parse_args(argv)

    clear_cli()
    header()

    if args.help or not any(vars(args).values()):
        helper(parser)
        return 0

    # ------------------------------------------
    if args.url:
        verify_web(args.url)
    # ------------------------------------------

if __name__ == "__main__":
    main()
