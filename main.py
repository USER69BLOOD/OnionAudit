import non_interactive as  cli 

def main():
    parser = cli.parse_args()
    args = cli.parse_and_validate_args(parser)
    cli.run(args)

if __name__ == "__main__":
    main()
    

    
