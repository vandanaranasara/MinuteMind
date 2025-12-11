def build_prompt(transcript: str, meeting_title: str = "", include_speakers: bool = True,
                 include_sentiment: bool = True, include_timeline: bool = True, language: str = "english") -> str:
    """
    Constructs a single prompt that instructs the LLM to return only the specified JSON format.
    """
    # Keep prompt explicit about JSON-only output.
    instructions = [
        "You are an assistant that MUST produce ONLY JSON and nothing else.",
        "The input 'transcript' is the meeting transcript extracted from TXT/PDF.",
        "You must produce the following JSON structure exactly (fields must exist; empty is allowed):",
        "{",
        '  "summary_short": ["..."],',
        '  "summary_detailed": "...",',
        '  "discussion_flow": ["..."],',
        '  "timeline": [{ "timestamp": "MM:SS", "topic": "..." }],',
        '  "action_items": [{ "task": "...", "assigned_to": "...", "deadline": "YYYY-MM-DD" }],',
        '  "speaker_sentiment": { "Speaker Name": "positive|neutral|negative" }',
        "}"
    ]

    extra = []
    if include_speakers:
        extra.append("Preserve and use speaker labels found in the transcript (e.g., 'Alice:', 'Bob:').")
    else:
        extra.append("Ignore speaker labels.")
    extra.append("Detect and extract actionable tasks, who was assigned, and deadlines (date-like strings).")
    if include_timeline:
        extra.append("Build an approximate timeline: for each major discussion point, give an approximate timestamp in MM:SS or HH:MM if possible; if transcript lacks timestamps, infer approximate timestamps assuming meeting length is unknown—provide relative order like 00:02, 00:05."
                     "Build a timeline only when explicit or clearly inferable time cues exist. "
                     "Do NOT invent or guess timestamps. If no reliable time markers exist, return an empty array for timeline.")
    if include_sentiment:
        extra.append("For each speaker that speaks at least once, identify sentiment as positive, negative or neutral.")
    extra.append("Do not include any markdown, explanations, or extra text. Only output JSON.")

    prompt_parts = [
        "### INSTRUCTIONS ###",
        "\n".join(instructions),
        "\n".join(extra),
        "### TRANSCRIPT ###",
        transcript
    ]
    if meeting_title:
        prompt_parts.insert(2, f"Meeting Title: {meeting_title}")

    full_prompt = "\n\n".join(prompt_parts)
    return full_prompt