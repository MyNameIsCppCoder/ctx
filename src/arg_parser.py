import argparse
from .copy import copy_report

def parse_arg():
    parser = argparse.ArgumentParser(
        description="Purpose of the util is making UX with LLM and develoopment are better.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("-copy", "--copy", )
