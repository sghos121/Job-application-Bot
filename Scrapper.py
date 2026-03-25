import pandas as pd
from jobspy import scrape_jobs
from datetime import datetime
import os

def scrape_soham_jobs():
    search_queries = [
        "Software Engineer",
        "Junior Software Engineer",
        "Java Developer",
        "PL/SQL Developer",
        "ServiceNow Developer"
    ]

    all_jobs = []
    print(f"🚀 Scraping started at {datetime.now().strftime('%H:%M:%S')}...")

    for query in search_queries:
        print(f"🔍 Searching: {query}")
        try:
            jobs = scrape_jobs(
                site_name=["linkedin", "indeed", "glassdoor"],
                search_term=query,
                location="Tempe, AZ",
                distance=50,
                results_wanted=15,
                hours_old=72,
                country_around="USA",
                is_remote=True
            )
            all_jobs.append(jobs)
        except Exception as e:
            print(f"❌ Error with {query}: {e}")

    if not all_jobs:
        print("No jobs found.")
        return

    # 1. Combine and Clean
    df = pd.concat(all_jobs, ignore_index=True)
    df = df.drop_duplicates(subset=['title', 'company'])

    # 2. Keep only the columns YOU care about
    # Note: JobSpy column names might vary slightly, so we use a safe list
    cols_to_keep = ['title', 'company', 'location', 'date_posted', 'job_url', 'site']
    existing_cols = [c for c in cols_to_keep if c in df.columns]
    df = df[existing_cols]

    # 3. Add a "Status" column for your tracking
    df['status'] = "Pending"

    # 4. Export to JSON (For the Autofill Bot later)
    df.to_json("jobs_data.json", orient="records", indent=4)

    # 5. Export to a Clean HTML Dashboard (For YOU)
    html_table = df.to_html(index=False, render_links=True, classes='job-table')
    
    html_content = f"""
    <html>
    <head>
        <title>Soham's Job Dashboard</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f4f4f9; }}
            h2 {{ color: #333; }}
            .job-table {{ width: 100%; border-collapse: collapse; background: white; }}
            .job-table th, .job-table td {{ padding: 12px; border: 1px solid #ddd; text-align: left; }}
            .job-table th {{ background-color: #0073b1; color: white; }}
            .job-table tr:nth-child(even) {{ background-color: #f2f2f2; }}
            a {{ color: #0073b1; text-decoration: none; font-weight: bold; }}
            a:hover {{ text-decoration: underline; }}
        </style>
    </head>
    <body>
        <h2>🎯 Job Leads for Soham Ghosh ({datetime.now().strftime('%Y-%m-%d')})</h2>
        <p>Found {len(df)} unique jobs. Click the link to open the application.</p>
        {html_table}
    </body>
    </html>
    """

    with open("job_dashboard.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print("\n" + "="*40)
    print(f"✅ DONE!")
    print(f"1. Open 'job_dashboard.html' in your browser to see your jobs.")
    print(f"2. 'jobs_data.json' created for the Autofiller.")
    print("="*40)

if __name__ == "__main__":
    scrape_soham_jobs()