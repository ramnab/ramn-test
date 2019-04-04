import glob
import fileinput
import sys
import os
import json
import argparse


def main():
    """
    Copies the transforms/ and modules/ directories, substituting in values from the
    given config file

    :return:    None
    """

    parser = argparse.ArgumentParser(description='''
    
    Usage:
        python token_replace.py -f CONFIG
    
    For example:
        python scripts/token_replace.py -f configs/ccm-tradeuk-dev.json 
    
    '''
                                     )
    parser.add_argument('-f', '--file',
                        help='Config file/path',
                        required=True)

    args = parser.parse_args()

    conf = {}
    with open(args.file, 'r') as f:
        d = json.load(f)
        for key, val in d.items():
            conf[f"[{key}]"] = val

    files = glob.glob("generated/**", recursive=True)

    if files is not []:
        for file in files:
            if os.path.isfile(file):
                for line in fileinput.input(file, inplace=1):
                    for key, val in conf.items():
                        line = line.replace(key, val)
                    sys.stdout.write(line)

    print("Success")


if __name__ == '__main__':
    sys.exit(main())
