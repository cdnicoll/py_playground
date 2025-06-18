# https://docs.crawl4ai.com/core/simple-crawling/

import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig


async def main():
    async with AsyncWebCrawler() as crawler:

        run_config = CrawlerRunConfig(
            word_count_threshold=10,        # Minimum words per content block
            exclude_external_links=True,    # Remove external links
            remove_overlay_elements=True,   # Remove popups/modals
            process_iframes=False,          # Process iframe content
            exclude_social_media_links=True,
            exclude_social_media_domains=["facebook.com", "twitter.com"],
            excluded_tags=['form', 'header',
                           'footer', 'nav'],  # Tag exclusions
        )

        # result = await crawler.arun(url="https://screenrant.com/serebii-pokemon-joe-merrick-interview/", run_config=run_config)
        result = await crawler.arun(url="https://www.mining.com/web/freeport-indonesia-requests-copper-concentrate-export-permit/", run_config=run_config)

        # Print the extracted content
        print(result.metadata)

        # Write the markdown content to a file
        with open('scraped_markdown.md', 'w', encoding='utf-8') as f:
            f.write(result.markdown)

asyncio.run(main())
