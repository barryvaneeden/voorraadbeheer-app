from __future__ import annotations

import datetime as dt
from pathlib import Path

import streamlit as st

STORAGE_DIR = Path("data/notulen")


def _save_text(meeting_dir: Path, filename: str, content: str) -> Path:
    meeting_dir.mkdir(parents=True, exist_ok=True)
    path = meeting_dir / filename
    path.write_text(content.strip() + "\n", encoding="utf-8")
    return path


def _render_action_items(action_items: list[dict]) -> None:
    if not action_items:
        st.info("Geen actiepunten gevonden.")
        return
    for index, item in enumerate(action_items, start=1):
        st.markdown(
            f"{index}. **{item['actie']}**  \n"
            f"   - Eigenaar: {item['eigenaar']}  \n"
            f"   - Deadline: {item['deadline']}"
        )


def _parse_action_items(raw_lines: list[str]) -> list[dict]:
    action_items: list[dict] = []
    for line in raw_lines:
        parts = [part.strip() for part in line.split("|")]
        actie = parts[0] if parts else ""
        eigenaar = parts[1] if len(parts) > 1 else "Nog te bepalen"
        deadline = parts[2] if len(parts) > 2 else "Nog te bepalen"
        if actie:
            action_items.append({"actie": actie, "eigenaar": eigenaar, "deadline": deadline})
    return action_items


def show() -> None:
    st.title("Notulen & Agenda")
    st.write(
        "Zet geschreven notities en (optioneel) audio-tekst om naar notulen met actiepunten "
        "en een agenda voor het volgende Algemeen Overleg."
    )

    st.subheader("1. Invoer")
    meeting_title = st.text_input("Titel van het overleg")
    meeting_date = st.date_input("Datum overleg", value=dt.date.today())
    notes_text = st.text_area("Geschreven notities", height=200, placeholder="Plak hier je notities.")
    transcript_text = st.text_area(
        "Transcriptie (uitgeschreven audio)",
        height=200,
        placeholder="Plak hier de transcriptie van de audio.",
    )

    st.subheader("2. Actiepunten")
    st.write("Voeg actiepunten toe in het formaat: actie | eigenaar | deadline")
    action_items_text = st.text_area(
        "Actiepunten",
        height=120,
        placeholder="Bijv. Contact opnemen met leverancier | Sam | 2024-10-01",
    )

    if st.button("Genereer notulen en agenda"):
        if not meeting_title.strip():
            st.error("Vul een titel van het overleg in.")
            st.stop()

        meeting_slug = f"{meeting_date.isoformat()}_{meeting_title.strip().replace(' ', '_')}"
        meeting_dir = STORAGE_DIR / meeting_slug
        combined_text = "\n\n".join([text for text in [notes_text, transcript_text] if text.strip()])

        if not combined_text:
            st.error("Voeg geschreven notities en/of een transcriptie toe.")
            st.stop()

        _save_text(meeting_dir, "notities.txt", notes_text or "")
        _save_text(meeting_dir, "transcriptie.txt", transcript_text or "")
        _save_text(meeting_dir, "combined.txt", combined_text)

        raw_action_lines = [line for line in action_items_text.splitlines() if line.strip()]
        action_items = _parse_action_items(raw_action_lines)

        st.success("Notulen en agenda zijn klaar!")

        st.subheader("Notulen (concept)")
        st.markdown(f"**Overleg:** {meeting_title}")
        st.markdown(f"**Datum:** {meeting_date}")
        st.markdown("**Samenvatting:**")
        st.markdown(combined_text)

        st.subheader("Actiepunten")
        _render_action_items(action_items)

        st.subheader("Agenda voor nieuw Algemeen Overleg")
        agenda_items = ["Opening", "Terugblik vorige actiepunten"]
        agenda_items.extend([item["actie"] for item in action_items] or ["Nieuwe actiepunten bespreken"])
        agenda_items.append("Rondvraag & afsluiting")
        for index, item in enumerate(agenda_items, start=1):
            st.markdown(f"{index}. {item}")
