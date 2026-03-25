import pandas as pd
from jobspy import scrape_jobs
from datetime import datetime
import time

def scrape_soham_jobs_national():
    # 1. Keywords updated with Junior/Associate roles
    search_queries = [
        "Software Engineer",
        "Junior Software Engineer",
        "Associate Software Engineer",
        "Java Developer",
        "PL/SQL Developer",
        "ServiceNow Developer"
    ]

    all_jobs_list = []
    print(f"🚀 Starting NATIONAL Scrape at {datetime.now().strftime('%H:%M:%S')}...")

    for query in search_queries:
        print(f"🔍 Searching USA for: '{query}'...")
        try:
            # location="USA" triggers a national search on most boards
            jobs = scrape_jobs(
                site_name=["linkedin", "indeed", "glassdoor"],
                search_term=query,
                location="USA", 
                results_wanted=25,    # Increased because USA is a huge market
                hours_old=24,         #  hours old, can be changed.
                country_around="USA",
                is_remote=False,      # Set to False to get BOTH on-site and remote
            )
            
            if not jobs.empty:
                print(f"✅ Found {len(jobs)} jobs for '{query}'")
                all_jobs_list.append(jobs)
            
            time.sleep(1) # Safety delay
        except Exception as e:
            print(f"❌ Error with {query}: {e}")

    if not all_jobs_list:
        print("No jobs found. Check your internet or library version.")
        return

    # 2. Combine and Clean
    df = pd.concat(all_jobs_list, ignore_index=True)
    df = df.drop_duplicates(subset=['title', 'company'])

    # 3. Visa Sponsorship Detection Logic
    # This checks the description for common F-1/H1-B terms
    def detect_visa_info(row):
        desc = str(row.get('description', '')).lower()
        if any(x in desc for x in ["sponsorship", "h1-b", "h1b", "opt ", "cpt ", "visa"]):
            return "⚠️ Mentioned"
        return "Not mentioned"

    df['visa_info'] = df.apply(detect_visa_info, axis=1)

    # 4. Save JSON for Autofiller
    df.to_json("jobs_data.json", orient="records", indent=4)

    # 5. Build Improved HTML Dashboard
    html_table = ""
    for _, row in df.iterrows():
        # Color code the Visa Info
        visa_style = "color: #d9534f; font-weight: bold;" if "Mentioned" in row['visa_info'] else "color: #777;"
        
        html_table += f"""
        <tr>
            <td><b>{row['title']}</b></td>
            <td>{row['company']}</td>
            <td>{row['location']}</td>
            <td style="{visa_style}">{row['visa_info']}</td>
            <td><a href="{row['job_url']}" target="_blank">Apply Now ↗</a></td>
        </tr>
        """

    full_html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; background-color: #f8f9fa; }}
            .container {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            h2 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th {{ background-color: #3498db; color: white; text-align: left; padding: 12px; }}
            td {{ padding: 12px; border-bottom: 1px solid #eee; }}
            tr:hover {{ background-color: #f1f1f1; }}
            a {{ background: #3498db; color: white; padding: 5px 10px; border-radius: 4px; text-decoration: none; font-size: 13px; }}
            a:hover {{ background: #2980b9; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>🎯 National Job Leads for Soham Ghosh</h2>
            <p>Total unique jobs found: <b>{len(df)}</b> | Location: <b>Anywhere in USA</b></p>
            <table>
                <tr>
                    <th>Position</th>
                    <th>Company</th>
                    <th>Location</th>
                    <th>Visa Mention?</th>
                    <th>Link</th>
                </tr>
                {html_table}
            </table>
        </div>
    </body>
    </html>
    """

    with open("job_dashboard.html", "w", encoding="utf-8") as f:
        f.write(full_html)

    print(f"\n✅ National Dashboard ready: Open 'job_dashboard.html' to see {len(df)} jobs.")

if __name__ == "__main__":
    scrape_soham_jobs_national()
