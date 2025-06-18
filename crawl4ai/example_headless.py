import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode


async def main():
    browser_conf = BrowserConfig(
        headless=False,
        viewport_width=1280,
        viewport_height=720
    )

    run_conf = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
    )

    async with AsyncWebCrawler(config=browser_conf) as crawler:
      url = "https://www.mining.com/web/freeport-indonesia-requests-copper-concentrate-export-permit/"
      
      result = await crawler.arun(url=url, config=run_conf)

      print(result.markdown)

      if result.success:
          print("Extracted content:", result.extracted_content)
      else:
          print("Error:", result.error_message)

if __name__ == "__main__":
    asyncio.run(main())