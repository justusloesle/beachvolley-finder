# beachvolley-finder
AI-augmented finder that automatically tracks beach volleyball tournaments and ranks them by public-transit convenience and personal fit.

<!-- ┌─ SCREENSHOT / GIF ────────────────────────────────────────────┐
     Highest-ROI element in the whole README. Add a screenshot of the
     Streamlit UI, or an example of the ranked message that lands on
     your phone, as soon as you have one. A reviewer scrolls, sees it,
     and immediately believes the project is real and does something.
     Leave this placeholder here until you have the image.
     └───────────────────────────────────────────────────────────────┘ -->

## Problem

Created to solve the issue of spontaniously appearing beach-volleyball tournaments on sites like ebf.li. Bad filtering-mechanisms on the sites and an often poor public transit connection to tournament locations create a tiresome searching experience for people with a busy schedule. 

## How it works

<!-- The money section for a technical reviewer. Make the
     deterministic-vs-LLM split explicit:
       - what is scraped / filtered deterministically
       - where the transit facts come from (which API)
       - what EXACTLY the LLM decides (the fuzzy multi-criteria
         ranking + the human-readable summary)
       - why that boundary — the "when NOT to use an LLM" judgment
     A small architecture diagram here is worth a lot. -->

## Tech stack

<!-- Short list so a reviewer can match it against a job posting in
     seconds. e.g. Python · pydantic · <transit API> · LangChain ·
     n8n · Streamlit · pytest -->

## Setup

<!-- Can someone actually run it? Even if nobody does, correct
     instructions signal you know how to ship.
       1. git clone ...
       2. uv sync
       3. cp .env.example .env  (then fill in the keys)
       4. <command to run> -->

## Results / Evaluation

<!-- Optional, but a real differentiator almost no student includes.
     Your mini-eval: on N tournaments you hand-ranked, how often does
     the LLM ranking agree with yours? Put the number here. -->

## TBD - Next Features

- Changing settings by texting the telegram bot - requires proper hosting of the service (not via github actions)
- New metric: tournament strength to rank "easier" tournaments higher - requires advanced scraping of individual tournaments



## License

MIT
