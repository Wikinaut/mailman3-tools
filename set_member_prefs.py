def set_member_prefs():
# setting certain standard member preferences to all members in all mailinglists
# TG 20250806

  from zope.component import getUtility
  from mailman.interfaces.listmanager import IListManager
  from mailman.interfaces.member import DeliveryMode, DeliveryStatus

  hide_address = False
  delivery_status = DeliveryStatus.enabled
  lm = getUtility(IListManager)

  for mlist in lm.mailing_lists:
    print(f"... setting standard member preferences in {mlist.fqdn_listname}")
    for member in mlist.members.members:
      prefs = member.preferences
      prefs.acknowledge_posts = True
      prefs.hide_address = hide_address
      prefs.preferred_language = 'de'
      prefs.receive_list_copy = True
      prefs.receive_own_postings = True
      prefs.delivery_mode = DeliveryMode.regular
      prefs.delivery_status = delivery_status
      # print(f"Updated {member.address.email} in list {mlist.fqdn_listname}")
