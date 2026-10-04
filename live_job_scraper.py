import urllib.request
import json
import xml.etree.ElementTree as ET
import html

class LiveJobScraper:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    def fetch_rss_live_jobs(self, query="Equity Research Analyst India"):
        """
        Fetches live real-time job announcements from RSS feeds (e.g. Google News / Job Alerts RSS).
        """
        jobs = []
        try:
            encoded = urllib.parse.quote(f"{query} hiring job")
            rss_url = f"https://news.google.com/rss/search?q={encoded}&hl=en-IN&gl=IN&ceid=IN:en"
            
            req = urllib.request.Request(rss_url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=6) as resp:
                xml_data = resp.read()
                root = ET.fromstring(xml_data)
                
                for item in root.findall('.//item')[:4]:
                    raw_title = item.find('title').text if item.find('title') is not None else ""
                    raw_link = item.find('link').text if item.find('link') is not None else ""
                    raw_pub = item.find('pubDate').text if item.find('pubDate') is not None else ""
                    source = item.find('source').text if item.find('source') is not None else "Live News / hiring"
                    
                    if raw_title:
                        clean_title = html.unescape(raw_title)
                        jobs.append({
                            "id": f"LIVE-{hash(clean_title) % 10000}",
                            "role_category": "Equity Research Analyst",
                            "title": clean_title[:75],
                            "company": source,
                            "location": "India (Live Listing)",
                            "portal": "Live Web Feed",
                            "portal_logo": "",
                            "url": raw_link,
                            "description": f"Live hiring announcement ({raw_pub}). Details: {clean_title}"
                        })
        except Exception as e:
            print(f"Live fetch notice: {e}")
            
        return jobs

if __name__ == "__main__":
    scraper = LiveJobScraper()
    live_jobs = scraper.fetch_rss_live_jobs()
    print(f"Fetched {len(live_jobs)} real-time live hiring feeds.")
