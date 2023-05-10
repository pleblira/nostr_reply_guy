from nostr.filter import Filter, Filters
from nostr.event import Event, EventKind
from nostr.message_type import ClientMessageType

def set_query_filters(public_key, since, subscription_id):
  # setting public key and filters

  # query all events from a npub. npub is a list.
  # filters = Filters([Filter(authors=[public_key], kinds=[EventKind.TEXT_NOTE])])

  # query events since and until specific dates
  # filters = Filters([Filter(authors=[public_key], kinds=[EventKind.TEXT_NOTE], since=1683602000, until=1676091000)])

  # query list of events since specific date
  filters = Filters([Filter(authors=[public_key], kinds=[EventKind.TEXT_NOTE], since=since)])

  # query a specific event from relays, based on event_id
  # filters = Filters([Filter(event_ids=["45e7358ab11687c68a27bd0ceb33836b014b1e9c3ed9f46d0fadd07d10bbe7e3"])])
  request = [ClientMessageType.REQUEST, subscription_id]
  request.extend(filters.to_json_array())
  # print(filters)
  return request, filters

