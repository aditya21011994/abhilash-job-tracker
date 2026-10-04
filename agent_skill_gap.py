import json
from collections import Counter

class SkillGapAgent:
    def __init__(self, profile_path="candidate_profile.json"):
        with open(profile_path, "r", encoding="utf-8") as f:
            self.profile = json.load(f)
            
        self.candidate_skills = set([s.lower() for s in self.profile.get("technical_skills", [])])
        # Add core profile implicitly known
        self.candidate_skills.update(["cfa", "cfa level 3", "statistics", "finance", "excel", "python", "mysql", "tally"])

    def generate_weekly_report(self, jobs_list):
        """
        Analyzes a batch of active market JDs, extracts top requested skills,
        and identifies gaps vs Abhilash's profile with actionable recommendations.
        """
        all_text = " ".join([f"{j.get('title', '')} {j.get('description', '')}" for j in jobs_list]).lower()
        
        industry_skill_pool = {
            "power bi": "Power BI / Tableau (Data Visualization)",
            "tableau": "Power BI / Tableau (Data Visualization)",
            "dcf": "DCF / Financial Valuation Modeling",
            "valuation": "DCF / Financial Valuation Modeling",
            "bloomberg": "Bloomberg Terminal / Refinitiv Eikon",
            "refinitiv": "Bloomberg Terminal / Refinitiv Eikon",
            "r": "R Language for Econometrics",
            "financial modeling": "Advanced Financial Modeling in Excel",
            "derivatives": "Derivatives & Fixed Income Analytics",
            "pandas": "Python Pandas / Quantitative Libraries"
        }
        
        detected_demand = Counter()
        for key, category in industry_skill_pool.items():
            if key in all_text:
                detected_demand[category] += 1
                
        # Classify into current strengths vs missing skill gaps
        skills_matched = []
        skill_gaps = []
        
        for category, count in detected_demand.most_common():
            # Check if Abhilash has related keywords
            if any(term in category.lower() for term in ["python", "excel", "cfa", "financial valuation"]):
                skills_matched.append({"skill": category, "demand_frequency": f"High ({count} JDs)"})
            else:
                skill_gaps.append({"skill": category, "demand_frequency": f"High ({count} JDs)"})

        # Concrete recommendations
        action_items = []
        if any("Visualization" in g["skill"] for g in skill_gaps):
            action_items.append("📊 **Visualization Project:** Build a 1-page Power BI dashboard visualizing portfolio returns or macro data, and link it in the resume.")
        if any("Financial Modeling" in g["skill"] for g in skill_gaps):
            action_items.append("📈 **Financial Modeling:** Add a specific bullet point under Projects detailing a 3-statement DCF financial model built in Excel/Python.")
        if any("Bloomberg" in g["skill"] for g in skill_gaps):
            action_items.append("💻 **Market Data Tools:** Familiarize with open-source financial APIs (yfinance, Alpha Vantage) as a Python alternative to Bloomberg terminal workflows.")

        return {
            "total_jobs_analyzed": len(jobs_list),
            "matched_strengths": skills_matched,
            "skill_gaps": skill_gaps,
            "recommended_weekly_actions": action_items
        }

if __name__ == "__main__":
    from agent_job_matcher import JobMatcherAgent
    matcher = JobMatcherAgent()
    jobs = matcher.sample_job_fetcher()
    gap_agent = SkillGapAgent()
    report = gap_agent.generate_weekly_report(jobs)
    print(f"Weekly Analysis Complete across {report['total_jobs_analyzed']} jobs.")
    print(f"Identified {len(report['skill_gaps'])} key market skill gaps.")
