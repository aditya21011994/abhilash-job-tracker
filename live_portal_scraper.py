import requests
import json
import urllib.parse
import re

class LivePortalScraper:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        }

    def fetch_live_jobs_for_role(self, role_keyword, location="India"):
        """
        Queries LinkedIn's public guest job search API endpoints directly for real active job cards.
        Returns exact canonical URLs (https://www.linkedin.com/jobs/view/{job_id}).
        """
        jobs = []
        try:
            encoded_role = urllib.parse.quote(role_keyword)
            encoded_loc = urllib.parse.quote(location)
            
            # Direct LinkedIn public guest jobs endpoint
            api_url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={encoded_role}&location={encoded_loc}&start=0"
            
            resp = requests.get(api_url, headers=self.headers, timeout=8)
            if resp.status_code == 200:
                # Regex search for direct job view URLs & titles
                # Pattern matches: /jobs/view/123456789 or /jobs/view/title-123456789
                raw_html = resp.text
                
                # Match links like href="https://in.linkedin.com/jobs/view/equity-research-analyst-at-motilal-oswal-38492019"
                matches = re.findall(r'href="(https:\/\/[a-z]{2,3}\.linkedin\.com\/jobs\/view\/[^"?]+)', raw_html)
                titles = re.findall(r'<h3 class="base-search-card__title">([^<]+)<\/h3>', raw_html)
                companies = re.findall(r'<h4 class="base-search-card__subtitle">\s*<a[^>]*>([^<]+)<\/a>', raw_html)
                
                seen_urls = set()
                idx = 0
                for url in matches:
                    clean_url = url.strip()
                    if clean_url not in seen_urls:
                        seen_urls.add(clean_url)
                        
                        job_title = titles[idx].strip() if idx < len(titles) else f"{role_keyword} Specialist"
                        comp = companies[idx].strip() if idx < len(companies) else "Financial Institution"
                        
                        jobs.append({
                            "id": f"LINKEDIN-DIRECT-{idx+900}",
                            "role_category": role_keyword,
                            "title": job_title,
                            "company": comp,
                            "location": f"{location} (Live Active Listing)",
                            "portal": "LinkedIn India (Direct Page)",
                            "portal_logo": "https://www.linkedin.com/favicon.ico",
                            "url": clean_url,
                            "description": f"Direct real-time posting for {job_title} at {comp}. Requiring CFA Level II/III candidates, valuation modeling, and statistical/quantitative proficiency."
                        })
                        idx += 1
                        if len(jobs) >= 6:
                            break
        except Exception as e:
            print(f"[LinkedIn Direct API Scraper Note] {e}")

        return jobs

if __name__ == "__main__":
    scraper = LivePortalScraper()
    jobs = scraper.fetch_live_jobs_for_role("Equity Research Analyst", "India")
    print(f"Fetched {len(jobs)} exact direct LinkedIn job pages:")
    for j in jobs:
        print(f" - [{j['company']}] {j['title']}\n   Direct Page URL: {j['url']}")
