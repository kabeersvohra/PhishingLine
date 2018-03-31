#!/usr/bin/env python
"""
Simple script to check files against signatures.

This script supports matching rules extracted from an ldb file (e.g.,
https://raw.githubusercontent.com/EmergingThreats/phishpunch/master/etphish.ldb) against the
content of one or more files.

:Copyright:
    Copyright 2018 Lastline, Inc.  All Rights Reserved.
"""
import argparse
import binascii
import collections
import sys

_RULE_FIELDS = [
    "name",
    "engine",
    "cond",
    "clauses",
]
Rule = collections.namedtuple("Rule", _RULE_FIELDS)


def _get_clauses(clauses_list):
    clauses = []
    for c in clauses_list:
        pattern_hex = c[:c.index("::")]
        pattern = binascii.unhexlify(pattern_hex)
        clauses.append(pattern)
    return clauses


def _get_rule(line):
    fields = line.split(";")
    rule = Rule(
        name=fields[0],
        engine=fields[1],
        cond=fields[2],
        clauses=_get_clauses(fields[3:]),
    )
    assert rule.clauses, "{} {}".format(line, fields)
    return rule


def get_rules(fname):
    rules = []
    with open(fname, "r") as f:
        for line in f.readlines():
            rules.append(_get_rule(line))
    return rules


def matches_rules(fname, rules):
    with open(fname, "rb") as f:
        data = f.read()

    for r in rules:
        pos = [data.find(e) for e in r.clauses]
        if all(e >= 0 for e in pos):
            return r, pos
    return None, None


def matches_rules_count(fname, rules):
    with open(fname, "rb") as f:
        data = f.read()

    matches = 0

    for r in rules:
        pos = [data.find(e) for e in r.clauses]
        if all(e >= 0 for e in pos):
            if len(pos) > matches:
                matches = len(pos)

    return matches


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("files", metavar="FILE", nargs="*", help="the files to match")
    parser.add_argument("--rules", metavar="LDB", help="the rules file")
    parser.add_argument("--list-rules", action='store_true')

    args = parser.parse_args(argv)

    rules = get_rules(args.rules)

    if args.list_rules:
        print("\n".join(map(str, rules)))
        return 0

    ret = 0
    for fname in args.files:
        m, pos = matches_rules(fname, rules)
        if m:
            ret = 1
            status = "PHISH ({}, {})".format(m.name, pos)
        else:
            status = "CLEAN"
        print("{}: {}".format(fname, status))

    return ret


if __name__ == "__main__":
    main(sys.argv[1:])
