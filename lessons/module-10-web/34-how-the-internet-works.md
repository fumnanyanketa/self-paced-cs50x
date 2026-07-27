# Module 10 · Lesson 34: How the Internet Works

> **Course:** Self-Paced CS50x
> **Module 10:** The web: from packets to pages people can use
> **Speaker:** David J. Malan, Harvard University
> **Source talk:** [CS50x 2026 - Lecture 8 - HTML, CSS, JavaScript](https://www.youtube.com/watch?v=yYst7puZXjw) · [full transcript](../../transcripts/11-lecture-8-html-css-javascript.txt)
> **Estimated time:** 45-60 minutes (read plus exercises)

---

## In one sentence

Every time you load a web page, four unglamorous protocols quietly cooperate: DHCP hands your device an address the moment it boots, DNS translates a name you can remember into a number a computer can route, IP gets a packet from your machine to the right one on Earth, and TCP slices big files into numbered, guaranteed-to-arrive pieces, and once you can name what each one contributes, "the internet" stops being magic and starts being a system you can trace by hand.

> 🎯 **Where this lesson is heading.** It builds to a hands-on **Capstone Project** where you run real lookups from your own codespace and sketch the full labeled journey of one packet from you to harvard.edu. Everything before the Capstone teaches the pieces you'll be labeling. If you want to see the finish line first, jump to the **"Capstone Project"** section, then come back.

## First-principles companion

> 💡 **The durable idea behind this lesson.** Browsers and codespaces will change; the addressing scheme underneath them will not.
>
> - **[RFC 791: Internet Protocol](https://www.rfc-editor.org/rfc/rfc791)** (DARPA/IETF, September 1981). This is the actual specification behind the "arcane diagram" of a 32-bit IP datagram Malan puts on screen: the formal, timeless definition of what goes on the outside of every packet's envelope, independent of any browser, language, or decade.

## A few plain-language basics first

This lesson uses some everyday terms. Here they are in plain words:

- **Network:** a group of computers connected so they can exchange information, whether by wires or wirelessly.
- **Router:** a computer whose only job is to forward data toward its destination, deciding, packet by packet, which wire or connection to send it out on next.
- **Protocol:** an agreed-upon set of rules for how to communicate, so that two computers (or two people) know what to expect from each other. A handshake between two strangers is a human protocol; TCP/IP is a computer one.
- **IP address:** a numeric address assigned to a device so it can be uniquely found on a network, the way a street address uniquely locates a building.
- **Packet:** a small chunk of data traveling across a network, wrapped with addressing information the way a letter is wrapped in an envelope. (Also called a datagram.)
- **Port number:** a number written alongside an IP address that identifies *which service* on that computer a packet is meant for (a web page, versus email, versus a video call).
- **Domain name / DNS:** a domain name is the human-friendly name for a website (like `harvard.edu`); DNS (Domain Name System) is the service that translates that name into the IP address computers actually need.
- **DHCP:** the service that automatically hands a device its IP address (and other settings) the moment it joins a network, so no human has to type any of it in by hand.

You do not need to memorise these. Each is explained again the first time it matters.

## Why this lesson matters

Every problem set you've written so far has lived entirely inside one machine: a black-and-white terminal window, text in, text out. As Malan puts it at the start of this lecture, that's about to change: **"the apps that you and I are using like every day are in the form of a web browser and on our phone."** Starting today, your code has to leave the building. It has to travel across wires and radio waves, find a specific computer among billions, and get an answer back, reliably, without you or the user ever thinking about it. This lesson is the "how" underneath that trust. Once you can explain what DHCP, DNS, IP, and TCP each contribute, you'll never look at a URL, a loading spinner, or a "can't reach this page" error the same way again, and by the time your own final project is live on the internet, every one of these protocols will be quietly carrying real visitors' requests to it.

## Learning objectives

By the end of this lesson you will be able to:

1. Explain what a network, a router, and a protocol are, and summarize how ARPANET became today's internet.
2. Do the bit-math behind an IPv4 address (why it's 32 bits, why that caps the internet at about 4 billion addresses) and explain why IPv6 exists.
3. Describe what lives "on the outside of the envelope" of a packet (source/destination IP addresses and port numbers) and explain how TCP fragments large files and guarantees they arrive intact.
4. Explain how DNS turns a domain name into an IP address through a hierarchical, cached, recursive lookup, and what a registrar does.
5. Explain what DHCP configures automatically the moment a device joins a network, and why that used to be done by hand.

## Prerequisites

- **Module 1 · Lesson 2: Bits and Binary**: you'll reuse the exact same place-value math (8 bits → 256 values) to understand why an IPv4 address is 32 bits, and the "everything is bits in an envelope" framing carries straight through.
- **Module 0: Pre-flight**: a working cs50.dev codespace, since the Capstone runs real lookup commands in its terminal.
- No prior networking knowledge assumed. (Module 9's AI lessons are not required background for this one: this lesson simply follows next in the course sequence.)

---

## Part 1: From a black terminal to a browser near you

Every program you've written up to now, in Scratch, C, or Python, ran and stayed on one machine: your own codespace, printing to your own terminal. Malan opens this lecture by naming the shift that's about to happen:

> "up until now, of course, in so many of our problem sets like we've been writing command line code like a black and white terminal window and everything is very keyboard based, very textual, but of course like the apps that you and I are using like every day are in the form of a web browser and on our phone." (David Malan)

To make that shift, you first need to understand the thing your code is about to live on: the internet. In the simplest terms, Malan defines the building block underneath it:

> "networks are interconnections of computers, whether with wires or wirelessly." (David Malan)

You already have a network at home, one on this campus, one at a company. As soon as you start connecting *networks* to other networks, you get, in effect, a network of networks: the internet. It didn't start out global. Rewind to 1969:

> "really something known as ARPANET for the Advanced Research Projects Agency, a project from the Department of Defense that was really designed to interconnect what limited supercomputers we had." (David Malan)

ARPANET began as just a handful of nodes, UCLA and a few others, with Harvard and MIT joining within about a year. Today's internet is the same idea at planetary scale, held together by devices called **routers**, whose entire job is to forward data toward its destination, one hop at a time, in whichever direction gets it closer.

To make that concrete, Malan's teaching fellows performed a live "packet-routing" skit over Zoom: each person played a router, passing along **packets**, chunks of data Malan describes with a physical metaphor:

> "packets of information which metaphorically you can think of as just like a little white envelope like this that we use to send things via snail mail via the US Postal Service or beyond that internationally." (David Malan)

The point of the skit wasn't that there was one correct path from sender to receiver. There wasn't. As Malan notes, a packet "could have gone up and then to the left. It could have gone left and then up. It could have zigzagged", and that's genuinely how the real internet behaves: a packet's path depends on which wires and wireless links happen to be available and how routers are configured that moment, not on some single fixed route.

For any of this coordination to work, every router and device has to speak the same language: a **protocol**, which Malan grounds in something you already do every day:

> "when I meet someone for the first time, I very often instinctively sort of extend my hand just sort of hoping that they too will extend their hand and shake." (David Malan)

That handshake works because both people silently agreed in advance on the rule. Computers need the exact same kind of agreement, just expressed in bits instead of body language, and the specific agreement nearly everything on the internet uses is a pair of protocols called **TCP/IP**, defined as **"a set of conventions that governs how computers behave on the internet."**

> 🔑 **The internet is just networks of networks, moved by routers that agree on a shared protocol.** There is no single correct path a packet must take: only a shared set of rules every router along whatever path it does take has to honor.

---

## Part 2: IP (giving every device on Earth a unique address)

TCP/IP is actually two different protocols solving two different problems. Start with the second half of that name, IP:

> "IP, short for Internet Protocol, is simply a protocol that decides to give all of us a unique address in the world." (David Malan)

Just as Memorial Hall has a street address (45 Quincy Street, Cambridge, MA 02138), every device on the internet (a Mac, a phone, a server) gets a numeric **IP address**. You've seen the format: four numbers separated by dots, like `1.2.3.4`, formally called **dotted decimal notation**.

Here's where Lesson 2's bit-counting comes back. Each of those four numbers ranges from 0 to 255: 256 total possibilities. From Lesson 2 you already know 256 = 2⁸, so each number takes **8 bits**. Four numbers × 8 bits each gives:

```text
   4 numbers  ×  8 bits each  =  32 bits total (an IPv4 address)

   2^32 possible values ≈ 4.3 billion unique addresses
```

Four billion sounds enormous, until you remember that most people in the room own at least two internet-connected devices, and the "internet of things" adds appliances, doorbells, and light bulbs to the count. That ceiling is exactly why the world is gradually moving to **IPv6**, which uses 128 bits instead of 32:

> "IP addresses are 32 bits, little trivia that's germane only insofar as it does kind of limit how many total devices we could seem to have in the world." (David Malan)

128 bits gives vastly more addresses than 32 (enough, as Malan puts it, "for the foreseeable future"), but the transition from IPv4 to IPv6 has been underway for decades and is still only partly complete, which is why this course (like most teaching material) still uses IPv4 addresses for simplicity.

Every packet's "envelope" carries, among other bits, a source IP address and a destination IP address. If Phyllis (`5.6.7.8`) is sending something to Brian (`1.2.3.4`), she writes his address as the destination and her own as the return address, exactly like a piece of physical mail:

```text
 ┌── OUTSIDE OF THE ENVELOPE ─────────────────────┐
 │  To:    1.2.3.4     (Brian's IP address)       │
 │  From:  5.6.7.8     (Phyllis's IP address)     │
 ├─────────────────────────────────────────────────┤
 │  [ contents of the envelope, sealed inside ]    │
 └─────────────────────────────────────────────────┘
```

> 🔑 **IP's entire job is uniquely addressing computers, nothing more.** It does not promise the data will arrive, and it says nothing about *what kind* of data is inside. Solving those two problems is TCP's job, next.

---

## Part 3: TCP (port numbers and guaranteed delivery)

A single server can do far more than one thing at once: serve email, host a video call, run a game, and serve web pages, all at the same address. IP alone can't tell those apart: it only gets a packet to the right *computer*, not the right *service on* that computer. That's the problem TCP solves, using **port numbers**:

> "TCP allows a computer to distinguish whether it has received a packet that's an email or receive a packet that's a chat message or a piece of a video conference or the like." (David Malan)

Port numbers are small, standardized values written on the outside of the envelope alongside the IP addresses. Two you'll use constantly:

| Port | Meaning |
|---|---|
| 80 | Plain HTTP (an unencrypted request for a web page) |
| 443 | HTTPS (an encrypted, secure request for a web page, the `S` in the URL) |

So when your browser requests `https://www.harvard.edu`, unbeknownst to you it writes Harvard's IP address *and* the number 443 on the outside of the envelope: telling Harvard's server, in effect, "this is a request for a secure web page, not an email." Phyllis also writes her own IP address *and* a port number of her own in the return-address corner, so Brian's reply reaches the right browser tab even if she has several tabs and apps open at once.

TCP solves a second problem too: reliability over long distances and large files. Suppose Phyllis wants to send a large image, say, a big, happy cat JPEG. Sending it as one giant envelope would hog the connection and prevent anyone else from using the internet at that moment. So:

> "at the risk of a bit of heresy, we can actually tear this cat in half and fragment it really." (David Malan)

TCP breaks a large file into multiple packets, each carrying part of the data plus a **sequence number**, a label like "piece 1 of 4," "piece 2 of 4," and so on. When packets arrive, possibly out of order (remember, each one may have taken a different path through the network), the receiving computer uses those sequence numbers to check whether anything is missing and to reassemble the pieces in the right order. If some are missing, the receiver can ask the sender to resend just those pieces, which is exactly what "guaranteed delivery" means here:

> "TCP guarantees delivery by just doing some bookkeeping on the outside of these envelopes." (David Malan)

Put together: **IP** gets a packet to the right computer; **TCP** gets it to the right service on that computer (via a port number), breaks large data into numbered pieces, and makes sure every piece actually arrives.

> ✅ **What to do about it:** whenever you see `https://` in a URL, you can now translate it in your head: "this connection is quietly using port 443, and whatever comes back will arrive complete, even if it had to travel in pieces."

---

## Part 4: DNS (trading numbers for names)

Nobody wants to type `1.2.3.4` into a browser to visit a website. Instead you type `harvard.edu` or `google.com`, a **domain name**. Something has to translate that name into the IP address computers actually need, and that something is **DNS**:

> "there's another acronym in the world and there's another technology used on the internet, namely DNS for domain name system, and this is just a certain type of server that every home has, even if you didn't know it. Every campus has, every company has." (David Malan)

Under the hood, a DNS server is essentially a giant two-column lookup table: domain names in one column, matching IP addresses in the other. When your device tries to reach `harvard.edu` for the first time since booting up, it doesn't already know Harvard's IP address (nobody pre-installs billions of IP addresses onto your phone), so it asks a nearby DNS server the question for you.

Where do domain names themselves come from? You rent them:

> "You can go to any number of what are called internet registrars and pay them some money, and it's essentially on a rental basis, so you rent a domain name for a year or maybe 3 or 5 years at a time." (David Malan)

Whoever rents a domain then configures some DNS server, somewhere, to know the IP address of the server that will host that domain's website.

DNS is deliberately **hierarchical**. Somewhere out in the world sit **root servers**:

> "there is out there somewhere these so-called root servers that essentially know what the IP addresses are of all of the dot-coms, for instance, or all of the dot EDUs or the like." (David Malan)

But your own computer doesn't ask a root server first: it's far more efficient to ask the *local* network. At home, that's the DNS server built into your home router; on campus, it's Harvard's own DNS server. If that local server already knows the answer (because someone else recently asked the same question), it just replies immediately. If it doesn't know, the question escalates upward:

> "this whole design is recursive, to borrow a term from a few weeks ago, in that if my computer doesn't know the answer... it eventually gets escalated to those so-called root servers, but then cached (that is, remembered) by all of these other DNS servers along the way." (David Malan)

Here's the whole lookup chain, sketched out:

```text
 You type: https://www.harvard.edu

 1. Your device        --  "What's the IP address for www.harvard.edu?"
        │
        ▼
 2. Local DNS server    --  (home router, or Harvard's own campus server)
        │  Already knows? → answers immediately (it was cached from an earlier lookup)
        │  Doesn't know?
        ▼
 3. Root server         --  knows which servers handle all the .edu domains
        │
        ▼
 4. Answer flows back down the same chain, and every server along
    the way CACHES it, so the next lookup for www.harvard.edu is instant
        │
        ▼
 5. Your device writes 1.2.3.4 on the outside of its envelope,
    and the IP/TCP conversation from Parts 2-3 can finally begin
```

The whole system is, in Malan's summary, satisfyingly unglamorous:

> "It's a big cheat sheet of domain names to IP addresses and the server is responding for us." (David Malan)

> 💡 **Nuance:** caching is why DNS mostly feels instant. The very first time anyone nearby visits a brand-new domain, there may be a slightly longer pause while the answer gets escalated up the chain; every lookup after that, from you or your neighbors, is served from a nearby cache instead.

---

## Part 5: DHCP (how your device learns the rules the moment it boots)

Everything so far assumes your own device already knows several things: its own IP address, the IP address of a DNS server to ask, and the IP address of the router to hand packets off to. Where does *that* information come from? One more acronym: **DHCP**, Dynamic Host Configuration Protocol.

> "How do I know what my Mac IP address should be? How do I know what my phone's IP address should be? How do I know what the IP address is of the DNS server of whom I should be asking any of these questions? ... DHCP is the solution to all of those problems." (David Malan)

It wasn't always automatic. Malan recalls a time before DHCP existed, when people had to type in their own IP address, DNS server, and router address by hand, based on numbers someone else told them. Today, the moment you boot up a laptop or phone and join a network, your device does this instead:

> "it essentially broadcasts a message like Hello world, what's my IP address?" (David Malan)

Somewhere on that local network (wired or wireless, at home, on campus, or in a company), a DHCP server is listening for exactly that broadcast, and answers it:

> "DHCP server on that local network wired or wirelessly that will respond based on how Harvard or Comcast or Verizon or someone at home has configured it to tell you what your device's IP address is, what the IP is of your local router, what the IP address is or are of your DNS servers, and the like." (David Malan)

In one broadcast-and-reply exchange, DHCP hands your device everything Parts 2 through 4 assumed it already had: its own IP address, the router's address (where to send outbound packets), and the DNS server's address (who to ask for domain-name lookups). That's why plugging in an ethernet cable or joining Wi-Fi "just works" today, with no manual configuration at all. As Malan puts it, with evident appreciation for a problem you'll never have to think about again:

> 💡 **"Dynamic host configuration protocol didn't always exist. Wonderful that it now does."** (David Malan)

---

## Part 6: Putting it all together (the journey of one packet)

Every piece from Parts 1-5 fires in a specific order, every single time you load a page. Here's the whole trip, end to end:

```text
 STEP 0: BOOT UP
   Your laptop joins Wi-Fi.
   DHCP broadcasts "hello, what's my IP?" and gets back:
     - this device's own IP address
     - the local router's IP address
     - a DNS server's IP address

 STEP 1: RESOLVE THE NAME
   You type https://www.harvard.edu into your browser.
   DNS is asked "what's the IP for www.harvard.edu?":
   the local DNS server answers (cached) or escalates to a root server.
   Result: an IP address, e.g. 1.2.3.4

 STEP 2: ADDRESS THE ENVELOPE
   Your device builds a packet:
     destination IP   = 1.2.3.4        (Harvard's server, from DNS)
     destination port = 443             (HTTPS, because of the "s")
     source IP        = your own address   (from DHCP)
     source port       = a number just for this browser tab

 STEP 3: SLICE AND SEND (TCP)
   If there's a lot of data, TCP breaks it into numbered pieces
   ("1 of 4," "2 of 4," ...) so no single transfer hogs the network.

 STEP 4: ROUTE IT (IP + routers)
   Each packet hops router to router, not necessarily the same path
   as the packet before or after it, until it reaches 1.2.3.4.

 STEP 5: REASSEMBLE AND REPLY
   Harvard's server checks the sequence numbers, reassembles the
   pieces, and sends a reply addressed back to your IP and port.
   TCP on your end confirms nothing is missing; if it is, it asks
   for a resend.
```

> 🔑 **Four protocols, four separate jobs.** DHCP gets your device its own identity on the network. DNS turns a name into an address. IP gets a packet to the right computer. TCP gets it to the right service on that computer and guarantees every piece arrives. None of the four can substitute for another: each solves exactly one part of the problem.

---

## Key takeaways

1. **The internet is a network of networks**, held together by routers that all agree on the same protocol (a shared set of communication rules): TCP/IP.
2. **An IPv4 address is 32 bits**: four numbers from 0-255 (each 8 bits), giving about 4.3 billion possible addresses, which is why the world is gradually adopting 128-bit IPv6.
3. **TCP adds port numbers and guaranteed delivery on top of IP.** Port numbers say *which service* a packet is for (80 for HTTP, 443 for HTTPS); sequence numbers let TCP fragment large files and confirm every piece arrived.
4. **DNS is a hierarchical, cached, recursive lookup** that turns a domain name into an IP address: your local network is asked first, and only unanswered questions escalate up toward root servers.
5. **DHCP is what lets a device configure itself automatically** the moment it joins a network, handing out its own IP address, the router's address, and a DNS server's address, all in one broadcast-and-reply exchange.
6. **A packet is just a structured chunk of bytes in an envelope**, the same "everything is bits, arranged by agreement" idea from Lesson 2, just now with fields for addresses, ports, and sequence numbers instead of ASCII or RGB.

## Common pitfalls

- ❌ Assuming a packet takes one fixed, predictable path from sender to receiver. Fix: remember the routing skit. Each packet may take a different route, and that's fine, because TCP checks that all the pieces eventually arrive.
- ❌ Confusing IP and TCP as the same thing. Fix: IP addresses the *computer*; TCP addresses the *service on that computer* (via ports) and guarantees delivery. They solve different problems and always travel together.
- ❌ Thinking DNS lookups always take the same amount of time. Fix: a brand-new domain may need to escalate all the way to a root server; anything recently looked up nearby is answered instantly from a cache.
- ❌ Forgetting that DHCP hands out more than just an IP address. Fix: it also configures your device's router address and DNS server address, three settings in one exchange, not one.
- ❌ Treating "IPv4 vs. IPv6" as ancient history that's already finished. Fix: as Malan notes, the transition has been "in motion" for 20-30 years and still isn't complete: IPv4 is still what you'll mostly see and use.

---

## 🛠️ Capstone Project: Trace a packet's journey to Harvard

> This is the main hands-on project for the lesson. Using only free, standard commands already available on cs50.dev, you'll look up real IP addresses and then sketch, by hand, the complete labeled journey of one packet from your codespace to harvard.edu, naming DHCP, DNS, IP, TCP, and ports at every hop. When you eventually host your own final project, this exact journey is what every visitor's request will take to reach it.

### What you will build

A short lookup log from your own cs50.dev terminal, plus a labeled text diagram (in a plain `.txt` or `.md` file) tracing one packet's full round trip. Its pieces:

- Real IP addresses for several domains, obtained with `nslookup` or `host`.
- A short written observation about what those results tell you about DNS.
- A complete, labeled diagram of one request's journey, naming every protocol from this lesson at the point where it acts.

### Why this is the perfect practice

| Lesson idea | Where you use it in the capstone |
|---|---|
| DNS resolves names to IPs (Part 4) | Milestone 1: you resolve real domains yourself |
| DNS caching and hierarchy (Part 4) | Milestone 2: you look for evidence of it |
| IP addresses and dotted decimal (Part 2) | Milestone 3: you label the diagram's IP fields |
| TCP ports and sequencing (Part 3) | Milestone 3: you label the diagram's port/TCP fields |
| DHCP assigns identity at boot (Part 5) | Milestone 3: you label where DHCP already did its job |

### Milestones (build them in order, each one works on its own)

1. **Resolve real domains.** In your cs50.dev terminal, run `nslookup harvard.edu` (or `host harvard.edu` if you prefer). Do the same for at least two more domains of your choosing, for example `cs50.dev` and `wikipedia.org`. Write down each domain's resolved IPv4 address(es) in a short log.
2. **Look for the hierarchy and caching in action.** Run `nslookup` on the *same* domain a second time and compare the response time or output to the first lookup. Note anything different (some domains return several IP addresses at once: that's normal, since one domain name can point to a cluster of servers, exactly as Malan describes for `www`).
3. **Sketch the full journey of one packet.** In a text file, draw a labeled, step-by-step diagram (using the Part 6 diagram as a model, not to copy verbatim) of what happens when your codespace requests `https://www.harvard.edu`, starting from "device already has an IP from DHCP" through DNS resolution, envelope addressing (destination IP + port 443, your IP + a port), TCP fragmentation if relevant, and the reply coming back. Every arrow in your diagram should be labeled with which protocol (DHCP, DNS, IP, or TCP) is responsible for that step.
4. **Confirm the port reasoning.** For each domain you looked up in Milestone 1, write one sentence stating which port a browser would use to reach it over HTTPS, and why (this should just be "443," reasoned from Part 3; the goal is fluency, not new information).
5. **Stretch goals.** Run `nslookup` on a domain you're confident doesn't exist (like `thisdomaindoesnotexist12345.com`) and note how the failure looks different from a successful lookup. Or, run `nslookup` on the *same* domain from two different networks (e.g., your codespace vs. your phone's hotspot) and compare whether you get the same IP address back.

### How you will know you are done

- ✅ You have real, resolved IPv4 addresses for at least three different domains, obtained with `nslookup` or `host`.
- ✅ You can point to your own lookup log and explain, out loud, which part was DNS doing its job.
- ✅ Your packet-journey diagram names DHCP, DNS, IP, TCP, and at least one port number, each at the specific step where it acts.
- ✅ You can explain, in one sentence, why two lookups of the same domain might return different response times.

> 💡 **Keep yourself honest:** don't just describe the journey from memory: run the actual `nslookup` commands first and build your diagram from what you genuinely saw on screen, the same way Malan pulled up real headers with `curl` rather than just describing them.

---

## Practice exercises (optional extra reps)

> **What these are:** small, self-contained tasks, each giving focused practice on one idea. Optional and independent; the Capstone already touches all of them, so feel free to skip straight to it.

### Exercise 1: The IPv4 ceiling, by hand (foundational)
Without a calculator, confirm that an IPv4 address is 32 bits: four numbers, each ranging 0-255. Using the place-value technique from Lesson 2 (place values 128, 64, 32, 16, 8, 4, 2, 1), convert the number 200 into 8-bit binary by hand. Then explain, in one sentence, why 2³² addresses is a hard ceiling rather than just a rough estimate.

### Exercise 2: Read an envelope (intermediate)
Given this packet summary: destination IP `192.0.2.10`, destination port `443`, source IP `192.0.2.55`, source port `52104`, sequence `2 of 3`, write one sentence each explaining what IP contributed to this envelope, what TCP contributed, and what would happen if packet "1 of 3" never arrived.

### Exercise 3: Trace the hierarchy from memory (advanced)
Without rereading Part 4, write out the full DNS lookup chain for a domain your device has never visited before, in order, naming every stop (your device, local DNS server, root server) and explaining what gets cached and where. Then check your answer against Part 4's diagram and note anything you got wrong or left out.

---

## Cheat sheet

```text
THE FOUR PROTOCOLS, ONE JOB EACH
  DHCP  -- hands your device its IP, router IP, and DNS server IP, at boot
  DNS   -- translates a domain name (harvard.edu) into an IP address
  IP    -- gets a packet to the right COMPUTER (via IP address)
  TCP   -- gets a packet to the right SERVICE on that computer (via a port),
           fragments large data into numbered pieces, and guarantees delivery

IPv4 ADDRESS MATH
  4 numbers, each 0-255 (= 2^8 = 8 bits)  ->  4 x 8 = 32 bits total
  2^32 =~ 4.3 billion possible addresses
  IPv6 uses 128 bits instead -- vastly more addresses, still rolling out

COMMON PORTS
  80  = HTTP  (plain, unencrypted web request)
  443 = HTTPS (encrypted web request -- the "s" in https://)

DNS LOOKUP ORDER (recursive + cached)
  your device -> local DNS server (cached? answer now)
             -> [if unknown] root server -> answer flows back, gets cached

USEFUL COMMANDS (free, built into cs50.dev)
  nslookup harvard.edu     -- ask DNS for a domain's IP address
  host harvard.edu         -- same idea, different tool

PACKET = STRUCTURED BYTES IN AN ENVELOPE
  outside: destination IP + port, source IP + port, sequence number
  inside:  the actual data (or one numbered fragment of it)
```

## How this connects to the rest of the course

- **Earlier, Module 1 · Lesson 2 ("Bits and Binary"):** you learned that everything a computer stores is bits arranged by agreement: ASCII bytes, RGB bytes. This lesson's packets are the exact same idea: structured bytes in an envelope, just with fields for addresses, ports, and sequence numbers instead of characters or colors.
- **Immediately before, Module 9 · Lesson 33 ("How machines learn"):** a different topic in the same course, and the last lesson before this module's shift to the web.
- **Next, Module 10 · Lesson 35 ("HTTP and the browser"):** you'll pick up exactly where this lesson's envelopes leave off: what actually goes *inside* them when you request a web page, using the port 80/443 distinction from Part 3 as your starting point.
- **Later, Module 11 (Flask web apps):** the server you build and host yourself will sit on the receiving end of exactly this DHCP → DNS → IP → TCP journey, for every single visitor.

---

*Source: "CS50x 2026 - Lecture 8 - HTML, CSS, JavaScript" by David J. Malan, Harvard University. Code snippets and diagrams are illustrative reconstructions of the patterns described in the talk. Adapt them to the current SDK.*
