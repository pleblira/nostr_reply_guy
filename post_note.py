import json
import ssl
import time
from nostr.event import Event
from nostr.relay_manager import RelayManager
from nostr.key import PrivateKey
from dotenv import load_dotenv, find_dotenv
import os
from apscheduler.schedulers.blocking import BlockingScheduler
import random

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

private_key = os.environ.get("PRIVATE_KEY")
private_key = PrivateKey.from_nsec(private_key)
# print(private_key)
# print("private_key")

# private_key = PrivateKey()
# print(private_key.bech32())

def post_note(private_key, content, tags):
    relay_manager = RelayManager()
    # relay_manager.add_relay("wss://relay.nostr.bg")
    relay_manager.add_relay("wss://relay.damus.io")
    # relay_manager.add_relay("wss://relay.snort.social")
    relay_manager.open_connections({"cert_reqs": ssl.CERT_NONE}) # NOTE: This disables ssl certificate verification
    time.sleep(1.25) # allow the connections to open

    event = Event(private_key.public_key.hex(), "Hey there " + str(random.randint(3, 9000)), tags=tags)
    # event = Event(private_key.public_key.hex(), "Hey there " + str(random.randint(3, 9000)))
    private_key.sign_event(event)

    relay_manager.publish_event(event)
    print("note sent")
    time.sleep(1)

    relay_manager.close_connections()


if __name__ == '__main__':
    # post_note()
    post_note(private_key.from_nsec("nsec1zajhm4ejm9sf50dc88eyex4myqf9wt8ru2d46wjs72am9w0t89yqmamg3e"), "content todo", tags="")
    # post_note(private_key.from_nsec("nsec1n6gpk38csg3yy78tgy55kunm4aald8p7s789npyup27zevu80ecqes3mvh"), "content todo", tags="")

    # scheduler = BlockingScheduler()
    # scheduler.add_job(post_note, 'cron', hour=0, minute=51, timezone="America/New_York")
    # scheduler.add_job(post_note, 'interval', seconds=20)
    # print('Press Ctrl+{0} to stop scheduler and switch to manual tweet.'.format('Break' if os.name == 'nt' else 'C'))