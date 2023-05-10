from nostr.filter import Filter, Filters
from nostr.event import Event, EventKind
from nostr.message_type import ClientMessageType
from nostr.key import *
import datetime
import uuid

def set_query_filters():

  since = int(datetime.datetime.fromisoformat("2023-05-09").timestamp())
  subscription_id = uuid.uuid1().hex
  public_key = PublicKey.from_npub("npub1x2v0vnn059dv3ep9h45lwfgdnynl9nseqsg7safkrrqdc6va3c2qs0kkjg").hex()


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

