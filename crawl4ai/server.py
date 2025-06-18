"""
curl -X POST \
  http://192.168.1.92:5001/get_markdown \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.metabase.com/data_sources/amazon-athena"}'
"""

import random
from flask import Flask, request, jsonify
import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig

app = Flask(__name__)


async def get_markdown_from_url(url):
    """
    Function to get markdown content from a URL using crawl4ai with configurations based on official docs.
    """

    # Browser Configuration
    browser_config = BrowserConfig(
        browser_type="chromium",  # or "firefox", "webkit"
        headless=True,  # Set to False for debugging
        user_agent=random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Mobile/15E148 Safari/604.1"
        ]),
        # user_agent_mode="random", # Alternatively, use built-in randomization (if you prefer)
        # proxy_config={"http": "http://yourproxy:port", "https": "http://yourproxy:port"}, # Optional proxy
        viewport_width=1280,
        viewport_height=720,
        text_mode=False,  # Keep images for realistic browsing
        # cookies=[{"name": "cookie_name", "value": "cookie_value", "domain": "example.com"}], # Optional cookies
        # headers={"Accept-Language": "en-US,en;q=0.9"}, # Optional headers
    )

    # Crawler Run Configuration
    run_config = CrawlerRunConfig(
        word_count_threshold=10,
        exclude_external_links=True,
        remove_overlay_elements=True,
        process_iframes=False,
        excluded_tags=['form', 'header', 'footer', 'nav'],
        # enable_javascript=True,  # Crucial for dynamic content
        # wait_for="css:.content-loaded",  # Wait for a specific element if needed
        # js_code="window.scrollTo(0, document.body.scrollHeight);",  # Example: Scroll to bottom
        # cache_mode=CacheMode.BYPASS # If bypassing cache is needed
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(url=url, config=run_config)

        return {
            "url": url,
            "markdown": result.markdown,
            "metadata": result.metadata
        }


# Example usage:
# asyncio.run(get_markdown_from_url("https://example.com"))


@app.route('/get_markdown', methods=['POST'])
def get_markdown():
    """
    Endpoint to get markdown content from a URL

    Request format:
    {
        "url": "https://example.com"
    }

    Response format:
    {
        "url": "https://example.com",
        "markdown": "# Markdown content...",
        "metadata": {
            "title": "Page Title",
            "description": "Page Description",
            ...
        }
    }
    """
    try:
        data = request.get_json()

        if not data or 'url' not in data:
            return jsonify({"error": "URL is required"}), 400

        url = data['url']

        # Run the async function to get markdown and metadata
        result = asyncio.run(get_markdown_from_url(url))

        # Return the result directly (contains url, markdown and metadata)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
