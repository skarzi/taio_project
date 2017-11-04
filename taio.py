#!/usr/bin/env python

import argparse

from taio.solution import solution

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "file", type=str, help="path to file containing input data",
    )
    parser.add_argument(
        "-n", "--no-assignments", help="don't print assignments",
        action="store_true"
    )
    args = parser.parse_args()

    max_flow, assignments = solution(args.file)
    if not args.no_assignments:
        for assignment in assignments:
            print(assignment)
    print(max_flow)
