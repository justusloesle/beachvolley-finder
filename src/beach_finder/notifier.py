"""Sends final results of the daily scrape to the users using a telegram bot. """
import requests

from beach_finder.config import TELEGRAM_BOT_API_KEY
from beach_finder.models import User, TournamentCandidate

EBF_TOURNAMENT_BASE = "https://www.ebf.li/de/frontend/tournament/details/"


def send_message(message: str, user: User):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_API_KEY}/sendMessage"
    resp = requests.post(url, json={"chat_id": user.telegram_chat_id, "text": message, "parse_mode": "Markdown"}, timeout=10)
    resp.raise_for_status()


WD = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]


def format_message_response(candidates: list[TournamentCandidate], top: int = 3, total: int = 6) -> str:
    if not candidates:
        return "🏐 Keine passenden Turniere gefunden."

    lines = ["🏐 *Deine Turniere*", ""]

    for i, c in enumerate(candidates[:top], start=1):
        t = c.tournament
        wd = WD[t.begin_time.weekday()]
        lines.append(f"*{i}. {t.name}*")
        lines.append(f"{wd}, {t.begin_time.strftime('%d.%m.')} · {t.begin_time.strftime('%H:%M')} Uhr · {c.estimated_travel_time} min")
        if c.reasoning:
            lines.append(f"_{c.reasoning}_")
        lines.append(f"[Anmelden]({EBF_TOURNAMENT_BASE}{t.id})")
        lines.append("")

    rest = candidates[top:total]
    if rest:
        lines.append("*Außerdem:*")
        for c in rest:
            t = c.tournament
            wd = WD[t.begin_time.weekday()]
            lines.append(f"· {wd}, {t.begin_time.strftime('%d.%m.')} · {t.name} · {c.estimated_travel_time} min — [Link]({EBF_TOURNAMENT_BASE}{t.id})")

    return "\n".join(lines).strip()

