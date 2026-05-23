# DNS — Domain Name System

> **Tags:** `networking` `dns` `records` `resolution` `dnssec` `cdn`
> **Level:** Intermediate | **Prerequisite:** `networking/01-http-networking.md`

---

## 1. How DNS Resolution Works

```
Browser types: www.example.com

Step 1: Browser DNS cache (0ms)
  → Chrome caches DNS records (chrome://net-internals/#dns)

Step 2: OS cache + /etc/hosts (0ms)
  → /etc/hosts file is checked first
  → OS has its own resolver cache

Step 3: Recursive Resolver (your ISP or 8.8.8.8, 1.1.1.1)
  → "I'll find the answer for you"
  → Starts the recursive lookup if not cached

Step 4: Root Name Servers (13 logical servers, globally distributed)
  → Resolver asks: "Who handles .com?"
  → Response: "The .com TLD servers at these IPs"

Step 5: TLD Name Servers (.com, .org, .io, etc.)
  → Resolver asks: "Who handles example.com?"
  → Response: "The authoritative servers for example.com"

Step 6: Authoritative Name Server (e.g., ns1.example.com)
  → Resolver asks: "What is www.example.com?"
  → Response: "93.184.216.34" with TTL

Step 7: Resolver returns answer to client, caches it for TTL duration

Total time: ~50-200ms for uncached, <1ms from cache
```

---

## 2. DNS Record Types

```bash
# A Record — IPv4 address
example.com.        3600  IN  A       93.184.216.34
www.example.com.    3600  IN  A       93.184.216.34

# AAAA Record — IPv6 address
example.com.        3600  IN  AAAA    2606:2800:220:1:248:1893:25c8:1946

# CNAME — Canonical Name (alias to another hostname)
www.example.com.    3600  IN  CNAME   example.com.
blog.example.com.   3600  IN  CNAME   myblog.wordpress.com.

# CNAME rules:
# ❌ Cannot CNAME the apex domain (example.com itself) — breaks MX, NS
# ✅ Use ALIAS/ANAME record for apex (Cloudflare's flattening)

# MX — Mail Exchange (where to send email)
example.com.  3600  IN  MX  10  mail1.example.com.  # Priority 10
example.com.  3600  IN  MX  20  mail2.example.com.  # Priority 20 (backup)

# TXT — Text records (verification, SPF, DKIM, DMARC)
example.com.  IN  TXT  "v=spf1 include:_spf.google.com ~all"
_dmarc.example.com. IN TXT "v=DMARC1; p=quarantine; rua=mailto:dmarc@example.com"

# SPF = who can send email for this domain (anti-spam)
# DKIM = cryptographic signature for email
# DMARC = policy for failed SPF/DKIM

# NS — Name Servers (authoritative for this domain)
example.com.  IN  NS  ns1.cloudflare.com.
example.com.  IN  NS  ns2.cloudflare.com.

# SOA — Start of Authority (zone info)
example.com.  IN  SOA  ns1.cloudflare.com. admin.example.com. (
              2024011501  ; Serial (date + increment)
              7200        ; Refresh
              3600        ; Retry
              604800      ; Expire
              300         ; Minimum TTL
)

# SRV — Service records (used by SIP, XMPP, Minecraft)
_http._tcp.example.com.  IN  SRV  10 5 80 www.example.com.
# Priority Weight Port Target

# PTR — Reverse DNS (IP → hostname)
34.216.184.93.in-addr.arpa.  IN  PTR  example.com.

# CAA — Certificate Authority Authorization (restrict who can issue SSL)
example.com.  IN  CAA  0 issue "letsencrypt.org"
example.com.  IN  CAA  0 issuewild ";"  # Don't issue wildcard certs

# TLSA — DNS-based Authentication of Named Entities (DANE)
_443._tcp.example.com.  IN  TLSA  3 1 1  <certificate-hash>
```

---

## 3. TTL Strategy

```
TTL (Time To Live) = how long resolvers cache the record (in seconds)

Low TTL (60-300s):
  + Fast propagation when you change records
  + Good for planned migrations
  - More DNS queries (higher load on your DNS provider)
  - Use before major changes!

High TTL (3600-86400s):
  + Fewer DNS queries (better performance)
  + More resilient to DNS provider outage
  - Slow propagation when you need to change records
  - Use for stable, long-lived records

Best Practice:
  Normal operation:   TTL = 3600 (1 hour)
  Before migration:   Lower TTL to 300 (5 min) 24-48 hours ahead
  During migration:   Change records, wait for old TTL to expire
  After migration:    Raise TTL back to 3600

DNS propagation ≠ TTL expiry:
  Propagation = time for authoritative changes to reach all resolvers
  Modern DNS: mostly immediate (authoritative servers update immediately)
  "Propagation takes 24-48h" is a myth from the past!
  Reality: if TTL is 300s → fully propagated in 5 minutes
```

---

## 4. Split-Horizon DNS

