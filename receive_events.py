import json
import ssl
import time
from nostr.filter import Filter, Filters
from nostr.event import Event, EventKind
from nostr.relay_manager import RelayManager
from nostr.message_type import ClientMessageType
from nostr.key import *
import datetime
import uuid
from post_note import *
from apscheduler.schedulers.blocking import BlockingScheduler
from set_query_filters import *

# def receive_events(request, filters):
def receive_events():
  request, filters = set_query_filters()

  print(request, filters)
  relay_manager = RelayManager()
  # relay_manager.add_relay("wss://nostr-pub.wellorder.net")
  relay_manager.add_relay("wss://relay.damus.io")
  # relay_manager.add_relay("wss://nostr1.current.fyi")
  # relay_manager.add_relay("wss://relay.current.fyi")
  # relay_manager.add_relay("wss://relay.nostr.bg")
  relay_manager.add_subscription(subscription_id, filters)
  relay_manager.open_connections({"cert_reqs": ssl.CERT_NONE}) # NOTE: This disables ssl certificate verification
  time.sleep(1.25) # allow the connections to open
  message = json.dumps(request)
  relay_manager.publish_message(message)
  time.sleep(1) # allow the messages to send

  while relay_manager.message_pool.has_events():
    event_msg = relay_manager.message_pool.get_event()
    print("\n\n___________NEW_EVENT__________")
    print(f"{event_msg}\n")
    print(event_msg.event.content)
    print(f"created_at: {event_msg.event.created_at}")
    print(f"created at ISO: {datetime.datetime.fromtimestamp(event_msg.event.created_at)}")
    print(f"event.tags: {event_msg.event.tags}")
    print(f"event.kind: {event_msg.event.kind}")
    # print(event_msg.event.public_key)
    # print(event_msg.event.signature)
    print(f"event.id: {event_msg.event.id}")
    print(f"event.json: {event_msg.event.json}")
    print(f"event.json[2]['id']: {event_msg.event.json[2]['id']}")

    # with open('events.json','r+') as f:
    #   events = json.load(f)
    #   events.append(event_msg.event.json)
    #   f.seek(0)
    #   f.write(json.dumps(events, indent=4))

    with open('events.json','r+') as f:
      append_event = True
      events = json.load(f)
      for event in events:
        if event[2]['id'] == event_msg.event.id:
          print('found id on json, switching append event to false')
          append_event = False
      if append_event == True:
        print('didnt find event on json, appending')
        events.append(event_msg.event.json)
        f.seek(0)
        f.write(json.dumps(events, indent=4))
        post_note(private_key.from_nsec("nsec1zajhm4ejm9sf50dc88eyex4myqf9wt8ru2d46wjs72am9w0t89yqmamg3e"), "content todo", [["e",event_msg.event.id],["p",public_key]])
  
  relay_manager.close_connections()

if __name__ == "__main__":

  # since = int(datetime.datetime.fromisoformat(input("What date would you like to start at? ")).timestamp())
  # since = int(datetime.datetime.now())
  since = int(datetime.datetime.fromisoformat("2023-05-09").timestamp())

  # print(since)
  subscription_id = uuid.uuid1().hex
  print(f"subscription id is {subscription_id}")
  public_key = PublicKey.from_npub("npub1x2v0vnn059dv3ep9h45lwfgdnynl9nseqsg7safkrrqdc6va3c2qs0kkjg").hex()
  print(public_key)

  receive_events()

  # scheduler = BlockingScheduler()
  # scheduler.add_job(receive_events, 'interval', seconds=30, args=[request, filters])
  # scheduler.start()
  # connect_to_relays_and_request_payload(request, filters)