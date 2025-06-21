from __future__ import annotations as _annotations

from dataclasses import dataclass
from dotenv import load_dotenv
import logfire
# https://python-devtools.helpmanual.io/usage/import asyncio
from devtools import debug
import httpx
import os

from pydantic_ai import Agent, ModelRetry, RunContext
from pydantic_ai.models.openai import OpenAIModel
from supabase import Client
from typing import List


load_dotenv('.env.local')

# 'if-token-present' means nothing will be sent (and the example will work) if you don't have logfire configured
# cdnicoll: How do I configure logfire?
logfire.configure(send_to_logfire='if-token-present')
logfire.instrument_pydantic_ai()


@dataclass
class Deps:
    supabase: Client
    openai_client: AsyncOpenAI


model = OpenAIModel('gpt-4o-mini')

system_prompt = """
## Tone
You are now the "College professor or K-12 teacher" — a conversational-speaking AI designed to Find activities or articles on sustainability activities or topics. You adapt to various creative fields and methodologies. Your tone is conversational, and you speak using "Casual You/Your" pronouns. You are known for being Logical*, Adaptive*, Patient*. As a "Specialist", you are a Retrieval-Augmented Generation (RAG) assistant designed to answer user questions. You use a corpus of text-based documents to retrieve relevant context. Your primary goal is to provide accurate, up-to-date, and relevant information based on user queries and the retrieved content.

## Responsibilities
- Answer user queries with a balance of comprehensiveness and conciseness.
- Present information in a clear, easy-to-understand, and professional manner.
- Correct any misconceptions or misinformation when detected.
- Provide proper source citations for all information retrieved from documents.

## Key Instructions
- If the answer cannot be found in the retrieved documents, clearly state that. Do not fabricate information.
- Use neutral, factual language. Avoid expressing opinions or showing bias.
- Always cite your sources using clickable numbered footnotes [[1]](source_url), [[2]](source_url), etc. when referencing information from retrieved documents.
- Include a "Sources" section at the bottom of your response with numbered references linking to the source_url.
- There are also featured_images within the metadata, you can embed those as well

## Citation Format
- Use in-text citations with clickable numbered links: [[1]](source_url_1), [[2]](source_url_2), etc.
- At the end of your response, include a "Sources" section formatted as:

**Sources:**
1. [source_url_1](source_url_1)
2. [source_url_2](source_url_2)
3. [source_url_3](source_url_3)

## Error Handling
- If no relevant information is found, respond with:
  "I'm sorry, I couldn't find relevant information based on your documents."
"""

sidekick_agent = Agent(
    model,
    system_prompt=system_prompt,
    retries=2,
    deps_type=Deps,
)


async def get_embedding(text: str, openai_client: AsyncOpenAI) -> List[float]:
    """Get embedding for the users question as a vector from OpenAI."""
    try:
        response = await openai_client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error getting embedding: {e}")
        return [0] * 1536  # Return zero vector on error


@sidekick_agent.tool
async def retrieve_relevant_documentation(ctx: RunContext[Deps], user_query: str) -> str:
    """
    Retrieve relevant documentation chunks based on the query with RAG.

    Args:
        ctx: The context including the Supabase client and OpenAI client
        user_query: The user's question or query

    Returns:
        A formatted string containing the top 5 most relevant documentation chunks
    """
    try:
        # Get the embedding for the query
        query_embedding = await get_embedding(user_query, ctx.deps.openai_client)
        debug(query_embedding)

        # Query Supabase for relevant documents using RPC call instead of direct order
        try:
            # First approach: Try using rpc for vector search
            result = ctx.deps.supabase.rpc(
                'match_documents',  # You need to create this function in Supabase
                {
                    'query_embedding': query_embedding,
                    'match_count': 5
                }
            ).execute()
        except Exception as e:
            # Fallback approach: Use a simpler query without vector search
            print(f"RPC approach failed: {e}, falling back to simple query")
            result = ctx.deps.supabase.table('sustainableamerica_vectors').select(
                '*',
                count='exact'
            ).limit(5).execute()

        if not result.data:
            return "No relevant documentation found."

        # Format the results
        formatted_chunks = []
        # TODO we may need to look into this a bit to see what we're getting back
        debug(result.data)
        for doc in result.data:
            chunk_text = f"""
            # {doc['title']}

            {doc['content']}
            """
            formatted_chunks.append(chunk_text)

        # Join all chunks with a separator
        return "\n\n---\n\n".join(formatted_chunks)

    except Exception as e:
        print(f"Error retrieving documentation: {e}")
        return f"Error retrieving documentation: {str(e)}"
