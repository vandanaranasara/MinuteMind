def build_prompt(
    transcript: str,
    meeting_title: str = "",
    meeting_date: str | None = None,
    include_speakers: bool = True,
    include_sentiment: bool = True,
    include_timeline: bool = True,
    language: str = "english",
) -> str:
    """
    Constructs a single prompt that instructs the LLM to return only the specified JSON format.
    """

    # ---------------- JSON STRUCTURE ----------------
    json_fields = [
        '  "summary_short": ["..."],',
        '  "summary_detailed": "...",',
        '  "discussion_flow": ["..."],',
    ]

    if include_timeline:
        json_fields.append(
            '  "timeline": [{ "timestamp": "MM:SS", "topic": "..." }],'
        )

    json_fields.append(
        '  "action_items": [{ "task": "...", "assigned_to": "...", "deadline": "YYYY-MM-DD|null" }],'
    )

    if include_sentiment:
        json_fields.append(
            '  "speaker_sentiment": { "Speaker Name": "positive|neutral|negative" }'
        )

    instructions = [
        "You are an assistant that MUST produce ONLY valid JSON and nothing else.",
        "The input 'transcript' is a real meeting transcript.",
        "You must produce the following JSON structure exactly (all fields must exist; empty is allowed):",
        "{",
    ] + json_fields + [
        "}",
        "For 'summary_detailed', write a detailed summary in 2–3 separate paragraphs."
    ]

    extra = []

    # ---------------- SPEAKER HANDLING ----------------
    if include_speakers:
        extra.append(
            "Preserve and use speaker labels found in the transcript (e.g., 'Alice:', 'Bob:')."
        )
    else:
        extra.append("Ignore speaker labels.")

    # ---------------- ACTION ITEM RULES ----------------
    extra.extend([
        "Extract only clear, actionable tasks with an explicit verb (e.g., add, update, deploy, fix).",
        "Each action item MUST represent exactly one unique task.",
        "Do NOT split a single commitment into multiple tasks unless they are clearly different.",
        "Merge overlapping or duplicate tasks into a single action item.",
        "If ownership is mentioned, populate 'assigned_to'. Otherwise, set it to null.",
    ])

    # ---------------- DEADLINE RULES (FINAL & CORRECT) ----------------
    if meeting_date:
        extra.extend([
            "Compute all deadlines relative to the meeting date.",
            f"Treat the meeting date as {meeting_date} (YYYY-MM-DD).",

            # 🔒 HARD, UNBREAKABLE RULE (THIS FIXES YOUR BUG)
            (
                "WEEKDAY RESOLUTION (STRICT, NO EXCEPTIONS): "
                "If a weekday name is mentioned WITHOUT the word 'next' "
                "(e.g., 'Friday', 'by Friday', 'Friday morning'), "
                "AND it matches the weekday of the meeting date, "
                "you MUST use the MEETING DATE itself. "
                "You are NOT allowed to move it to the next day or next week."
            ),

            (
                "If a weekday name is mentioned WITHOUT 'next' "
                "and it occurs later in the SAME calendar week after the meeting date, "
                "use that same-week date."
            ),

            (
                "If the phrase 'next <weekday>' is explicitly used "
                "(e.g., 'next Friday'), resolve it to the weekday in the FOLLOWING week."
            ),

            # Relative phrases
            "If someone says 'tomorrow', deadline = meeting date + 1 day.",
            "If someone says 'day after tomorrow', deadline = meeting date + 2 days.",

            # Absolute dates
            (
                "If an absolute date is mentioned (e.g., '18/12/2025', 'December 18, 2025'), "
                "convert it to strict YYYY-MM-DD format."
            ),

            # Safety rules
            "Deadlines must NEVER be earlier than the meeting date.",
            "If resolving a deadline places it before the meeting date, use the meeting date instead.",
            "If multiple deadlines are mentioned for the same task, choose the earliest explicit one.",
            "If no explicit or clearly inferable deadline exists, set deadline to null.",
            "Do NOT guess or invent deadlines.",
            "Always output deadlines in strict YYYY-MM-DD format."
        ])
    else:
        extra.append(
            "Only extract deadlines if explicitly mentioned. "
            "Do NOT infer or guess dates without a meeting date. "
            "If unclear, set deadline to null."
        )

    # ---------------- TIMELINE RULES ----------------
    if include_timeline:
        extra.append(
            "Generate a timeline only if explicit timestamps or clear time cues exist. "
            "Do NOT invent timestamps. If unreliable, return an empty array."
        )
    else:
        extra.append("DO NOT generate a timeline field.")

    # ---------------- SENTIMENT RULES ----------------
    if include_sentiment:
        extra.append(
            "For each speaker who speaks at least once, classify sentiment as positive, neutral, or negative."
        )
    else:
        extra.append("DO NOT generate speaker_sentiment.")

    extra.append(
        "Do not include markdown, explanations, or any text outside the JSON object."
    )

    # ---------------- FINAL PROMPT ----------------
    prompt_parts = [
        "### INSTRUCTIONS ###",
        "\n".join(instructions),
        "\n".join(extra),
        "### TRANSCRIPT ###",
        transcript,
    ]

    if meeting_title:
        prompt_parts.insert(2, f"Meeting Title: {meeting_title}")

    if meeting_date:
        insert_pos = 3 if meeting_title else 2
        prompt_parts.insert(
            insert_pos, f"Meeting Date: {meeting_date} (YYYY-MM-DD)"
        )

    return "\n\n".join(prompt_parts)
