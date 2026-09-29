# Source study: "The definitive guide to copywriting for outbound"

- Video: https://www.youtube.com/watch?v=uSTGNHGFOAo (Nick Saraev, about 4 hours)
- Method: I read the full auto-generated English transcript (0:00 to 3:59:10) end to end.
  Get your own copy with `python scripts/get_transcript.py`; the transcript isn't
  redistributed here.
- These notes are my paraphrase, organised by chapter, with timestamps so you can
  check any claim against the video. Items tagged **[guardrail]** are places where
  the skill deliberately differs from the video. The reasons are in `skill/.../SKILL.md`.

## 1. Psychology: why a stranger says yes (3:56 to 18:30)
The core problem in outbound is that the reader has no trust in you yet. Seven
levers, mostly taken from Cialdini's *Influence*:

| # | Principle | What it means for the message | ts |
|---|---|---|---|
| 1 | Give first | Offer something the reader values, such as an insight, an audit, a sample or credits. The ask is implied rather than stated. | 5:17 |
| 2 | Micro-commitments | Start with a tiny yes, then escalate: reply, then watch 1 minute, then a call, then a proposal. | 7:56 |
| 3 | Social proof | Name specific people and exact numbers (not ranges or vague "lots of clients"), and match the reader's reference group, e.g. a similar business nearby. | 9:45 |
| 4 | Authority | Relevant credentials (partner programmes, well-known clients) and confident, unhedged wording. Credibility has to fit the ICP. | 12:44 |
| 5 | Rapport | Shared context, plus mirroring tone, length, punctuation and casing. | 14:27 |
| 6 | Scarcity | A real limit on capacity or time, e.g. "I can only take on X this month" or a proposal expiry. Invented limits trip the reader's BS detector. It's the least-used lever. | 15:50 |
| 7 | Shared identity | Same industry, struggles or values, and in-group language. He rates it the most important. | 17:00 |

## 2. Three components of a campaign (18:33 to 34:10)
1. **One goal per message, stateable in one sentence.** Each message should work on its own. Pick one action:
   reply, watch/click, book a call, or (rarely) buy. The fewer steps to reach the goal, the better, because
   every back-and-forth loses leads.
2. **Frame = person-to-person (P2P).** Write as if to one person.
   - *Text-message test*: would a friend who saw it think it was personal or a mass email?
   - Cut corporate signals: "hope this finds you well", big signature blocks, "we".
   - Short, casual, slightly imperfect.
3. **Iterate like a scientist.** Form a hypothesis, send, measure KPIs (open, reply, booked, proposal,
   close, LTV), cut the losers, and build new variants from the winners. Trust data over your gut, and
   revealed preference over stated preference.

## 3. The 4-step copywriting framework (34:14 to 1:05:40)
1. **Personalization** (1 to 2 sentences, 1 is ideal). The opening is the highest-ROI real estate because
   readership drops off word by word. Its only job is to make the reader think "wait, do I know this
   person?" and never signal a sale.
   - *Cold reading*: statements that feel specific but are true for most of the segment.
   - Optionally, a scraped fact woven into a cold-read template.
   - Voluntary self-disclosure builds trust.
   - Anti-pattern: LLM-sounding flattery about the reader's "passion for process optimization".
2. **Who am I and why does it matter** (1 to 2 sentences). It answers "is this a scammer?", then "who is
   this and why should I care?". The best form is "I currently work with [similar client / similar
   industry + location] to do [thing], and we got [specific number] in [time]". That gives social proof,
   authority and in-group in one line. Your job title alone ("I'm a thumbnail designer") is weak.
3. **Offer**: an observation or pain point (cold-readable), then an offer so good that "no" feels
   irrational, with built-in risk reversal. Template: **I will do X in Y time, or Z risk mitigation.**
   Quantified, time-bound, no ranges.
4. **CTA**: one specific ask with specific times, e.g. "open to a 15-min call? I can ring you at 3:30pm
   today or before noon tomorrow". It should be one step from yes to booked. Vague CTAs like "let me know
   your thoughts" add round-trips, and he estimates they leak about 25% of leads.

## 4. Offer formula (1:05:46 to 1:35:00)
`Conversion ≈ (perceived ROI × trust you'll deliver) / friction to start`

- **ROI** = a quantified result plus a time bound, e.g. "20 booked meetings in 60 days". Define the unit
  unambiguously: a meeting isn't a "conversation".
- **Trust** comes from rapport, social proof, in-group and authority. Promise less than you've proven,
  e.g. offer 10 patients/month when you've done 109 in a week.
- **Friction**: only 15 minutes of the reader's time, once; "we won't need to talk again until...";
  one-click invites. The risk reversal also removes friction.
- Size claims relative to the prospect's scale. Revenue up 2 to 20% can sound huge in absolute terms.
- Offer shapes seen in the video:
  - Guaranteed result or you don't pay
  - Free work up front and pay only if you like it
  - Free audit delivered in 24 to 48 hours
  - "Send me a title and I'll send a free sample"
  - Pay only after the first N clients
  - Rewrite your last 3 campaigns for free
  - Credits or a free programme entry
