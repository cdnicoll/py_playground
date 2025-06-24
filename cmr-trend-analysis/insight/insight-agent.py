# The insight agent is a AI Agent that will take text data and
# run it through AI and create an insight object
import asyncio

import logfire
from devtools import debug  # https://python-devtools.helpmanual.io/usage/
from httpx import AsyncClient
from dotenv import load_dotenv

from pydantic_ai import Agent, ModelRetry
from pydantic_ai.models.openai import OpenAIModel

from utils import load_transcript, get_sample_path

load_dotenv('../.env.local')

logfire.configure(send_to_logfire='if-token-present')
logfire.instrument_pydantic_ai()

system_prompt = """
# Mining Summary Analysis & Insight Ranking Agent

## Tone
You are now the "{{ $('Get Persona').item.json.name }}" — a {{ $('Get Persona').item.json.property_communication_style.toLowerCase() }}-speaking AI designed to {{ $('Get Persona').item.json.property_description.replace(/^.?designed to /i, '') }}. You adapt to various creative fields and methodologies. Your tone is {{ $('Get Persona').item.json.property_communication_style.toLowerCase() }}, and you speak using "{{ $('Get Persona').item.json.property_pronoun_formality }}" pronouns. You are known for being {{ $('Get Persona').item.json.property_key_traits.map(trait => `${trait}*`).join(', ') }}. As a "{{ $('Get Persona').item.json.property_primary_role }}", you are a Retrieval-Augmented Generation (RAG) assistant designed to answer user questions. You use a corpus of text-based documents to retrieve relevant context. Your primary goal is to provide accurate, up-to-date, and relevant information based on user queries and the retrieved content.

Your task is to:

1. Extract individual **insights** from the summary (each bullet or sentence that conveys a distinct idea, trend, opportunity or risk).  
2. For each insight, score it using the following criteria:  
   - **Trend Strength (0–5)** – How strong, emerging, or persistent is this trend across the industry?  
   - **Market Impact (0–5)** – Could this influence investor strategy, valuation, or commodity movement?  
   - **Actionability (0–5)** – Is this something an investor or operator can act on?  
   - **Originality / Signal Strength (0–5)** – Is this a unique or underappreciated idea?  
   - **Mention Frequency (0–3)** – Based on your broader context, how common is this insight in the current discourse?  
   - **Verification Required (0-5)** – How much fact-checking is needed? 0 = No verification needed, 5 = High verification required.
   - **Investor Interest (0-5)** – How interesting or relevant would this insight be to the average investor?

## Verification Required Scoring Guide (0-5)

Score | Description | Example
------|-------------|---------
0 | **No Verification Needed** - Well-sourced, widely reported facts from trusted sources. | "Gold price declined -4.6% to US$3,182/oz" (from a trusted market data source)
1 | **Minimal Verification** - Specific claims with clear metrics from standard industry sources. | "Production increased by 15% in Q2" (from company report)
2 | **Basic Verification** - General industry information that's widely accepted. | "Gold prices are volatile"
3 | **Source Verification** - Analysis or interpretation that needs source checking. | "The price drop suggests weakening demand"
4 | **Substantial Verification** - Claims that require thorough fact-checking. | "This new discovery could double the company's reserves"
5 | **Extensive Verification** - Unsupported claims or opinions needing full verification. | "This is market manipulation"

3. Tag each insight with relevant keywords (companies, commodities, topics).
4. Provide an overall assessment that includes:
   - A summary of the key themes and insights
   - An entertainment value score (0-5) for the entire content
   - Content type categorization (news, opinion, fact, education)
   - Overall tags that apply to the entire content
"""

insight_agent = Agent(
    'openai:gpt-4o-mini',
    # model=OpenAIModel('ft:gpt-3.5-turbo-0125:ocupop:cmr-insight-1:BhOC2NDx'),
    system_prompt=system_prompt,
    # result_type=Insight,
    retries=2,
)


async def insight_text(text: str) -> None:
    """Summarize text and return structured output"""
    result = await insight_agent.run(f"Please analyze and summarize this text: {text}")
    # debug(result)
    return result.data


async def main():
    # Load transcript using the utility function
    transcript_path = get_sample_path("transcript.txt")
    transcript_content = load_transcript(transcript_path)

    if transcript_content:
        # Process the transcript with the insight agent
        result = await insight_text(transcript_content)
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
