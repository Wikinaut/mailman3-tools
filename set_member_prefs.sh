#!/bin/bash
sudo -u mailman ./run_mailman.sh /home/maillistgen/set_member_prefs
# sudo -u mailman bash -c '
#  source /opt/mailman/venv/bin/activate
#  PYTHONPATH="/home/maillistgen" mailman withlist -r set_member_prefs
#  deactivate
#'
