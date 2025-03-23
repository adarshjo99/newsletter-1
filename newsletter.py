# -*- coding: utf-8 -*-
from datetime import datetime
import feedparser
import os

user_personas = {
    "Alex Parker": {
        "interests": ["AI", "cybersecurity", "blockchain", "startups", "programming"],
        "sources": [
            "https://techcrunch.com/feed/",
            "https://www.wired.com/feed/category/tech/latest/rss",
            "https://www.technologyreview.com/feed/",
            "https://arstechnica.com/feed/"
        ]
    },
    "Priya Sharma": {
        "interests": ["Global markets", "startups", "fintech", "cryptocurrency", "economics"],
        "sources": [
            "https://www.bloomberg.com/feed",
            "https://www.ft.com/?format=rss",
            "https://www.forbes.com/markets/feed/",
            "https://www.coindesk.com/arc/outboundfeeds/rss/"
        ]
    },
    "Marco Rossi": {
        "interests": ["Football", "F1", "NBA", "Olympic sports", "esports"],
        "sources": [
            "https://www.espn.com/espn/rss/news",
            "https://feeds.bbci.co.uk/sport/rss.xml?edition=uk",
            "https://www.skysports.com/rss/12040",
            "https://theathletic.com/feed/"
        ]
    },
    "Lisa Thompson": {
        "interests": ["Movies", "celebrity news", "TV shows", "music", "books"],
        "sources": [
            "https://variety.com/feed/",
            "https://www.rollingstone.com/music/music-news/feed/",
            "https://www.billboard.com/feed/",
            "https://www.hollywoodreporter.com/t/television/feed/"
        ]
    },
    "David Martinez": {
        "interests": ["Space exploration", "AI", "biotech", "physics", "renewable energy"],
        "sources": [
            "https://www.nasa.gov/rss/dyn/breaking_news.rss",
            "https://www.sciencedaily.com/rss/all.xml",
            "https://www.nature.com/subjects/physics.rss",
            "https://arstechnica.com/science/feed/"
        ]
    }
}


def fetch_articles(sources):
    articles = []
    for url in sources:
        print(f"Fetching from: {url}")
        feed = feedparser.parse(url)
        for entry in feed.entries:
            articles.append({
                'title': entry.get('title', ''),
                'summary': entry.get('summary', ''),
                'link': entry.get('link', ''),
                'published': entry.get('published', ''),
                'source': url
            })
    return articles


def categorize_articles(articles, interests):
    categorized = {interest: [] for interest in interests}
    for article in articles:
        for interest in interests:
            if interest.lower() in article['title'].lower() or interest.lower() in article['summary'].lower():
                categorized[interest].append(article)
    return categorized


def generate_newsletter(username, categorized_articles):
    today = datetime.today().strftime('%Y-%m-%d')
    filename = f"{username}_newsletter_{today}.md"

    newsletter = f"# 📬 {username}'s Personalized Newsletter\n\n"
    newsletter += f"Date: {today}\n\n"
    newsletter += "## Top Picks\n"

    # Get top picks (1 article from each category)
    for interest, articles in categorized_articles.items():
        if articles:
            article = articles[0]
            newsletter += f"- [{article['title']}]({article['link']})\n"

    newsletter += "\n---\n\n"

    
    for interest, articles in categorized_articles.items():
        if articles:
            newsletter += f"## {interest}\n"
            for article in articles:
                newsletter += f"**{article['title']}**\n\n"
                newsletter += f"{article['summary']}\n\n"
                newsletter += f"[Read more]({article['link']})\n\n"
            newsletter += "\n---\n\n"

    
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, filename)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(newsletter)

    print(f"Newsletter generated: {file_path}")
    return file_path


def main():
    # Select a user persona
    print("Available personas:")
    for name in user_personas:
        print(f"- {name}")
    print()

    username = input("Enter the name of the persona you want to generate a newsletter for: ")

    if username not in user_personas:
        print("❌ Persona not found! Please try again.")
        return

    print(f"\nGenerating newsletter for {username}...\n")

    persona = user_personas[username]
    sources = persona['sources']
    interests = persona['interests']

    articles = fetch_articles(sources)
    categorized_articles = categorize_articles(articles, interests)
    newsletter_file = generate_newsletter(username, categorized_articles)

    print(f"\n✅ Newsletter ready! Check the file: {newsletter_file}")


if __name__ == "__main__":
    main()

