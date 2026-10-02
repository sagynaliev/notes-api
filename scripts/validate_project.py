#!/usr/bin/env python3
"""
INF 345 week 3 - checks a project registration: projects/<username>.yml

    python3 scripts/validate_project.py --author <github-username>   # a pull request
    python3 scripts/validate_project.py --all                        # every file on main

Checks: the file is named after the pull request's author; it has repo,
language and what; the repository URL belongs to the author; the repository
is public (it can be cloned without logging in). No third-party packages.
"""
import argparse, os, re, subprocess, sys

REQUIRED = ("repo", "language", "what")
URL = re.compile(r"^https://github\.com/([A-Za-z0-9-]+)/([A-Za-z0-9._-]+?)(?:\.git)?/?$")


def parse(path):
    """The file is three 'key: value' lines. No YAML library needed for that."""
    data = {}
    for n, line in enumerate(open(path, encoding="utf-8", errors="replace"), 1):
        line = line.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"line {n} is not 'key: value': {line.strip()[:60]}")
        k, v = line.split(":", 1)
        data[k.strip().lower()] = v.strip().strip('"').strip("'")
    return data


def is_public(url):
    env = {**os.environ, "GIT_TERMINAL_PROMPT": "0", "GIT_ASKPASS": "true"}
    p = subprocess.run(["git", "ls-remote", "--heads", url], env=env,
                       capture_output=True, text=True, timeout=60)
    return p.returncode == 0


def check(path, author=None):
    errors = []
    user = os.path.splitext(os.path.basename(path))[0]
    if author and user.lower() != author.lower():
        errors.append(f"the file must be named projects/{author}.yml (your GitHub "
                      f"username), not {os.path.basename(path)}")
    try:
        data = parse(path)
    except ValueError as exc:
        return [str(exc)]
    for key in REQUIRED:
        if not data.get(key):
            errors.append(f"missing '{key}:'")
    m = URL.match(data.get("repo", ""))
    if not m:
        errors.append("repo must look like https://github.com/<you>/<project>")
    else:
        owner = m.group(1)
        expected = author or user
        if owner.lower() != expected.lower():
            errors.append(f"the repository belongs to '{owner}', not '{expected}'. "
                          f"Register your own repository.")
        elif not is_public(data["repo"]):
            errors.append("the repository cannot be cloned without logging in. Make it "
                          "public: Settings -> General -> Danger Zone -> Change visibility.")
    return errors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--author")
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    files = sorted(f for f in os.listdir("projects")
                   if f.endswith(".yml") and f != "EXAMPLE.yml")
    if a.author:
        files = [f for f in files if f[:-4].lower() == a.author.lower()] or \
                [f"{a.author}.yml"]
    bad = 0
    for f in files:
        p = os.path.join("projects", f)
        if not os.path.isfile(p):
            print(f"::error::projects/{f} not found. Add exactly that file.")
            bad += 1
            continue
        errs = check(p, a.author)
        for e in errs:
            print(f"::error file={p}::{e}")
        print(f"{'FAIL' if errs else 'ok  '} {p}")
        bad += bool(errs)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
