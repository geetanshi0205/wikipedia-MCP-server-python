from typing import Any
import httpx
from fastmcp import FastMCP

# Create a FastMCP server instance
mcp = FastMCP(
    "wikipedia",
    description="A Wikipedia search and article retrieval server for accessing Wikipedia content",
    version="1.0.0"
)

WIKIPEDIA_API_BASE = "https://en.wikipedia.org/api/rest_v1"
WIKIPEDIA_SEARCH_API = "https://en.wikipedia.org/w/api.php"
USER_AGENT = "wikipedia-mcp/1.0"

async def make_wikipedia_request(url: str, params: dict[str, Any] = None) -> dict[str, Any] | None:
    """Make a request to Wikipedia API with proper headers and error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

def format_search_result(page: dict) -> str:
    """Format a search result into a readable string."""
    title = page.get('title', 'Unknown')
    snippet = page.get('snippet', 'No description available').replace('<span class="searchmatch">', '').replace('</span>', '')
    return f"""Title: {title}
Description: {snippet}
URL: https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"""

def format_article_summary(data: dict) -> str:
    """Format article summary data into readable text."""
    title = data.get('title', 'Unknown')
    extract = data.get('extract', 'No summary available')
    content_urls = data.get('content_urls', {}).get('desktop', {}).get('page', '')
    
    return f"""Title: {title}
Summary: {extract}
URL: {content_urls}"""

def format_article_sections(sections: list) -> str:
    """Format article sections into a readable list."""
    if not sections:
        return "No sections found."
    
    formatted_sections = []
    for section in sections[:10]:  # Limit to first 10 sections
        line = section.get('line', 'Unknown Section')
        formatted_sections.append(f"- {line}")
    
    return "\n".join(formatted_sections)

@mcp.tool()
async def search_wikipedia(query: str, limit: int = 10) -> str:
    """
    Search Wikipedia for articles matching a query.
    
    Args:
        query: The search terms to look for
        limit: Maximum number of results to return (1-20, default: 10)
    
    Returns:
        Formatted string with search results including titles, descriptions, and URLs
    """
    params = {
        'action': 'query',
        'format': 'json',
        'list': 'search',
        'srsearch': query,
        'srlimit': min(limit, 20)
    }
    
    data = await make_wikipedia_request(WIKIPEDIA_SEARCH_API, params)
    if not data or 'query' not in data or 'search' not in data['query']:
        return "Unable to search Wikipedia or no results found."
    
    search_results = data['query']['search']
    if not search_results:
        return f"No Wikipedia articles found for query: '{query}'"
    
    results = [format_search_result(result) for result in search_results]
    return f"Found {len(results)} Wikipedia articles:\n\n" + "\n---\n".join(results)

@mcp.tool()
async def get_wikipedia_article(title: str) -> str:
    """
    Get the full content of a Wikipedia article.
    
    Args:
        title: The title of the Wikipedia article
    
    Returns:
        Formatted string with article summary and sections list
    """
    # First get the page summary
    summary_url = f"{WIKIPEDIA_API_BASE}/page/summary/{title.replace(' ', '_')}"
    summary_data = await make_wikipedia_request(summary_url)
    
    if not summary_data:
        return f"Unable to fetch Wikipedia article '{title}'. Article may not exist."
    
    # Get page sections
    sections_url = f"{WIKIPEDIA_API_BASE}/page/sections/{title.replace(' ', '_')}"
    sections_data = await make_wikipedia_request(sections_url)
    
    # Format the response
    article_info = format_article_summary(summary_data)
    
    if sections_data and sections_data.get('sections'):
        sections_list = format_article_sections(sections_data['sections'])
        article_info += f"\n\nSections:\n{sections_list}"
    
    return article_info

@mcp.tool()
async def get_wikipedia_summary(title: str) -> str:
    """
    Get a concise summary of a Wikipedia article.
    
    Args:
        title: The title of the Wikipedia article
    
    Returns:
        Formatted string with article title, summary, and URL
    """
    url = f"{WIKIPEDIA_API_BASE}/page/summary/{title.replace(' ', '_')}"
    data = await make_wikipedia_request(url)
    
    if not data:
        return f"Unable to fetch summary for Wikipedia article '{title}'."
    
    return format_article_summary(data)

@mcp.tool()
async def get_wikipedia_sections(title: str) -> str:
    """
    Get the sections of a Wikipedia article.
    
    Args:
        title: The title of the Wikipedia article
    
    Returns:
        Formatted string listing all sections in the article
    """
    url = f"{WIKIPEDIA_API_BASE}/page/sections/{title.replace(' ', '_')}"
    data = await make_wikipedia_request(url)
    
    if not data or 'sections' not in data:
        return f"Unable to fetch sections for Wikipedia article '{title}'."
    
    sections = data['sections']
    formatted_sections = format_article_sections(sections)
    
    return f"Sections for '{title}':\n{formatted_sections}"

@mcp.tool()
async def get_wikipedia_links(title: str, limit: int = 20) -> str:
    """
    Get links contained within a Wikipedia article.
    
    Args:
        title: The title of the Wikipedia article
        limit: Maximum number of links to return (1-50, default: 20)
    
    Returns:
        Formatted string with list of links found in the article
    """
    # Use the Wikipedia API to get page links
    params = {
        'action': 'query',
        'format': 'json',
        'titles': title,
        'prop': 'links',
        'pllimit': min(limit, 50)
    }
    
    data = await make_wikipedia_request(WIKIPEDIA_SEARCH_API, params)
    if not data or 'query' not in data or 'pages' not in data['query']:
        return f"Unable to fetch links for Wikipedia article '{title}'."
    
    pages = data['query']['pages']
    page = next(iter(pages.values()))
    
    if 'links' not in page:
        return f"No links found in Wikipedia article '{title}'."
    
    links = [link['title'] for link in page['links']]
    
    return f"Links in '{title}' (showing {len(links)} links):\n" + "\n".join([f"- {link}" for link in links])

@mcp.tool()
async def get_related_topics(title: str, limit: int = 10) -> str:
    """
    Get topics related to a Wikipedia article based on categories.
    
    Args:
        title: The title of the Wikipedia article
        limit: Maximum number of related topics to return (default: 10)
    
    Returns:
        Formatted string with list of related topics based on article categories
    """
    # Get page categories
    params = {
        'action': 'query',
        'format': 'json',
        'titles': title,
        'prop': 'categories',
        'cllimit': 20
    }
    
    data = await make_wikipedia_request(WIKIPEDIA_SEARCH_API, params)
    if not data or 'query' not in data or 'pages' not in data['query']:
        return f"Unable to fetch related topics for Wikipedia article '{title}'."
    
    pages = data['query']['pages']
    page = next(iter(pages.values()))
    
    if 'categories' not in page:
        return f"No categories found for Wikipedia article '{title}'."
    
    categories = [cat['title'].replace('Category:', '') for cat in page['categories']]
    related_topics = categories[:limit]
    
    return f"Topics related to '{title}':\n" + "\n".join([f"- {topic}" for topic in related_topics])

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')### Write code for the new module here and import it from agent.py.