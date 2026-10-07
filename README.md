# Domain WHOIS RDAP Lookup - DNS, MX & Expiry

Bulk domain lookup: official RDAP (WHOIS) registration, expiry and availability plus DNS, mail provider, SPF/DMARC and hosting ASN, with expiry and registrar filters.

[![Run on Apify](https://img.shields.io/badge/Run%20on-Apify-0f9f74)](https://apify.com/datagrit/domain-whois-rdap-lookup) [![Docs](https://img.shields.io/badge/docs-getdatagrit.github.io-0e1726)](https://getdatagrit.github.io/domain-whois-rdap-lookup/)

**from $3.50 per 1,000 results + $10 per run (pay per result; the rate depends on your Apify plan).** Export as JSON, CSV or Excel, call it through the API, or schedule it on Apify.

## What it does

Domain WHOIS RDAP Lookup takes a list of domains and returns one flat row per domain: official registration data from the registry's RDAP server (the structured successor of WHOIS) plus the domain's DNS, mail provider, SPF and DMARC policy, and hosting network. It is built for bulk work: SEO and domain investors checking age and expiry, sales teams enriching lead lists with mail stack data, and security teams auditing email authentication.

## Quick start

1. Open [Domain WHOIS RDAP Lookup - DNS, MX & Expiry on Apify Store](https://apify.com/datagrit/domain-whois-rdap-lookup) and click **Try for free**.
2. Fill in the input form (or paste the JSON below) and run it.
3. Download the dataset, or fetch it from the API.

```json
{
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
}
```

## Input

| Field | Type | What it does |
|---|---|---|
| `domains` | array | Domain names, one per line. URLs, www. hostnames, subdomains and e-mail addresses are accepted and reduced to the registered domain (https://blog.example.co.uk/x -> example.co.uk). Duplicates are merged. Entries that are not a domain are skipped and listed in the run status; if none is valid the run fails. With an empty list the Actor runs a small free example lookup (stripe.com, wikipedia.org, bbc.co.uk, lemonde.fr, google.io, google.de) and says so in the status message. |
| `includeDns` | boolean | Query A, AAAA, MX, NS and TXT records, the DMARC record and common DKIM selectors for every registered domain, and detect the mail provider, mail security gateway and DNS provider. Turn off for registration data only. |
| `includeHosting` | boolean | Map the first IPv4 address of the domain to its network (ASN number, network name and country) through the public Team Cymru IP-to-ASN DNS service. Needs DNS to be included. |
| `registrantFromRegistrar` | boolean | For registries that publish no registrant (for example .com, .net, .org), make a second request to the registrar's own RDAP server to read the registrant organization and country. Registrar servers are rate-limited (GoDaddy allows about 6 requests per minute), so large lists run slower; domains skipped because of a registrar limit are marked registrarRdap = rateLimited. |
| `onlyAvailable` | boolean | Return only domains with no registration at the registry (RDAP answers not found and the name is not delegated in DNS). Cannot be combined with the expiry, registration date or registrar filters. |
| `expiringWithinDays` | integer | Keep only registered domains whose registry expiry date is at most this many days away (daysToExpiry <= N), including domains already past expiry that the registry still holds. Domains whose registry publishes no expiry date (for example .ch) are dropped by this filter. 0 disables the filter. |
| `registeredAfter` | string | Keep only registered domains created on or after this date (YYYY-MM-DD, compared with createdAt in UTC). Domains without a creation date are dropped. |
| `registeredBefore` | string | Keep only registered domains created before this date (YYYY-MM-DD, the date itself excluded). Domains without a creation date are dropped. |
| `registrarContains` | array | Keep only registered domains whose registrar name contains one of these words (case-insensitive), for example GoDaddy or Namecheap. |
| `maxItems` | integer | Stop after this many returned domains. Domains not looked up because of this limit are listed in the run status. |
| `proxyConfiguration` | object | Optional proxy for the RDAP requests. Leave disabled: RDAP servers are public. DNS queries never go through the proxy. |

## Output

| Field | Type | Description |
|---|---|---|
| `input` | string | The entry from your input that produced this row. Null only on the "no match" status row. |
| `domain` | string | Registered domain that was looked up, lowercase ASCII (IDN names in punycode). Subdomains and URLs are reduced to it. |
| `tld` | string | Top-level domain (last label) used to find the RDAP server. |
| `found` | boolean | true when the registry gave a definitive answer (registered or not registered); false on rows that could not be looked up (see reason). found:false rows are free. |
| `registered` | boolean | true = the registry holds a registration; false = RDAP answered not found and the name is not delegated in DNS (available, unless the registry reserves it); null = unknown (found:false). |
| `reason` | string | Why the row has no answer: noRdapService (no RDAP server is known for the TLD: not in the IANA bootstrap nor in the verified list, e.g. .de), rateLimited, rdapError, rejectedByRegistry (the registry refused the name), unexpectedResponse, notFoundButDelegated (RDAP says not found but DNS delegates the name), dnsUnavailable (RDAP says not found but the DNS delegation check failed, so availability is not confirmed), noMatch (no domain passed your filters). Null on answered rows. |
| `registrar` | string | Sponsoring registrar name as published by the registry (for .uk the Nominet tag holder). |
| `registrarIanaId` | integer | IANA Registrar ID of the sponsoring registrar; null when the registry publishes none (many ccTLDs). |
| `registrarAbuseEmail` | string | Abuse contact e-mail of the registrar from the registry record (or from the registrar RDAP record when that lookup is on and the registry has none). |
| `createdAt` | string | Registration date (RDAP event "registration"), ISO 8601 UTC. |
| `updatedAt` | string | Last change of the registry record (RDAP event "last changed"), ISO 8601 UTC. |
| `expiresAt` | string | Registry expiry date (RDAP event "expiration"), ISO 8601 UTC. Null when the registry does not publish it (for example .ch and .li). |
| `domainAgeDays` | integer | Whole days since createdAt at the time of the run. |
| `daysToExpiry` | integer | Whole days from the run to expiresAt; negative when the date has passed and the registry still holds the domain. |
| `status` | array | Registry status codes converted from RDAP wording to EPP names, for example clientTransferProhibited, redemptionPeriod, pendingDelete; RDAP "active" becomes ok. |
| `transferLocked` | boolean | true when status contains clientTransferProhibited or serverTransferProhibited. |
| `deletionPending` | boolean | true when status contains redemptionPeriod, pendingDelete or pendingRestore (the domain is on its way to being released). |
| `nameservers` | array | Nameservers delegated at the registry, lowercase, sorted. |
| `dnssec` | boolean | Whether the delegation is DNSSEC-signed (RDAP secureDNS.delegationSigned); null when the registry does not say. |
| `registrantOrganization` | string | Registrant organization when the registry (or the registrar, with Registrant from registrar RDAP) publishes it. Null when redacted, when a privacy or proxy service is shown instead, or when no registrant data is published. Personal names, addresses, e-mails and phone numbers are never returned. |
| `registrantCountry` | string | Two-letter country code of the registrant when published and not redacted. Null when the registrant card belongs to a privacy or proxy service (Domains By Proxy, Withheld for Privacy and similar), because its address is that of the service, not of the owner; GDPR-redacted cards that keep the real country (for example MarkMonitor, Cloudflare) keep it. |
| `registrantRedacted` | boolean | true = registrant data withheld or replaced by a privacy service; false = registrant organization published; null = the record carries no registrant data (thin registries such as .com unless Registrant from registrar RDAP is on). |
| `registrarRdap` | string | notNeeded (the registry record already had registrant data), off (option disabled), noLink (the registry gives no registrar RDAP link), ok, failed, rateLimited. Null on rows of unregistered or unanswered domains. |
| `dnsStatus` | string | ok (the resolver answered; empty lists mean no such records), nxdomain (the name does not exist in DNS), failed (resolver errors for every record type; list fields are then null), skipped (DNS turned off). For not-registered domains only the NS delegation is checked. |
| `aRecords` | array | IPv4 addresses of the domain apex, sorted. [] = no A record, null = lookup failed or not run. |
| `aaaaRecords` | array | IPv6 addresses of the domain apex, sorted. [] = none, null = lookup failed or not run. |
| `mxRecords` | array | Mail exchanger hosts ordered by priority. [] = no MX record, null = lookup failed or not run. |
| `mailProvider` | string | Mailbox provider recognised from the MX hosts (Google Workspace, Microsoft 365, Zoho Mail, Proton Mail, Amazon WorkMail / SES and 25 more). When the MX points to a security gateway it is taken from the SPF include for Google, Microsoft, Zoho, Proton, Fastmail or Amazon SES if present. "Other" = MX present but not recognised; null = no MX, or a gateway with no recognisable SPF include. |
| `mailGateway` | string | Email security gateway in front of the mailboxes, recognised from the MX hosts (Mimecast, Proofpoint, Broadcom Email Security.cloud, Barracuda, Cisco Secure Email and others); null when none. |
| `dnsNameservers` | array | NS records answered by DNS for the domain, sorted; can differ from the registry list during a DNS migration. |
| `dnsProvider` | string | Managed DNS provider recognised from the NS hosts (Cloudflare, Amazon Route 53, Google Cloud DNS, Azure DNS, GoDaddy, Namecheap and others); "Other" when not recognised. |
| `spfRecord` | string | The v=spf1 TXT record of the domain; null when absent or DNS not run. |
| `spfPolicy` | string | The final all mechanism of the SPF record: -all, ~all, ?all or +all, or redirect when the record delegates with redirect=. |
| `dmarcRecord` | string | The v=DMARC1 TXT record at _dmarc.<domain>; null when absent or DNS not run. |
| `dmarcPolicy` | string | The p= tag of the DMARC record: none, quarantine or reject. |
| `dkimSelectors` | array | Which of the common selectors google, selector1, selector2, k1, s1, s2, default, dkim and mail publish a DKIM key. An empty list does not prove the domain has no DKIM: custom selectors cannot be listed. |
| `hostingIp` | string | The IPv4 address used for the hosting lookup (first A record in sorted order). |
| `hostingAsn` | integer | Autonomous system number announcing hostingIp (Team Cymru IP-to-ASN service). |
| `hostingAsnName` | string | Registered name of that autonomous system, e.g. "CLOUDFLARENET - Cloudflare, Inc., US". |
| `hostingCountry` | string | Country code of the announcing network prefix. |
| `rdapServer` | string | Base URL of the RDAP server that answered. |
| `rdapSource` | string | How the server was chosen: iana-bootstrap (IANA RDAP bootstrap file), registry-unlisted (official registry RDAP server not yet in the IANA file: .io .sh .ac .me .us .ch .li), rdap.org (fallback used only when the IANA file is unreachable). |
| `sourceUrl` | string | RDAP URL of the domain record. |
| `scrapedAt` | string | Time of the lookup, ISO 8601 UTC. |

Sample record:

```json
{
  "input": "https://www.wikipedia.org/wiki/Domain",
  "domain": "wikipedia.org",
  "tld": "org",
  "found": true,
  "registered": true,
  "reason": null,
  "registrar": "MarkMonitor Inc.",
  "registrarIanaId": 292,
  "registrarAbuseEmail": "abusecomplaints@markmonitor.com",
  "createdAt": "2001-01-13T00:12:14.754Z",
  "updatedAt": "2026-08-12T08:47:19.410Z",
  "expiresAt": "2027-01-13T00:12:14.000Z",
  "domainAgeDays": 9391,
  "daysToExpiry": 104,
  "status": [
    "clientDeleteProhibited",
    "clientTransferProhibited",
    "clientUpdateProhibited"
  ],
  "transferLocked": true,
  "deletionPending": false,
  "nameservers": [
    "ns0.wikimedia.org",
    "ns1.wikimedia.org",
    "ns2.wikimedia.org"
  ],
  "dnssec": false,
  "registrantOrganization": "Wikimedia Foundation, Inc.",
  "registrantCountry": "US",
  "registrantRedacted": false,
  "registrarRdap": "ok",
  "dnsStatus": "ok",
  "aRecords": [
    "103.102.166.224"
  ],
  "aaaaRecords": [
    "2001:df2:e500:ed1a::1"
  ],
  "mxRecords": [
    "mx-in1001.wikimedia.org",
    "mx-in2001.wikimedia.org"
  ],
  "mailProvider": "Google Workspace",
  "mailGateway": "Proofpoint",
  "dnsNameservers": [
    "ns0.wikimedia.org",
    "ns1.wikimedia.org",
    "ns2.wikimedia.org"
  ],
  "dnsProvider": "Cloudflare",
  "spfRecord": "v=spf1 include:_spf.google.com ~all",
  "spfPolicy": "~all",
  "dmarcRecord": "v=DMARC1; p=reject; rua=mailto:dmarc-rua@wikimedia.org;",
  "dmarcPolicy": "reject",
  "dkimSelectors": [
    "google"
  ],
  "hostingIp": "103.102.166.224",
  "hostingAsn": 14907,
  "hostingAsnName": "WIKIMEDIA - Wikimedia Foundation Inc., US",
  "hostingCountry": "US",
  "rdapServer": "https://rdap.publicinterestregistry.org/rdap/",
  "rdapSource": "iana-bootstrap",
  "sourceUrl": "https://rdap.publicinterestregistry.org/rdap/domain/wikipedia.org",
  "scrapedAt": "2026-10-01T08:00:00.000Z"
}
```

## Call it from code

Runnable examples are in [`examples/`](examples). Replace `YOUR_APIFY_TOKEN` with the token from your Apify account settings.

```bash
curl -X POST "https://api.apify.com/v2/acts/datagrit~domain-whois-rdap-lookup/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"domains":["stripe.com","shopify.com","atlassian.com","nature.com","wikipedia.org","mozilla.org","bbc.co.uk","lemonde.fr","web.dev","google.io","google.us","zzqx-nonexist-8841.com"]}'
```


## More from datagrit

- [Website Tech Stack Lookup - Technology Detector](https://github.com/getdatagrit/website-tech-stack-lookup) - Detect the technology stack of any list of domains: CMS, ecommerce, analytics, CDN, frameworks with versions, plus mail provider, SPF and DMARC.
- [TED Contract Expiry Radar - Recompete Leads](https://github.com/getdatagrit/ted-contract-expiry-radar) - Find EU public contracts approaching expiry from TED award notices: incumbent, buyer, value, end date and renewal options.
- [UK Contract Expiry Radar - Recompete Leads](https://github.com/getdatagrit/uk-contract-expiry-radar) - UK public contracts ending soon with incumbent supplier, buyer, value and contact - recompete leads from Contracts Finder award notices.
- [French Company Finder - Sirene Financials](https://github.com/getdatagrit/french-company-finder) - French company lead lists from Sirene screened by net result and revenue, with net margin, size, matching establishment and optional directors.
- [IRS 990 Nonprofit Officers and Compensation](https://github.com/getdatagrit/irs-990-officer-compensation) - Named officers, directors and key employees with pay, hours and titles from IRS e-filed 990, 990-EZ and 990-PF returns.

All Actors: [https://getdatagrit.github.io/](https://getdatagrit.github.io/) · [Apify Store](https://apify.com/datagrit)

---

This repository holds documentation and usage examples. Questions, bug reports and feature requests: use the **Issues** tab of the Actor page on [Apify Store](https://apify.com/datagrit/domain-whois-rdap-lookup). Examples are MIT licensed.
