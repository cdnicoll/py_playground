from pydantic import BaseModel, Field
from pydantic_ai import Agent
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()

# Define the structure you want back


class TextSummary(BaseModel):
    """Structured summary of text content"""
    main_summary: str = Field(
        description="A concise 2-3 sentence summary of the text")
    key_points: List[str] = Field(
        description="3-5 most important points from the text")
    sentiment: str = Field(
        description="Overall sentiment: positive, negative, or neutral")
    word_count: int = Field(
        description="Approximate word count of original text")
    topics: List[str] = Field(description="Main topics or themes covered")
    confidence_score: Optional[float] = Field(
        description="Confidence in summary quality (0-1)",
        default=None
    )


# Create the agent with your desired model and return type
summarizer_agent = Agent(
    'openai:gpt-4',  # or 'anthropic:claude-3-sonnet-20240229', etc.
    result_type=TextSummary,
    system_prompt="""
    You are an expert text analyzer. Analyze the provided text and return a structured summary.
    Be accurate and concise. For sentiment, consider the overall tone and message.
    Extract the most meaningful topics and key points.
    """
)


async def summarize_text(text: str) -> TextSummary:
    """Summarize text and return structured output"""
    result = await summarizer_agent.run(
        f"Please analyze and summarize this text: {text}"
    )
    return result.data

# Example usage


async def main():
    sample_text = """
    Artificial intelligence has transformed numerous industries over the past decade. 
    From healthcare diagnostics to autonomous vehicles, AI systems are becoming 
    increasingly sophisticated and reliable. However, concerns about job displacement 
    and ethical considerations continue to spark debate among policymakers and the public. 
    Despite these challenges, the potential benefits of AI in solving complex global 
    problems like climate change and disease remain enormous.
    """

    summary = await summarize_text(sample_text)

    print("Structured Summary:")
    print(f"Main Summary: {summary.main_summary}")
    print(f"Key Points: {summary.key_points}")
    print(f"Sentiment: {summary.sentiment}")
    print(f"Word Count: {summary.word_count}")
    print(f"Topics: {summary.topics}")

    # You can also convert to dict or JSON
    print("\nAs JSON:")
    print(summary.model_dump_json(indent=2))

# Run the example
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
