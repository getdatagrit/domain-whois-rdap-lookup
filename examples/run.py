# pip install apify-client
import os
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("datagrit/domain-whois-rdap-lookup").call(run_input={
    "domains": [
        "stripe.com",
        "shopify.com",
        "atlassian.com",
        "nature.com",
        "wikipedia.org",
        "mozilla.org",
        "bbc.co.uk",
        "lemonde.fr",
        "web.dev",
        "google.io",
        "google.us",
        "zzqx-nonexist-8841.com"
    ]
})
items = client.dataset(run["defaultDatasetId"]).list_items().items
print(len(items), "records")
print(items[0] if items else None)