- "Just say yes" CTAs are wearing out (1:25:10).
- **System > template**: templates decay as the market gets used to them. The underlying system keeps
  producing new templates.

## 5. Roast-and-rewrite drills (1:35:08 to 2:50:40)
He scores real inbound pitches against the 7 principles (for example 1/7 or 0/7), then rewrites each one
with the 4 steps. Recurring faults:

- No give; the only offer is "a 15-minute call", which takes time rather than giving value.
- Scraped variables not cleaned, e.g. "Hi Nick Daily Updates" or a legal company name.
- Quotes or bold around variables.
- Tracking or signature footers, links in cold email (hurts deliverability), and prices in the first email.
- Branding yourself as an AI or robot, and LLM-isms.
- "We" instead of "I".
- Vague "quick chat" instead of a timed, sized ask.
- Downplaying proof ("small team"), commercial-sounding generic openers, walls of text, too many actors.

Fix for scraped names: take the first word, or casualize the company name. Rewrites are often longer,
but only because the originals had no offer.

## 6. Platform specifics (2:50:52 to 3:13:50)
Everything visible before the open is copy you can optimise:

- **Email**: sender name (about 20 characters, use a full name), address, avatar, subject (about 30 to
  50 characters) plus preview text (about 50 to 100). Together they show roughly 150 characters, and any
  unused space fills with metadata, so write at least about 150 characters.
- **LinkedIn**: professional photo, Premium badge, credentials in the headline, a short first name
  (it takes teaser room), and a teaser of about 50 to 55 characters. Avoid the "Other" inbox.
- **X / Instagram**: getting out of message requests is the whole game. Use a real-looking, aged profile,
  keep it casual (lowercase is fine), and remember the teaser is about 30 to 50 characters.
- **iMessage / SMS**: the teaser (about 90 characters) is effectively the whole message. Write about
  1.5 times that and put a curiosity hook near the cut-off.

## 7. Subject lines, follow-ups, iteration (3:13:51 to 3:35:30)
- **Subject lines** are there to buy the click, not to sell. They should be plausibly deniable: could be
  a friend, a fan, a buyer. Keep them simple and lowercase-casual, with a name in the subject or preview
  (e.g. "nick, are you hiring?").
  - Loss framing works ("you're wasting $2,300/mo").
  - Bad: generic ("video editor"), selling, long, "quick ...", no subject.
- **Follow-ups**: start with a 2-step sequence (initial plus one short human ping). Add steps only once a
  variant clearly wins, because extra touches raise spam/block risk. Follow-ups look like "hey pete,
  checking in on this, did it get buried?", not a mini newsletter. Change the subject to test more.
- **Iteration**:
  - Always run multiple variants.
  - Keep a fixed weekly iteration slot and log the changes.
  - Aim for about 500 to 1,000 sends per variant before deciding (100 sends is noise).
  - Pick a large TAM so you can run many tests.
  - Make big changes early (radically different emails) and small changes late (words, subject).
  - At 3:30:40 he mentions using autoresearch to design and run these iterations.

## 8. AI in copywriting (3:35:34 to 3:47:40)
- He rarely uses AI for whole emails. His claim: AI reaches about the "two weeks of practice" level, and
  the market's quality floor is above that.
- Use AI for **small template variables** inside a template that already works:
  - Personalization snippets
  - A "casualization layer": "Pacific Creative Group LLC" becomes "PCG", "Vancouver, BC" becomes
    "East Van", plus school names and the like
  - Scraping and enrichment

## 9. Grey-hat techniques (3:47:40 to 3:58:30) **[guardrail]**
He describes rather than recommends:
- Bought or pre-warmed accounts and fake-persona mailboxes
- Renting employees' LinkedIn accounts (he calls this slimy)
- Power dialers and voicemail drops
- Mass cold SMS/WhatsApp and blue-bubble emulation

**The skill excludes all of these.** They break platform terms of service, telemarketing and
anti-spam law, or amount to impersonation.

## Where the skill deliberately departs from the video **[guardrail]**
| Video tactic | Skill behaviour | Why |
|---|---|---|
| "Case studies are easier to make than you think"; invented proof in rewrites ("work with a few of the top 20") | Proof comes **only** from facts the user supplies. If there's none, lead with give-first and cold reading instead. | Fabricated results are deceptive, and also the easiest way for an optimiser to game the eval. |
| Invented personal disclosures ("my GF says...") | Disclosures must be true and come from the sender profile, or be left out. | Same reason. |
| Deliberate typos, fake "Sent from my iPhone" | Casual register is fine; staged device signatures are off by default. | Minor deception; the user can opt in. |
| Never include an opt-out | Add a light opt-out line when the recipient's jurisdiction requires it (CAN-SPAM, GDPR/PECR, CASL). | Legal. |
| Grey-hat channels | Refuse. | Law and terms of service. |
