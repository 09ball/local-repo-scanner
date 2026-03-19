#!/usr/bin/env python3
import os
import subprocess
import sys
import json

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                data = json.load(f)
                return set(data.get("ignored_directories", []))
        except (json.JSONDecodeError, IOError):
            return set()
    return set()

ignored_directories = load_config()

def prune(search_path):
    repo_path = []
    for root, dirs, files in os.walk(search_path, topdown=True):
        to_ignore = ignored_directories.copy()
        if ".git" in to_ignore:
            to_ignore.remove(".git")

        dirs[:] = [d for d in dirs if d not in to_ignore]

        if ".git" in dirs:
            repo_path.append(root)
            if ".git" in dirs:
                dirs.remove(".git")

    return repo_path

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    search_root = os.path.abspath(target)
    found_dirty = False

    repos = prune(search_root)

    for repo in repos:
        status_cmd = subprocess.run(["git", "status", "--porcelain", "-u"], cwd=repo, capture_output=True, text=True)
        stash_cmd = subprocess.run(["git", "stash", "list"], cwd=repo, capture_output=True, text=True)

        tags = []
        if status_cmd.stdout.strip():
            tags.append("MODIFIED")
        if stash_cmd.stdout.strip():
            tags.append("STASH")
        if os.path.isdir(os.path.join(repo, "bin")):
            tags.append("BIN")

        if tags:
            found_dirty = True
            print(f"\n[FOUND] [{','.join(tags)}] {repo}")

            if "MODIFIED" in tags:
                print("Changes:")
                print(status_cmd.stdout.rstrip())

            if "STASH" in tags:
                print("Stashes:")
                print(stash_cmd.stdout.rstrip())

    if not found_dirty:
        print("\n[INFO] All repos are clean.")

if __name__ == "__main__":
    main()