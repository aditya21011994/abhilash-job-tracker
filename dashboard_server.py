import http.server
import socketserver
import json
import urllib.parse
from agent_job_matcher import JobMatcherAgent
from agent_ats_optimizer import ATSOptimizerAgent
from agent_skill_gap import SkillGapAgent
from pdf_resume_generator import PDFResumeGenerator

PORT = 8502

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/" or parsed.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            html = self.render_dashboard()
            self.wfile.write(html.encode("utf-8"))
        elif parsed.path == "/api/jobs":
            query = urllib.parse.parse_qs(parsed.query)
            roles = query.get("roles", [])
            if roles and "," in roles[0]:
                roles = roles[0].split(",")
                
            matcher = JobMatcherAgent()
            jobs = matcher.get_role_jobs(roles)

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(jobs).encode("utf-8"))
        elif parsed.path == "/api/export-resume":
            with open("candidate_profile.json", "r", encoding="utf-8") as f:
                profile = json.load(f)
            
            generator = PDFResumeGenerator()
            resume_html = generator.generate_html_resume(profile, {"title": "Equity Analyst", "company": "Target Firm"}, [])
            
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(resume_html.encode("utf-8"))
        else:
            super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/optimize":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            jd = data.get("jd", "")
            job_info = data.get("job", {})
            
            ats_agent = ATSOptimizerAgent()
            analysis = ats_agent.analyze_resume_vs_jd(jd)
            cover_letter = ats_agent.generate_cover_letter(job_info)
            
            response = {
                "analysis": analysis,
                "cover_letter": cover_letter
            }
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode("utf-8"))

    def render_dashboard(self):
        matcher = JobMatcherAgent()
        all_roles = matcher.key_roles
        initial_jobs = matcher.get_role_jobs(all_roles)
        
        skill_agent = SkillGapAgent()
        weekly_report = skill_agent.generate_weekly_report(initial_jobs)

        jobs_json = json.dumps(initial_jobs)
        report_json = json.dumps(weekly_report)
        roles_json = json.dumps(all_roles)

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Abhilash Srivastava - Career Advancement Suite</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        /* Custom scrollbars */
        ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
        ::-webkit-scrollbar-track {{ background: #0f172a; }}
        ::-webkit-scrollbar-thumb {{ background: #334155; border-radius: 4px; }}
    </style>
</head>
<body class="bg-slate-900 text-slate-100 font-sans min-h-screen">

    <!-- Header -->
    <header class="bg-slate-800/90 backdrop-blur border-b border-slate-700 p-4 sticky top-0 z-50">
        <div class="max-w-7xl mx-auto flex justify-between items-center">
            <div class="flex items-center space-x-3">
                <div class="bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-bold p-2.5 rounded-xl shadow-lg shadow-blue-900/30 flex items-center justify-center w-11 h-11">
                    <i class="fa-solid fa-chart-line text-lg"></i>
                </div>
                <div>
                    <h1 class="text-xl font-bold text-white tracking-tight">Abhilash B. Srivastava | Career Co-Pilot</h1>
                    <p class="text-xs text-blue-400 font-medium">CFA Level III Cleared • M.Com Statistics • BBA Finance • Python & MySQL</p>
                </div>
            </div>
            <div class="hidden sm:flex space-x-2">
                <span class="px-3 py-1.5 bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 rounded-full text-xs font-semibold flex items-center">
                    <i class="fa-solid fa-award me-1.5"></i> CFA Level III Cleared
                </span>
                <span class="px-3 py-1.5 bg-blue-500/20 text-blue-400 border border-blue-500/30 rounded-full text-xs font-semibold flex items-center">
                    <i class="fa-solid fa-location-dot me-1.5"></i> Target Portals: Naukri • LinkedIn • Indeed
                </span>
            </div>
        </div>
    </header>

    <!-- Main Content Container -->
    <div class="max-w-7xl mx-auto p-6">
        
        <!-- Navigation Tabs -->
        <div class="flex border-b border-slate-700 mb-6 space-x-1">
            <button id="tab-jobs" onclick="switchTab('jobs')" class="py-3 px-5 text-sm font-bold border-b-2 border-blue-500 text-blue-400 focus:outline-none flex items-center transition">
                <i class="fa-solid fa-briefcase me-2"></i> 1. Indian Job Portal Feed (<span id="job-count">{len(initial_jobs)}</span>)
            </button>
            <button id="tab-ats" onclick="switchTab('ats')" class="py-3 px-5 text-sm font-bold border-b-2 border-transparent text-slate-400 hover:text-slate-200 focus:outline-none flex items-center transition">
                <i class="fa-solid fa-wand-magic-sparkles me-2"></i> 2. ATS Resume Optimizer & Cover Letter
            </button>
            <button id="tab-weekly" onclick="switchTab('weekly')" class="py-3 px-5 text-sm font-bold border-b-2 border-transparent text-slate-400 hover:text-slate-200 focus:outline-none flex items-center transition">
                <i class="fa-solid fa-chart-pie me-2"></i> 3. Skill Gap & Action Recommendations
            </button>
        </div>

        <!-- TAB 1: JOBS FEED WITH MULTI-ROLE SELECT -->
        <div id="view-jobs" class="space-y-6">
            
            <!-- Filter Bar: Multi-Select Key Roles -->
            <div class="bg-slate-800/80 p-5 rounded-2xl border border-slate-700 shadow-xl space-y-3">
                <div class="flex justify-between items-center">
                    <label class="text-sm font-bold text-white flex items-center">
                        <i class="fa-solid fa-sliders text-blue-400 me-2"></i> Select Core Competency Roles (Multi-Select):
                    </label>
                    <button onclick="selectAllRoles()" class="text-xs text-blue-400 hover:text-blue-300 font-semibold underline">
                        Select All Roles
                    </button>
                </div>
                
                <!-- Multi-select Pills Container -->
                <div id="role-pills-container" class="flex flex-wrap gap-2 pt-1">
                    <!-- Dynamically Generated Multi-select Role Pills -->
                </div>

                <div class="text-xs text-slate-400 pt-2 flex items-center justify-between border-t border-slate-700/60">
                    <span><i class="fa-solid fa-circle-info text-blue-400 me-1"></i> Showing live openings from popular Indian portals: <b>Naukri.com</b>, <b>LinkedIn India</b>, <b>Indeed India</b>, & <b>Foundit</b>.</span>
                    <span id="active-roles-count" class="font-semibold text-slate-300">All 6 Roles Active</span>
                </div>
            </div>

            <!-- Job Cards Grid -->
            <div id="jobs-grid" class="grid grid-cols-1 md:grid-cols-2 gap-5">
                <!-- Dynamically Inserted Cards -->
            </div>
        </div>

        <!-- TAB 2: ATS RESUME OPTIMIZER -->
        <div id="view-ats" class="hidden space-y-6">
            <div class="bg-slate-800 p-6 rounded-2xl border border-slate-700 shadow-xl">
                <h2 class="text-lg font-bold text-white mb-2 flex items-center">
                    <i class="fa-solid fa-file-contract text-blue-400 me-2"></i> Resume & ATS Optimizer Assistant
                </h2>
                <p class="text-sm text-slate-400 mb-4">Select a job from Tab 1 or paste a custom Job Description (JD) below to get instant ATS scores, bullet recommendations, and a tailored cover letter.</p>

                <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <!-- Input Section -->
                    <div class="space-y-4">
                        <div>
                            <label class="block text-xs font-semibold text-slate-300 mb-1">Target Job Title & Company</label>
                            <input type="text" id="ats-job-title" value="Equity Research Analyst - Motilal Oswal" class="w-full bg-slate-900 text-slate-200 text-sm p-3 rounded-xl border border-slate-700">
                        </div>
                        <div>
                            <label class="block text-xs font-semibold text-slate-300 mb-1">Job Description (JD)</label>
                            <textarea id="ats-jd-text" rows="8" class="w-full bg-slate-900 text-slate-200 text-sm p-3 rounded-xl border border-slate-700 font-mono" placeholder="Paste JD here...">Looking for a candidate with CFA Level 2 or Level 3 cleared. Responsibilities include building financial models, conducting equity research, performing DCF valuation, and tracking market macros in Python and Excel.</textarea>
                        </div>
                        <button onclick="runATSOptimizer()" class="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-3 rounded-xl text-sm transition shadow-lg shadow-blue-900/40">
                            <i class="fa-solid fa-bolt me-2"></i> Run ATS Optimization & Generate Pitch
                        </button>
                    </div>

                    <!-- Output Section -->
                    <div class="space-y-4 bg-slate-900 p-5 rounded-2xl border border-slate-800">
                        <div class="flex items-center justify-between pb-3 border-b border-slate-800">
                            <span class="text-sm font-semibold text-slate-300">Calculated ATS Fit Score</span>
                            <span id="ats-score-badge" class="px-3.5 py-1 bg-emerald-500/20 text-emerald-400 border border-emerald-500/40 font-extrabold text-xl rounded-xl">
                                85%
                            </span>
                        </div>

                        <!-- Recommendations -->
                        <div>
                            <h3 class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Recommended Resume Bullet Edits</h3>
                            <div id="ats-recommendations" class="space-y-2 text-xs">
                                <!-- Dynamic -->
                            </div>
                        </div>

                        <!-- Cover Letter Preview -->
                        <div class="pt-3 border-t border-slate-800">
                            <div class="flex justify-between items-center mb-2">
                                <h3 class="text-xs font-bold text-slate-400 uppercase tracking-wider">Tailored Cover Letter Pitch</h3>
                                <div class="space-x-2">
                                    <button onclick="copyCoverLetter()" class="text-xs text-blue-400 hover:underline me-2">
                                        <i class="fa-solid fa-copy me-1"></i> Copy Letter
                                    </button>
                                    <a href="/api/export-resume" target="_blank" class="px-2.5 py-1 bg-blue-600 hover:bg-blue-500 text-white rounded text-xs font-bold transition inline-flex items-center">
                                        <i class="fa-solid fa-file-pdf me-1"></i> Export Tailored Resume (PDF)
                                    </a>
                                </div>
                            </div>
                            <pre id="cover-letter-box" class="bg-slate-950 p-3 rounded-xl text-slate-300 text-xs font-sans whitespace-pre-wrap max-h-48 overflow-y-auto border border-slate-800/80"></pre>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 3: WEEKLY SKILL GAP ANALYSIS -->
        <div id="view-weekly" class="hidden space-y-6">
            <div class="bg-slate-800 p-6 rounded-2xl border border-slate-700 shadow-xl">
                <div class="flex justify-between items-start mb-6">
                    <div>
                        <h2 class="text-lg font-bold text-white flex items-center">
                            <i class="fa-solid fa-chart-line text-blue-400 me-2"></i> Weekly Market Skill Gap Analysis
                        </h2>
                        <p class="text-sm text-slate-400">Aggregated demand metrics across active CFA & Finance openings on Indian hiring portals.</p>
                    </div>
                    <span class="px-3 py-1 bg-blue-500/20 text-blue-400 border border-blue-500/30 rounded-xl text-xs font-medium">
                        Active Catalog Analysis
                    </span>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                    <!-- Matched Strengths -->
                    <div class="bg-slate-900 p-5 rounded-2xl border border-slate-800">
                        <h3 class="text-sm font-bold text-emerald-400 mb-3 flex items-center">
                            <i class="fa-solid fa-circle-check me-2"></i> Abhilash's Top Matched Strengths
                        </h3>
                        <div id="weekly-strengths" class="space-y-2"></div>
                    </div>

                    <!-- Identified Skill Gaps -->
                    <div class="bg-slate-900 p-5 rounded-2xl border border-slate-800">
                        <h3 class="text-sm font-bold text-amber-400 mb-3 flex items-center">
                            <i class="fa-solid fa-triangle-exclamation me-2"></i> Identified High-Demand Skill Gaps
                        </h3>
                        <div id="weekly-gaps" class="space-y-2"></div>
                    </div>
                </div>

                <!-- Action Plan -->
                <div class="bg-slate-900 p-5 rounded-2xl border border-slate-800">
                    <h3 class="text-sm font-bold text-blue-400 mb-3 flex items-center">
                        <i class="fa-solid fa-lightbulb me-2"></i> Weekly Action Recommendations
                    </h3>
                    <div id="weekly-actions" class="space-y-2 text-xs text-slate-300"></div>
                </div>
            </div>
        </div>

    </div>

    <!-- JavaScript logic -->
    <script>
        const allRoles = {roles_json};
        let selectedRoles = [...allRoles];
        let currentJobs = {jobs_json};
        const weeklyReportData = {report_json};

        function renderRolePills() {{
            const container = document.getElementById('role-pills-container');
            container.innerHTML = '';
            
            allRoles.forEach(role => {{
                const isSelected = selectedRoles.includes(role);
                const pill = document.createElement('button');
                pill.onclick = () => toggleRole(role);
                
                if (isSelected) {{
                    pill.className = 'px-3.5 py-1.5 rounded-xl text-xs font-bold bg-blue-600 text-white border border-blue-400 shadow-md flex items-center transition';
                    pill.innerHTML = `<i class="fa-solid fa-check me-1.5 text-[10px]"></i> ${{role}}`;
                }} else {{
                    pill.className = 'px-3.5 py-1.5 rounded-xl text-xs font-medium bg-slate-900 text-slate-400 border border-slate-700 hover:border-slate-500 hover:text-slate-200 transition';
                    pill.innerHTML = `<i class="fa-solid fa-plus me-1.5 text-[10px]"></i> ${{role}}`;
                }}
                container.appendChild(pill);
            }});

            document.getElementById('active-roles-count').innerText = `${{selectedRoles.length}} of ${{allRoles.length}} Roles Selected`;
        }}

        function toggleRole(role) {{
            if (selectedRoles.includes(role)) {{
                if (selectedRoles.length > 1) {{
                    selectedRoles = selectedRoles.filter(r => r !== role);
                }} else {{
                    alert('Please keep at least one role selected.');
                    return;
                }}
            }} else {{
                selectedRoles.push(role);
            }}
            renderRolePills();
            fetchJobsForSelectedRoles();
        }}

        function selectAllRoles() {{
            selectedRoles = [...allRoles];
            renderRolePills();
            fetchJobsForSelectedRoles();
        }}

        function fetchJobsForSelectedRoles() {{
            const rolesQuery = selectedRoles.join(',');
            fetch('/api/jobs?roles=' + encodeURIComponent(rolesQuery))
            .then(res => res.json())
            .then(jobs => {{
                currentJobs = jobs;
                document.getElementById('job-count').innerText = jobs.length;
                renderJobs(jobs);
            }});
        }}

        function renderJobs(jobsList) {{
            const container = document.getElementById('jobs-grid');
            container.innerHTML = '';
            
            if (jobsList.length === 0) {{
                container.innerHTML = `<div class="col-span-2 text-center p-8 bg-slate-800 rounded-2xl border border-slate-700 text-slate-400 text-sm">No openings found for the selected roles.</div>`;
                return;
            }}

            jobsList.forEach(job => {{
                const card = document.createElement('div');
                card.className = 'bg-slate-800 p-5 rounded-2xl border border-slate-700 flex flex-col justify-between hover:border-slate-500 transition shadow-lg hover:shadow-xl';
                
                const scoreColor = job.fit_score >= 85 ? 'emerald' : (job.fit_score >= 70 ? 'blue' : 'amber');
                
                let reasonsHtml = '';
                if (job.match_reasons) {{
                    reasonsHtml = job.match_reasons.map(r => `<div><i class="fa-solid fa-check text-emerald-400 me-1"></i> ${{r}}</div>`).join('');
                }}

                card.innerHTML = `
                    <div>
                        <div class="flex justify-between items-start mb-2">
                            <div>
                                <span class="text-[11px] px-2.5 py-0.5 bg-blue-950 text-blue-300 border border-blue-800 rounded-md font-semibold">${{job.role_category}}</span>
                                <h3 class="text-base font-bold text-white mt-1.5">${{job.title}}</h3>
                                <p class="text-xs text-blue-400 font-semibold mt-0.5">${{job.company}} • <span class="text-slate-400">${{job.location}}</span></p>
                            </div>
                            <span class="px-3 py-1 bg-${{scoreColor}}-500/20 text-${{scoreColor}}-400 border border-${{scoreColor}}-500/40 text-xs font-extrabold rounded-xl">
                                ${{job.fit_score}}% Fit
                            </span>
                        </div>

                        <!-- Portal Source Tag -->
                        <div class="flex items-center space-x-2 my-2.5">
                            <span class="text-[10px] px-2 py-0.5 bg-slate-900 text-slate-300 border border-slate-700 rounded flex items-center font-medium">
                                <i class="fa-solid fa-globe me-1 text-slate-400"></i> Portal: <b class="ms-1 text-white">${{job.portal}}</b>
                            </span>
                        </div>

                        <p class="text-xs text-slate-300 line-clamp-3 mb-3 bg-slate-900/60 p-3 rounded-xl border border-slate-800/80 font-sans leading-relaxed">
                            ${{job.description}}
                        </p>

                        <div class="text-[11px] text-slate-400 space-y-1 mb-4">
                            ${{reasonsHtml}}
                        </div>
                    </div>

                    <!-- Action Buttons -->
                    <div class="flex space-x-2 pt-3 border-t border-slate-700/80">
                        <button onclick="selectForATS('${{job.id}}')" class="flex-1 py-2.5 bg-blue-600 hover:bg-blue-500 text-white rounded-xl text-xs font-bold transition flex items-center justify-center shadow-md">
                            <i class="fa-solid fa-wand-magic-sparkles me-1.5"></i> Optimize Resume
                        </button>
                        <a href="${{job.url}}" target="_blank" rel="noopener noreferrer" class="px-4 py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded-xl text-xs flex items-center justify-center transition shadow-lg shadow-emerald-900/40">
                            <i class="fa-solid fa-paper-plane me-1.5"></i> Apply on ${{job.portal.split('.')[0]}} <i class="fa-solid fa-arrow-up-right-from-square text-[10px] ms-1.5 opacity-90"></i>
                        </a>
                    </div>
                `;
                container.appendChild(card);
            }});
        }}

        function switchTab(tabName) {{
            ['jobs', 'ats', 'weekly'].forEach(t => {{
                document.getElementById('view-' + t).classList.add('hidden');
                document.getElementById('tab-' + t).className = 'py-3 px-5 text-sm font-bold border-b-2 border-transparent text-slate-400 hover:text-slate-200 focus:outline-none flex items-center transition';
            }});

            document.getElementById('view-' + tabName).classList.remove('hidden');
            document.getElementById('tab-' + tabName).className = 'py-3 px-5 text-sm font-bold border-b-2 border-blue-500 text-blue-400 focus:outline-none flex items-center transition';
        }}

        function selectForATS(jobId) {{
            const job = currentJobs.find(j => j.id === jobId);
            if (job) {{
                document.getElementById('ats-job-title').value = job.title + ' - ' + job.company;
                document.getElementById('ats-jd-text').value = job.description;
                switchTab('ats');
                runATSOptimizer(job);
            }}
        }}

        function runATSOptimizer(jobObj = null) {{
            const jd = document.getElementById('ats-jd-text').value;
            const title = document.getElementById('ats-job-title').value;
            
            const payload = {{
                jd: jd,
                job: jobObj || {{ title: title, company: title.split('-')[1] || 'Target Firm' }}
            }};

            fetch('/api/optimize', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify(payload)
            }})
            .then(res => res.json())
            .then(data => {{
                document.getElementById('ats-score-badge').innerText = data.analysis.ats_match_percentage + '%';
                
                const recContainer = document.getElementById('ats-recommendations');
                recContainer.innerHTML = '';
                data.analysis.recommendations.forEach(r => {{
                    recContainer.innerHTML += `
                        <div class="p-3 bg-slate-950 rounded-xl border border-slate-800">
                            <span class="font-bold text-blue-400 block mb-1">${{r.category}}</span>
                            <p class="text-slate-300 mb-1">${{r.issue}}</p>
                            <p class="text-emerald-400 font-medium">💡 Recommendation: ${{r.action}}</p>
                        </div>
                    `;
                }});

                document.getElementById('cover-letter-box').innerText = data.cover_letter;
            }});
        }}

        function renderWeeklyReport() {{
            const strengthsBox = document.getElementById('weekly-strengths');
            strengthsBox.innerHTML = weeklyReportData.matched_strengths.map(s => `
                <div class="p-2.5 bg-slate-950 rounded-xl text-xs flex justify-between border border-slate-800">
                    <span class="text-slate-200 font-medium">${{s.skill}}</span>
                    <span class="text-emerald-400 font-semibold">${{s.demand_frequency}}</span>
                </div>
            `).join('');

            const gapsBox = document.getElementById('weekly-gaps');
            gapsBox.innerHTML = weeklyReportData.skill_gaps.map(g => `
                <div class="p-2.5 bg-slate-950 rounded-xl text-xs flex justify-between border border-slate-800">
                    <span class="text-slate-200 font-medium">${{g.skill}}</span>
                    <span class="text-amber-400 font-semibold">${{g.demand_frequency}}</span>
                </div>
            `).join('');

            const actionsBox = document.getElementById('weekly-actions');
            actionsBox.innerHTML = weeklyReportData.recommended_weekly_actions.map(a => `
                <div class="p-3 bg-slate-950 rounded-xl border border-slate-800 leading-relaxed">${{a}}</div>
            `).join('');
        }}

        function copyCoverLetter() {{
            const text = document.getElementById('cover-letter-box').innerText;
            navigator.clipboard.writeText(text);
            alert('Cover letter copied to clipboard!');
        }}

        // Initialize UI
        renderRolePills();
        renderJobs(currentJobs);
        renderWeeklyReport();
        runATSOptimizer();
    </script>
</body>
</html>
        """

if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), DashboardHandler) as httpd:
        print(f"Abhilash Career Suite Dashboard running at http://localhost:{PORT}")
        httpd.serve_forever()