```
Different DNS answers depending on WHERE the request comes from

Use case: internal services accessible by hostname, different IPs inside vs outside

Example:
  External request for api.example.com → returns 1.2.3.4 (public IP → NAT → server)
  Internal request for api.example.com → returns 10.0.1.10 (private IP, no NAT)

Benefit:
  - Developers can use same hostnames in code for both environments
  - No hairpin NAT issues
  - Internal traffic stays internal (faster, cheaper)

Implementation:
  Cloud: AWS Route53 private hosted zones
  On-prem: Two DNS servers (one internal, one external)
  Kubernetes: CoreDNS handles internal .cluster.local
```

---

## 5. DNS-Based Load Balancing

```bash
# Round-robin DNS — simple, no health checking
www.example.com.  60  IN  A  1.2.3.4
www.example.com.  60  IN  A  1.2.3.5
www.example.com.  60  IN  A  1.2.3.6
# OS/browser shuffles order → distributes traffic

# Geo-based routing (Route53 / Cloudflare)
# US users → us-east1.example.com → 1.2.3.4
# EU users → europe1.example.com → 5.6.7.8
# Asia users → asia1.example.com → 9.10.11.12

# Weighted routing (A/B testing, gradual rollout)
# 90% of traffic → current.example.com
# 10% of traffic → canary.example.com

# Failover routing (health-check based)
# Primary: api.us-east.example.com → check health every 30s
# If unhealthy → automatically serve secondary IP
```

---

## 6. DNSSEC

```
Problem: DNS is unauthenticated by default
  DNS cache poisoning: attacker injects fake records
  "Kaminsky attack" (2008): tricked resolvers into caching bad records

DNSSEC solution: Cryptographic chain of trust
  Each zone signs its records with public key cryptography
  Parent zone signs child zone's public key
  
Chain of trust:
  . (root) → signs .com → signs example.com → signs www.example.com

Record types added:
  RRSIG: Digital signature for each record set
  DNSKEY: Public key used to verify signatures
  DS: Delegation Signer (hash of child zone's key, held in parent)
  NSEC/NSEC3: Proof that a name does NOT exist (prevent negative caching attacks)

DNSSEC deployment:
  ~30% of domains signed
  ~90% of resolvers validate DNSSEC

Check DNSSEC:
  dig +dnssec example.com
  dig +dnssec . DNSKEY    # View root zone keys
```

---

## 7. DNS Tools

```bash
# dig — primary tool (available everywhere)
dig example.com                        # A record
dig example.com A                      # Explicit type
dig example.com MX                     # Mail records
dig example.com NS                     # Name servers
dig example.com TXT                    # TXT records
dig example.com ANY                    # All record types
dig @8.8.8.8 example.com              # Use specific resolver (Google DNS)
dig @1.1.1.1 example.com              # Cloudflare DNS
dig +short example.com                  # Short output (just IPs)
dig +trace example.com                  # Full resolution trace
dig -x 93.184.216.34                   # Reverse DNS (PTR)
dig +dnssec example.com                # DNSSEC info

# nslookup (Windows-friendly, simpler than dig)
nslookup example.com
nslookup example.com 8.8.8.8           # Specific DNS server
nslookup -type=MX example.com

# host — simple (great for scripts)
host example.com
host -t MX example.com

# whois — domain registration info
whois example.com

# Check DNS propagation from multiple locations
# curl "https://dns.google/resolve?name=example.com&type=A"
# Use: https://dnschecker.org|https://whatsmydns.net

# macOS: see DNS cache
sudo dscacheutil -statistics
sudo dscacheutil -flushcache         # Clear DNS cache

# Linux: flush DNS cache
sudo systemd-resolve --flush-caches
sudo resolvectl flush-caches

# Windows:
ipconfig /flushdns
ipconfig /displaydns                  # View cache
```

---

## 8. Common DNS Problems

```
1. "DNS propagation taking forever"
   Cause: Old TTL still being cached by resolvers
   Fix: Wait for TTL to expire, or lower TTL before next change

2. "Resolves on my machine but not others"
   Cause: Different DNS servers, or one has stale cache
   Debug: 
     dig @8.8.8.8 example.com    # What does Google see?
     dig @1.1.1.1 example.com    # What does Cloudflare see?
     dig @$YOUR_DNS example.com  # What does your resolver see?

3. "www.example.com works but example.com doesn't"
   Cause: Missing A/AAAA record for apex domain
   Fix: Add A record for example.com, or use CNAME flattening

4. "Email not delivering"
   Cause: Wrong/missing MX records or SPF/DKIM/DMARC misconfiguration
   Debug: 
     dig example.com MX          # Check MX records
     dig example.com TXT          # Check SPF
     Use: mxtoolbox.com

5. CNAME loop
   Cause: a.example.com CNAME → b.example.com CNAME → a.example.com
   Fix: Find and break the loop

6. SSL/TLS errors after DNS change
   Cause: Certificate doesn't match new hostname
   Fix: Reissue certificate for correct domain
```

---

*Tài liệu liên quan: `networking/01-http-networking.md` | `networking/04-tls-ssl.md` | `cloud/cloudflare.md`*
