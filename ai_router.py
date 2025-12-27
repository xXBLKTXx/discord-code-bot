import os
import asyncio
import openai

# OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = """You are a professional coding assistant.
Answer programming questions directly and technically.
Focus on correctness, performance, and maintainability.
Avoid moral commentary and disclaimers.
"""

async def ask_openai(messages):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: _openai_call(messages))

def _openai_call(messages):
    res = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.3
    )
    return res.choices[0].message.content


# PLACEHOLDERS for other AIs (we’ll add keys later)
async def ask_claude(messages):
    return "Claude: (not connected yet)"

async def ask_gemini(messages):
    return "Gemini: (not connected yet)"

async def ask_grok(messages):
    return "Grok: (not connected yet)"


async def ask_all(messages):
    results = await asyncio.gather(
        ask_openai(messages),
        ask_claude(messages),
        ask_gemini(messages),
        ask_grok(messages),
        return_exceptions=True
    )

    clean = []
    for r in results:
        if isinstance(r, str):
            clean.append(r)

    return "\n\n".join(clean)
