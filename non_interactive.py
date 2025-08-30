import argparse
import sys
from msgs import show_banner, log
from tor_search import search, check_onion
import interactive
from utils import live_check

def parse_args():
    """
    Handles CLI arguments for OnionAudit.
    Returns a namespace of parsed arguments.
    """
    SOURCE = ["Ahmia", "TOR66", "Torch"]

    parser = argparse.ArgumentParser(
        description="OnionAudit - Search and validate .onion links"
    )

    # Core arguments
    parser.add_argument(
        "-q", "--query",
        type=str,
        help="Keyword to search for"
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Show only live onion links"
    )
    parser.add_argument(
        "--sources",
        type=str,
        nargs="+",
        help=f"Custom sources to search available: {','.join(SOURCE)} (default: All)"
    )
    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Enable interactive mode for guided usage"
    )
    parser.add_argument(
        "-c","--check",
        type=str,
        help="Check if a single .onion URL is live"
    )
    parser.add_argument(
        "-o","--output",
        type=str,
        help="Save the resulting onion links to the specified file"
    )
    parser.add_argument(
    "--quiet",
    action="store_true",
    help="Suppress output, only show essential information"
    )
    parser.add_argument(
    "--check-list",
    type=str,
    help="Path to a file containing .onion URLs to check if they are live"
    )
    parser.add_argument(
    "--output-live",
    type=str,
    help="Save only live onion links to the specified file"
    )


    return parser


def parse_and_validate_args(parser):
    """
    Checks if user provided arguments and validates them.
    Returns parsed args if non-interactive, or None for interactive mode.
    """

    KNOWN_ARGS = [
        "--interactive", "-i",
        "--query", "-q",
        "--sources",
        "--check",
        "--check-list",
        "--quiet",
        "--output", "-o",
        "--live",
        "--output-live",
        "--help"
    ]


    # Check for unknown args
    unknown_args = [
        arg for arg in sys.argv[1:]
        if arg.startswith('-') and arg not in KNOWN_ARGS
    ]
    if unknown_args:
        print(f"Unknown arguments: {', '.join(unknown_args)}")
        sys.exit(1)

    args = parser.parse_args()

    # --- Rules enforcement ---

    # If interactive, no other switch allowed
    if args.interactive and (
        args.query or args.sources or args.check or args.check_list or args.output or args.live
    ):
        print("Error: --interactive (-i) cannot be used with other options.")
        sys.exit(1)

    if args.query and (args.check or args.check_list):
        print("Error: --query cannot be used with --check or --check-list.")
        sys.exit(1)

    if args.check and (
        args.sources or args.check_list or args.output or args.live
    ):
        print("Error: --check must be used alone.")
        sys.exit(1)

    if args.check_list and (args.query or args.sources or args.check or args.live) :
        print("Error: --check-list can only be used with --output.")
        sys.exit(1)


    if args.output and not (args.query or args.check_list):
        print("Error: --output must be used with --query or --check-list.")
        sys.exit(1)
    
    if args.sources and not args.query:
        print("Error: --sources can only be used with --query.")
        sys.exit(1)

    if args.live and not (args.query or args.check_list):
        print("Error: --live must be used with --query or --check-list.")
        sys.exit(1)

    if len(sys.argv) == 1 or args.interactive:
        return None

    return args

def valid_source(source):
    known = ["AHMIA", "TOR66", "TORCH"]

    for _ in [field.strip() for field in sources.split(",")]:
        if _ not in known:
            print(log("Sources Error.", "error"))


def run(args):
    
    # If no arguments passed, run interactive mode and exit
    if args is None:
        interactive.run()
        sys.exit()

    if not args.quiet:
        show_banner()

     # --- Case: Search query provided ---
    if args.query:

        if args.sources is not None:
            valid_source(args.sources)
        
        print(log(f"Searching {args.query} for '{args.sources}'...", "info"))

        onions = search(args.query, args.sources)
        print(log(f"Found {len(onions)} potential onion addresses.", "success"))

        # Handle no results scenario
        if len(onions) == 0:
            print(log(f"Might some error.......", "warn"))
            print(log(f"Or the query has no result.", "info"))
            
            time.sleep(2)
            sys.exit()

        # --- Case: Save fetched onions to a file ---
        if args.output:
            print(log(f"Fetching Onion....", "info"))
            with open(args.output, "a", encoding="utf-8") as file:
                for onion in onions:
                    if not args.quiet:
                        print(log(f"fetched onion : {onion}", "info"))
                    file.write(onion + "\n")

            print(log(f"Fetched Onions Saved to {args.output}.", "info"))

        if args.live:
            print(log(f"Checking onions if Live....", "info"))
            with open(args.output_live, "a", encoding="utf-8") as file:
                for onion in onions:
                    if check_onion(onion):
                        if not args.quiet:
                            print(log(f"live : {onion}", "info"))
                        if args.output_live:
                            file.write(onion + "\n")
            
            if args.output_live:
                print(log(f"Live Onions Saved to {args.output_live}.", "info"))

        sys.exit()

    # --- Case: Single onion check ---
    if args.check:
        _ = live_check(args.check)

     # --- Case: Check list of onions from a file ---
    if args.check_list:

        try:
            with open(args.check_list, "r", encoding="utf-8") as f:
                onions_to_check = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(log(f"File not found: {args.check_list}", "error"))
            sys.exit(1)

        with open(args.output_live or args.output, "a", encoding="utf-8") as file:
            for onion in onions_to_check:
                if (args.output_live or args.output) and live_check(onion, args.quiet):
                    file.write(onion + "\n")

            if args.output_live or args.output:
                print(f"Live Onions Saved to {args.output_live or args.output}", "info")

