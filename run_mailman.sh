#!/bin/bash
# run as "sudo -u mailman ./run_mailman.sh /path/to/<mailman-shell-script-ohne-extension.py>"
#
#  upd 20250825
# init 20250810
#
# If you want to run a mailman-shell-script with output:
#
# login as mailman and switch to (venv)
# sudo su mailman
# then issue
# PYTHONPATH="/home/maillistgen" mailman withlist -r <mailman-shell-script-filename-without-path-and-without-extension>
# The script is one function def(mailman-shell-script-filename-without-extension)
#
# Example:
#
# /home/maillistgen/script.py:
# def script():
#   return
#
# sudo su mailman
# PYTHONPATH="/home/maillistgen" mailman withlist -r script
#
# or
# sudo -u mailman /home/maillistgen/run_mailman.sh /home/maillistgen/script
#
# or - better
# sudo -u mailman /bin/bash -c 'source /opt/mailman/venv/bin/activate && PYTHONPATH="/home/maillistgen" mailman withlist -r script'


if [ $# -eq 0 ]; then
   if [ $(id -un) != "mailman" ]; then
      echo "Das Script muss unbedingt als user mailman ausgeführt werden."
   fi
   echo "run as \"sudo -u mailman ./run_mailman.sh /path/to/<mailman-shell-script-ohne-extension.py>\""
   exit 1
fi

# check for user maillistgen
if [ $(id -un) != "mailman" ]; then
  echo
  echo "Das Script muss als user mailman ausgeführt werden."
  echo
  echo "Benutze alternativ \"sudo -u mailman ./run_mailman.sh /path/to/<mailman-shell-script-ohne-extension.py>\""
  echo "25.08.2025 Pascal"
  exit 1
fi

# Extrahiere Pfad
if [[ "$1" == */* ]]; then
    SPATH=${1%/*}       # Pfad aus $1
else
    SPATH=$(pwd)         # aktuelles Verzeichnis
fi

# remove path and remove extension like .py
SCRIPTX=${1##*/}
SCRIPT=${SCRIPTX%.*}

source /opt/mailman/venv/bin/activate
PYTHONPATH="$SPATH" mailman withlist -r "$SCRIPT" $2
deactivate
