def list_or_delete_held_messages(delete_older_than=-1):

# list or list and delete held messages
#
#  upd 20250826
# init 20250824
#
# [MM3-users] Is there a way to see all the list's held messages
# https://lists.mailman3.org/archives/list/mailman-users@mailman3.org/thread/GLYTIS5HN6MDTEINFHNIXURDVCSSGIBY/
#
# [MM3-users] Re: Getting rid of held messages from the command line
# https://lists.mailman3.org/archives/list/mailman-users@mailman3.org/message/2JACJENOUDODYHRVL6VCNZNFRZNIRIE3/

  import re
  def parse_cutoffdays(arg: str | None):
    if (not arg) or (arg == -1):
        return False
    m = re.fullmatch(r"delete_older_than=(\d+)", arg)
    if not m:
        return False
    number = int(m.group(1))
    return number if number > 0 else False

  days = parse_cutoffdays(delete_older_than)

  if days:
    print(f"Forced deletion of held messages older than {days} days.")
  else:
    print(f"Example usage for listing held messages (default):")
    print(f"mailman withlist -r list_or_delete_held_messages")
    print()
    print(f"Example usage for forced deletion of held messages older than 7 days:")
    print(f"mailman withlist -r list_or_delete_held_messages delete_older_than=7")

  from datetime import datetime, timedelta
  if days:
     cutoff = datetime.utcnow() - timedelta(days)

  from zope.component import getUtility
  from mailman.app.moderator import handle_message
  from mailman.interfaces.listmanager import IListManager
  from mailman.interfaces.requests import IListRequests
  from mailman.interfaces.messages import IMessageStore
  from mailman.interfaces.requests import RequestType

  lm = getUtility(IListManager)
  msg_db = getUtility(IMessageStore)

  def now():
    now = datetime.now()
    return now.strftime("%Y%m%d-%H%M%S")

  outfn=f"/home/maillistgen/held-messages/held-messages-{now()}.log"
  print()
  print(f"Writing list of held messages to file {outfn}")
  print()

  with open( outfn, 'w') as f:
     for mlist in getUtility(IListManager):
        requests = IListRequests(mlist)
        first = True
        for request in requests.held_requests:
           print(f"Request-Id: {request.id}")
           key, data = requests.get_request(request.id)

           xstr = ""
           if days:
              submitted = datetime.fromisoformat(data['_mod_hold_date'])
              compared = submitted > cutoff

              if compared:
                 xstr = f"submitted {submitted} > cutoff {cutoff}"
              else:
                 xstr = f"*** OLDER THAN {days} DAYS *** WILL BE DELETED *** submitted {submitted} < cutoff {cutoff}"
                 requests.delete_request(request.id)

           if first:
              first = False
              print(mlist.list_id)

           print(f"""\
{xstr}Sender: {data['_mod_sender']}
Subject: {data['_mod_subject']}
Date: {data['_mod_hold_date']}
Reason: {data['_mod_reason']}
""")

           f.write(f"""\
{xstr}Sender: {data['_mod_sender']}
Subject: {data['_mod_subject']}
Date: {data['_mod_hold_date']}
Reason: {data['_mod_reason']}
""")
           f.write('\n')


  f.close()

  print("\nOverview:")
  print("=========\n")

  held_messages_total_count = 0
  for mlist in lm.mailing_lists:
    requests = IListRequests(mlist)

    if not requests.held_requests:
        continue

    discarded_count = 0
    held_messages_count = requests.count_of(RequestType.held_message)
    if held_messages_count > 0:
       print(f"{mlist.fqdn_listname}: {held_messages_count} messages waiting for moderation.")
       held_messages_total_count += held_messages_count

  print(f"\nTotal count: {held_messages_total_count} messages are waiting for moderation.")
