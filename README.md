Scripts for maintenance or setting-up of modern mailman3 instances

To say it loud and clearly:

mailman3 lives in (venv) in `/opt/mailman`

* set preferences for all users
* list held messages
* delete held messages older n days


My setting is strictly as described in the documentation:

* mailman3 + postorius/hyperkitty are installed via `pip` in an `(venv) /opt/mailman/`
* My user scripts and a huge mailing list generator (not published here) are in a directory apart from that: user `maillistgen` home directory `/home/maillistgen`
* user maillistgen has some sudo rights set uo in /etc/sudoers
* a wrapper script is `/home/maillistgen/run_mailman.sh` which sets the correct path for Python, mailman3 and the (venv).
  
