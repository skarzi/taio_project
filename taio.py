#!/usr/bin/env python
from __future__ import print_function

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

    flow_loss, assignments = solution(args.file)
    if not args.no_assignments:
        for worker, project in assignments:
            print(worker, project)
    print(flow_loss)
