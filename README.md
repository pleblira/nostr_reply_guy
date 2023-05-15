# nostr_reply_guy

All keys included are test keys.

- Set the query filters on set_query_filters.py

Events that have been replied to are saved to events.json file.

Every time the scheduler runs, it checks the date on the last queried event and runs the query based on the date of the last event queried and replied to.

- Requires an update to the nostr Python library. All Nostr dependencies are included in the package.
