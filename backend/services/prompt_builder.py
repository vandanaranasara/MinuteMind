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
    # Keep prompt explicit about JSON-only output.
    # Build JSON structure dynamically based on what's enabled
    json_fields = [
        '  "summary_short": ["..."],',
        '  "summary_detailed": "...",',
        '  "discussion_flow": ["..."],',
    ]
    
    # Only include timeline in JSON structure if enabled
    if include_timeline:
        json_fields.append('  "timeline": [{ "timestamp": "MM:SS", "topic": "..." }],')
    
    json_fields.append('  "action_items": [{ "task": "...", "assigned_to": "...", "deadline": "YYYY-MM-DD" }],')
    
    # Only include sentiment in JSON structure if enabled
    if include_sentiment:
        json_fields.append('  "speaker_sentiment": { "Speaker Name": "positive|neutral|negative" }')
    
    instructions = [
        "You are an assistant that MUST produce ONLY JSON and nothing else.",
        "The input 'transcript' is the meeting transcript extracted from TXT/PDF.",
        "You must produce the following JSON structure exactly (fields must exist; empty is allowed):",
        "{",
    ] + json_fields + [
        "}",
        "For 'summary_detailed', write a detailed summary in **2–3 separate paragraphs**, not a single paragraph."
    ]

    extra = []
    if include_speakers:
        extra.append("Preserve and use speaker labels found in the transcript (e.g., 'Alice:', 'Bob:').")
    else:
        extra.append("Ignore speaker labels.")
    extra.append("Detect and extract actionable tasks and who was assigned.")

    # Use meeting_date for interpreting deadlines in action items
    if meeting_date:
        extra.append(
            f"For deadlines in action_items, use the meeting date {meeting_date} (YYYY-MM-DD) as the reference "
            "when interpreting relative phrases like 'next Monday', 'by Friday', or 'in two weeks'. "
            "Convert all deadlines to YYYY-MM-DD format. If no deadline is mentioned for an action item, set deadline to null."
        )
    else:
        extra.append(
            "For deadlines in action_items: only extract if explicitly mentioned in the transcript. "
            "Convert relative dates (like 'Wednesday', 'Friday', 'next week') to YYYY-MM-DD format using the meeting date "
            "mentioned in the transcript if it is clearly stated. If no deadline is mentioned, set deadline to null. "
            "Do NOT invent or guess deadlines."
        )
    
    if include_timeline:
        extra.append("Build an approximate timeline: for each major discussion point, give an approximate timestamp in MM:SS or HH:MM if possible; if transcript lacks timestamps, infer approximate timestamps assuming meeting length is unknown—provide relative order like 00:02, 00:05."
                     "Build a timeline only when explicit or clearly inferable time cues exist. "
                     "Do NOT invent or guess timestamps. If no reliable time markers exist, return an empty array for timeline.")
    else:
        extra.append("DO NOT generate or include a timeline field. Do not analyze or extract any timeline information. This will save tokens.")
    
    if include_sentiment:
        extra.append("For each speaker that speaks at least once, identify sentiment as positive, negative or neutral.")
    else:
        extra.append("DO NOT generate or include speaker_sentiment field. Do not analyze or extract any sentiment information. This will save tokens.")
    
    extra.append("Do not include any markdown, explanations, or extra text. Only output JSON.")

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
        # Insert after title (or after instructions if no title)
        insert_pos = 3 if meeting_title else 2
        prompt_parts.insert(insert_pos, f"Meeting Date: {meeting_date} (YYYY-MM-DD)")

    full_prompt = "\n\n".join(prompt_parts)
    return full_prompt