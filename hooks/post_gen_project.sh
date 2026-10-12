#!/usr/bin/env bash
# Restore the real manifest name after generation.
#
# The template ships this file as `pyproject.toml.jinja`. GitHub's dependency-graph
# updater scans every push and tries to resolve a pip manifest at
# `{{cookiecutter.project_slug}}/pyproject.toml` - a path that does not exist,
# because the directory name is a cookiecutter placeholder. That job fails on every
# push to main ("update-pip-graph"), leaving the branch permanently red and training
# everyone to ignore red.
#
# The generated project needs a real `pyproject.toml` (its Dockerfile COPYs it), so
# the file is renamed back here, right after generation. Cookiecutter runs a
# post_gen_project.sh from inside the directory it just created - the project root.
set -euo pipefail

SRC="pyproject.toml.jinja"
DST="pyproject.toml"

if [ -f "$SRC" ]; then
  mv "$SRC" "$DST"
  echo "post-gen: restored $DST"
elif [ -f "$DST" ]; then
  echo "post-gen: $DST already in place"
else
  echo "post-gen: ERROR - neither $SRC nor $DST exists" >&2
  exit 1
fi