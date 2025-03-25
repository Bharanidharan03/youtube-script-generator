import requests
import feedparser
import google.generativeai as genai
import praw  # Reddit API

# Set API Keys (Replace with your actual keys)
YOUTUBE_API_KEY = "AIzaSyC_cs1a2AaKzSggU4D0q_t1gasPDFiPFWQ"
REDDIT_CLIENT_ID = "VCdisDPPEbyk8lTnc5iVWg"
REDDIT_CLIENT_SECRET = "KwvUNyVjOJSWcFuwOYqzl37TLPZ69g"
GEMINI_API_KEY = "AIzaSyDjQtV8jpzeu2CiO4lLSVbcCjwL6Bp45Zo"

# Configure Google Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Configure Reddit API
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent="TrendingScriptGenerator"
)

REGION_CODE = "IN"

# Get YouTube Categories
def get_youtube_categories():
    url = f"https://www.googleapis.com/youtube/v3/videoCategories?part=snippet&regionCode={REGION_CODE}&key={YOUTUBE_API_KEY}"
    response = requests.get(url).json()
    categories = [{"id": item["id"], "name": item["snippet"]["title"]} for item in response.get("items", [])] #Return a list of dictionaries.
    return categories

# Get Trending Videos
def get_trending_videos(category_id):
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "part": "snippet",
        "chart": "mostPopular",
        "regionCode": REGION_CODE,
        "videoCategoryId": category_id,
        "maxResults": 5,
        "key": YOUTUBE_API_KEY
    }
    response = requests.get(url, params=params).json()
    return [{"id": video["id"], "title": video["snippet"]["title"]} for video in response.get("items", [])] #Return a list of dictionaries.

# Fetch Google News
def get_google_news():
    feed = feedparser.parse("https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en")
    return [entry.title for entry in feed.entries[:5]]

# Fetch Reddit Trending Topics
def get_reddit_trending():
    subreddit = reddit.subreddit("all")
    return [post.title for post in subreddit.hot(limit=5)]

# Generate AI-Based YouTube Script
def generate_script(topic):
    model = genai.GenerativeModel("gemini-1.5-pro")
    prompt = f"Generate an SEO-optimized YouTube script for: {topic}. Include keywords, engaging introduction, and a call-to-action."
    response = model.generate_content(prompt)
    return response.text

#Combine trending topics
def get_all_trending():
    news_trends = get_google_news()
    reddit_trends = get_reddit_trending()
    all_trends = news_trends + reddit_trends
    return all_trends