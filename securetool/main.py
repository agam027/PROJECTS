from password_strength import strength
from util import strength_check, hasher, verify, audit, struct_print
import argparse

def main():
    parser = argparse.ArgumentParser(
        description="A Personal Security Utility"
    )
    subparser = parser.add_subparsers(
        dest="command",
        required=True
    )


    check_parser = subparser.add_parser(
        "check",
        help="check password strength"
    )
    check_parser.add_argument(
        "password",
        help="type password"
    )


    hash_parser = subparser.add_parser(
        "hash",
        help="hash your password"   
    )
    hash_parser.add_argument(
        "password",
        help="type password"
    )
    hash_parser.add_argument(
        "--algo",
        default="sha256",
        help="name the algorithm to use"
    )


    verify_parser = subparser.add_parser(
        "verify",
        description="Verify a password with hash"
    )
    verify_parser.add_argument(
        "--hash",
        help="Password hash"
    )
    verify_parser.add_argument(
        "--password",
        help="Enter password"
    )
    verify_parser.add_argument(
        "--algo",
        default="sha256",
        help="algorithm used while hashing"
    )


    audit_parser = subparser.add_parser(
        "audit",
        description="scans a text file for weak passwords"
    )
    audit_parser.add_argument(
        "file",
        help="name the file location"
    )
    audit_parser.add_argument(
        "--min-score",
        help="minimum score to be considered not weak"
    )


    args = parser.parse_args()

    if args.command == "check":
        strength_check(args.password)
    elif args.command == "hash":
        hasher(args.password, args.algo)
    elif args.command == "verify":
        print("\n Matched\n" if verify(args.hash, args.password, args.algo) else "\n  Match Failed\n")
    elif args.command == "audit":
        struct_print(audit(args.file, args.min_score))
    
    



if __name__ == "__main__":
    main()

#python main.py check "P@ssw0rd123"
#python main.py hash "mypassword" --algo sha256
#python main.py verify --hash <hash> --password "test123"
#python main.py audit passwords.txt --min-score 
