from textwrap import dedent
system_prompt = dedent(
    "You are an award-winning multilingual short-fiction writer and literary translator. "
    "Produce vivid, memorable stories with character desire, tension, and a satisfying turn. "
    "Avoid bland slice-of-life filler. Keep language level matched to the requested CEFR difficulty. "
    "Output must strictly follow the structured schema."
)

user_prompt = dedent(
    "Create one short story and aligned translations.\\n"
    "Requirements:\\n"
    "1) Difficulty: {difficulty}.\\n"
    "2) Languages (must include exactly these, no extras): {language_codes_csv}.\\n"
    "3) Keep each language version under {max_words} words.\\n"
    "4) Use the creative seed as inspiration: {creative_seed}.\\n"
    "5) Return each story as an ordered list of complete sentences.\\n"
    "6) Every language must have the exact same number of sentences.\\n"
    "7) Sentences at the same index must be faithful translations of each other.\\n"
    "8) Do not combine two source sentences into one target sentence, and do not split one source sentence into two.\\n"
    "9) Avoid abbreviations that contain periods (for example Mr., Dr., etc.) because they break sentence alignment.\\n"
    "10) End each sentence with terminal punctuation (. ! ?).\\n"
    "11) Keep titles concise and engaging (max 128 chars)."
)
