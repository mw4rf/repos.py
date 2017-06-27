#!/usr/bin/env python3

# MIT License
# Copyright (c) [2017] [mw4rf]
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# HowTo
#
# 1.a) Setup (mandatory)
# Fill the configuration file (default: repos.cfg) with the following syntax:
# Repo1_name | Repo1_url
# Repo2_name | Repo2_url
#
# 1.b) Setup (optional)
# Run < chmod u+x repos.py >
# Then, replace < python3 repos.py COMMAND > with < ./repos.py COMMAND >
#
# 2. Clone repositories
# Run < python3 repos.py clone >
# All repositories defined in the configuration file will be cloned. Existing repositories will be ignored.
#
# 3. Get informations about repositories
# Run < python3 repos.py info >

# HISTORY
#
# V. 0.1.1 (27/06/2017)
# Code cleanup & licence
#
# v.0.1 (26/06/2017)
# Cloning Repos

# Configuration
config_file = "repos.cfg"

# Imports
import subprocess
import string


# Classes
class Repo:
	def __init__(self):
		self.name = ""
		self.url = ""


# Get repositories list from config file
repos = [] # Store repositories in this array
with open(config_file) as f: # Read config file 
	content = (line.rstrip() for line in f) # Read all the lines, including empty ones
	content = list(line for line in content if line) # Remove blank lines
content = [x.strip() for x in content] # Remove leading & trailing spaces & line feed characters (\n)
for line in content:
	# Ignore commentaries, i.e. lines starting with #
	if(line.startswith("#")):
		continue
	# Explode line with | delimiter
	res = line.split("|")
	# Make Repo object
	r = Repo()
	r.name = res[0].strip()
	r.url = res[1].strip()
	# Append object to array
	repos.append(r)


# Run shell commands
def run_command(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line 
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        #raise subprocess.CalledProcessError(return_code, cmd)
        pass


# Parse command line arguments
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("commande")
args = parser.parse_args()


# Command = info
def info():
	print("Repositories list.")
	for repo in repos:
		print(repo.name + ": <" + repo.url + ">")


# Command = clone
def clone():
	print("Cloning repositories...")
	for repo in repos:
		print("Cloning: <" + repo.name + ">")
		for op in run_command(["git", "clone", repo.url]):
			print(op, end="")


# Run commands
if(args.commande == "info"):
	info()
elif(args.commande == "clone"):
	clone()
else:
	print("Unknown command!")