import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from agent_skill_gap import SkillGapAgent
from agent_job_matcher import JobMatcherAgent

class EmailDigestNotifier:
    def __init__(self, profile_path="candidate_profile.json"):
        with open(profile_path, "r", encoding="utf-8") as f:
            self.profile = json.load(f)
            
    def generate_digest_html(self):
        """Generates a clean HTML weekly email digest for Abhilash."""
        matcher = JobMatcherAgent()
        jobs = matcher.get_role_jobs(matcher.key_roles)
        
        gap_agent = SkillGapAgent()
        report = gap_agent.generate_weekly_report(jobs)

        name = self.profile.get("personal_info", {}).get("name", "Abhilash Srivastava")

        actions_html = "".join([f"<li style='margin-bottom:8px;'>{a}</li>" for a in report["recommended_weekly_actions"]])
        gaps_html = "".join([f"<li><b>{g['skill']}</b> — High market demand ({g['demand_frequency']})</li>" for g in report["skill_gaps"]])

        digest_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; color: #1e293b; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background-color: #1e3a8a; color: white; padding: 20px; border-radius: 8px; text-align: center;">
                <h2 style="margin: 0;">Weekly Career Advancement Digest</h2>
                <p style="margin: 5px 0 0 0; font-size: 13px;">Tailored for {name} (CFA Level III Cleared)</p>
            </div>
            
            <div style="padding: 20px 0;">
                <h3 style="color: #1e40af; border-bottom: 2px solid #e2e8f0; padding-bottom: 5px;">📊 Key Market Skill Gaps This Week</h3>
                <ul>{gaps_html}</ul>

                <h3 style="color: #1e40af; border-bottom: 2px solid #e2e8f0; padding-bottom: 5px;">💡 Recommended Actions For The Week</h3>
                <ul>{actions_html}</ul>

                <div style="background-color: #f1f5f9; padding: 15px; border-radius: 6px; margin-top: 20px; font-size: 12px; color: #64748b;">
                    Analyzed across active hiring listings on <b>Naukri.com</b>, <b>LinkedIn India</b>, and <b>Indeed</b>.<br>
                    Open your dashboard at <a href="http://localhost:8502" style="color:#2563eb;">http://localhost:8502</a> to apply or optimize your resume.
                </div>
            </div>
        </body>
        </html>
        """
        return digest_body

if __name__ == "__main__":
    notifier = EmailDigestNotifier()
    digest = notifier.generate_digest_html()
    print("Generated weekly email digest HTML (length:", len(digest), "bytes)")
