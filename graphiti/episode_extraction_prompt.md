# Episode Extraction Prompt for Graphiti

Given the following blog article in JSON format with:
- `frontMatter`: metadata including title, date, author, tags, and categories
- `content`: the main article body as HTML

Process each logical section or paragraph of the content to create episodes for Graphiti ingestion.

## Episode Creation Process

For each logical section or paragraph:

1. **Content Processing:**
   - Convert HTML section/paragraph to clean plain text
   - Remove HTML tags while preserving paragraph structure
   - Include section heading if available
   - Ensure content is substantial enough to be meaningful (combine short paragraphs if needed)

2. **Context Enhancement:**
   - Add relevant context from the article metadata (title, author, publication date)
   - Include the section heading for better context
   - Ensure each episode can stand alone as a coherent piece of information

## Output Format

Return a JSON array where each object represents one episode:

```json
[
  {
    "name": "Article Title - Section Name",
    "content": "The actual text content of the section, including any relevant context",
    "type": "text",
    "description": "Source description (e.g., 'blog article', 'news article', 'technical documentation')",
    "metadata": {
      "source_title": "Original article title",
      "author": "Author name", 
      "date": "Publication date",
      "section_heading": "Section heading if available",
      "tags": ["tag1", "tag2"],
      "categories": ["category1"]
    }
  }
]
```

## Guidelines

- **Content Quality:** Each episode should contain enough information to be meaningful on its own
- **Context Preservation:** Include relevant metadata context so the episode makes sense without the full article
- **Logical Segmentation:** Break content at natural boundaries (headings, topic changes, etc.)
- **Avoid Duplication:** Don't repeat the same information across multiple episodes
- **Maintain Source Attribution:** Always include author and publication information

## Example Processing

If you have a section like:
```html
<h2>OpenAI Releases GPT-4 Turbo</h2>
<p>OpenAI announced the release of GPT-4 Turbo, a more efficient version of their flagship language model...</p>
```

Transform it to:
```json
{
  "name": "Latest AI Developments - OpenAI Releases GPT-4 Turbo",
  "content": "OpenAI announced the release of GPT-4 Turbo, a more efficient version of their flagship language model. The new model offers improved performance while reducing costs for developers by up to 3x compared to GPT-4.",
  "type": "text", 
  "description": "blog article",
  "metadata": {
    "source_title": "Latest AI Developments in 2024",
    "author": "Jane Smith",
    "date": "2024-03-15", 
    "section_heading": "OpenAI Releases GPT-4 Turbo",
    "tags": ["AI", "OpenAI", "GPT-4"],
    "categories": ["Technology News"]
  }
}
```

The entity and relationship extraction will be handled automatically by Graphiti's processing pipeline.