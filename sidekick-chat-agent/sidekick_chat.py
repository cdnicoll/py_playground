import os
import asyncio
from supabase import Client
from openai import AsyncOpenAI
from devtools import debug

from sidekick_agent import sidekick_agent, Deps


openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
supabase: Client = Client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY")
)


async def main():
    deps = Deps(
        openai_client=openai_client,
        supabase=supabase,
    )
    result = await sidekick_agent.run(
        "Tell me about offgrid living", deps=deps
    )
    debug(result)
    print('Response:', result.output)

if __name__ == "__main__":
    asyncio.run(main())
