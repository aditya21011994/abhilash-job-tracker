import html
import re

class PDFResumeGenerator:
    @staticmethod
    def generate_html_resume(profile, job_info, recommendations):
        """
        Generates a clean, print-ready, ATS-tailored HTML resume for Abhilash.
        """
        name = profile.get("personal_info", {}).get("name", "Abhilash B. Srivastava")
        email = profile.get("personal_info", {}).get("email", "abhilash8021@gmail.com")
        phone = profile.get("personal_info", {}).get("phone", "+91 91045 31002")
        location = profile.get("personal_info", {}).get("location", "Surat, Gujarat, India")
        
        cfa_level = profile.get("cfa_status", {}).get("level", "CFA Level III Cleared")
        cfa_details = profile.get("cfa_status", {}).get("details", "Cleared all exams")
        
        job_title = job_info.get("title", "Finance & Analytics Professional")
        company = job_info.get("company", "Target Firm")

        skills = ", ".join(profile.get("technical_skills", []))
        
        recs_html = ""
        if recommendations:
            recs_html = '<div class="section"><div class="section-title">TAILORED ATS HIGHLIGHTS FOR THIS ROLE</div>'
            for r in recommendations:
                recs_html += f'<div class="bullet"><b>• {r["category"]}:</b> {r["action"]}</div>'
            recs_html += '</div>'

        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Resume - {name}</title>
    <style>
        body {{ font-family: 'Helvetica Neue', Arial, sans-serif; margin: 40px; color: #1e293b; line-height: 1.5; font-size: 13px; }}
        .header {{ text-align: center; border-b: 2px solid #2563eb; padding-bottom: 12px; margin-bottom: 20px; }}
        .name {{ font-size: 24px; font-weight: bold; color: #0f172a; text-transform: uppercase; }}
        .contact {{ font-size: 11px; color: #475569; margin-top: 5px; }}
        .badge {{ background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; font-size: 11px; font-weight: bold; padding: 3px 8px; border-radius: 4px; display: inline-block; margin-top: 6px; }}
        .section {{ margin-bottom: 18px; }}
        .section-title {{ font-size: 12px; font-weight: bold; color: #1e40af; border-bottom: 1px solid #cbd5e1; padding-bottom: 3px; margin-bottom: 8px; letter-spacing: 0.5px; text-transform: uppercase; }}
        .item-header {{ font-weight: bold; color: #0f172a; display: flex; justify-content: space-between; }}
        .item-sub {{ font-style: italic; color: #475569; font-size: 12px; margin-bottom: 4px; }}
        .bullet {{ margin-left: 12px; margin-bottom: 4px; text-align: justify; }}
        @media print {{
            body {{ margin: 0; padding: 20px; }}
            .no-print {{ display: none; }}
        }}
    </style>
</head>
<body>
    <div class="no-print" style="background:#f8fafc; border:1px solid #e2e8f0; padding:10px; margin-bottom:20px; border-radius:6px; text-align:center;">
        <b>📄 Tailored ATS Resume Preview for: {job_title} ({company})</b> — 
        <button onclick="window.print()" style="background:#2563eb; color:white; border:none; padding:6px 14px; border-radius:4px; font-weight:bold; cursor:pointer;">Print / Save as PDF</button>
    </div>

    <div class="header">
        <div class="name">{name}</div>
        <div class="contact">{location} • {email} • {phone}</div>
        <div class="badge">{cfa_level} ({cfa_details})</div>
    </div>

    <div class="section">
        <div class="section-title">PROFESSIONAL SUMMARY</div>
        <div class="bullet">
            Analytical and detail-oriented candidate with <b>CFA Level III Cleared</b> status, postgraduate training in <b>Statistics (M.Com)</b>, and a Bachelor's in <b>Finance (BBA)</b>. Skilled in Python, MySQL, financial statement analysis, DCF valuation modeling, and macro-economic research.
        </div>
    </div>

    {recs_html}

    <div class="section">
        <div class="section-title">EDUCATION</div>
        <div class="item-header">
            <span>Chartered Financial Analyst (CFA Institute)</span>
            <span>2022 - 2026</span>
        </div>
        <div class="item-sub">Cleared all 3 exam levels (Charter pending) • Passed Level 1 & Level 2 in top 90th percentile</div>

        <div class="item-header" style="margin-top:8px;">
            <span>Masters of Commerce (Statistics) — Veer Narmad South Gujarat University</span>
            <span>2022 - 2024</span>
        </div>
        <div class="item-sub">Postgraduate Degree • CGPA: 6.83</div>

        <div class="item-header" style="margin-top:8px;">
            <span>Bachelors of Business Administration (Finance) — MSU Baroda</span>
            <span>2017 - 2020</span>
        </div>
        <div class="item-sub">Undergraduate Degree • CGPA: 7.27</div>
    </div>

    <div class="section">
        <div class="section-title">TECHNICAL & QUANTITATIVE SKILLS</div>
        <div class="bullet"><b>Financial & Quantitative Analysis:</b> Equity Valuation, DCF Modeling, Fixed Income, Derivatives, Econometric Modeling, Practical Macro</div>
        <div class="bullet"><b>Programming & Software:</b> Python, MySQL, Advanced Excel (Macros), Tally Accounting, MS Word, PowerPoint</div>
    </div>

    <div class="section">
        <div class="section-title">RESEARCH & KEY PROJECTS</div>
        <div class="item-header">
            <span>A Study On The Doughnut Economic Model And Its Application in the Indian Economy</span>
        </div>
        <div class="bullet">• Conducted statistical analysis evaluating social deprivation indices against ecological stress indicators in India.</div>
        <div class="bullet">• Built data processing models in Excel/Python to analyze macroeconomic variables.</div>
    </div>

    <div class="section">
        <div class="section-title">POSITIONS OF RESPONSIBILITY</div>
        <div class="item-header">
            <span>Treasurer — MSU BBA Students' Association</span>
            <span>2019 - 2020</span>
        </div>
        <div class="bullet">• Managed organizational funds; spearheaded digital event generating Rs 50,000 turnover in 2 days.</div>
    </div>
</body>
</html>
        """
        return html_content

if __name__ == "__main__":
    import json
    with open("candidate_profile.json", "r") as f:
        prof = json.load(f)
    gen = PDFResumeGenerator()
    res_html = gen.generate_html_resume(prof, {"title": "Equity Analyst", "company": "Motilal Oswal"}, [])
    print("Generated print-ready ATS resume HTML (length:", len(res_html), "bytes)")
