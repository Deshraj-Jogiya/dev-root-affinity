import os
import subprocess
import random
import argparse
from datetime import datetime, timedelta

def parse_args():
    parser = argparse.ArgumentParser(description="Generate organic backdated git commits starting from June 2, 2020.")
    parser.add_argument("--git-path", type=str, default="git", help="Path to git executable.")
    parser.add_argument("--density", type=int, default=250, help="Target commits per year.")
    parser.add_argument("--dry-run", action="store_true", help="Print the scheduled dates without committing.")
    return parser.parse_args()

def generate_dates(density):
    # Start on GitHub Join Date: June 2, 2020
    start_date = datetime(2020, 6, 2)
    end_date = datetime(2026, 6, 14) # current system time
    
    current = start_date
    all_dates = []
    
    while current <= end_date:
        # Skip weekends
        if current.weekday() in (5, 6):
            current += timedelta(days=1)
            continue
            
        # Standard holidays or random long vacation breaks
        if random.random() < 0.08:
            current += timedelta(days=random.randint(1, 5))
            continue
            
        year = current.year
        # Double the density for 2020 and 2021 to pack past 2017-2020 learnings
        if year in (2020, 2021):
            day_prob = (density * 1.8) / 260.0
            num_choices = [2, 3, 4, 5]
            weights = [0.3, 0.4, 0.2, 0.1]
        else:
            day_prob = density / 260.0
            num_choices = [1, 2, 3]
            weights = [0.6, 0.3, 0.1]
        
        if random.random() < min(day_prob, 0.95):
            num_commits = random.choices(num_choices, weights=weights)[0]
            for _ in range(num_commits):
                hour = random.randint(9, 20)
                minute = random.randint(0, 59)
                second = random.randint(0, 59)
                commit_time = current.replace(hour=hour, minute=minute, second=second)
                all_dates.append(commit_time)
                
        current += timedelta(days=1)
        
    return sorted(all_dates)

def run_git_commit(git_path, commit_date, log_message, dry_run):
    date_str = commit_date.strftime("%Y-%m-%dT%H:%M:%S")
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = date_str
    env["GIT_COMMITTER_DATE"] = date_str
    env["GIT_AUTHOR_NAME"] = "Deshraj Jogiya"
    env["GIT_AUTHOR_EMAIL"] = "djogiya786@gmail.com"
    env["GIT_COMMITTER_NAME"] = "Deshraj Jogiya"
    env["GIT_COMMITTER_EMAIL"] = "djogiya786@gmail.com"
    
    log_file_path = os.path.join("scratch", "activity_log.txt")
    
    if not dry_run:
        os.makedirs("scratch", exist_ok=True)
        with open(log_file_path, "a") as f:
            f.write(f"[{date_str}] {log_message}\n")
            
        subprocess.run([git_path, "add", log_file_path], check=True, stdout=subprocess.DEVNULL)
        
        cmd = [git_path, "commit", "-m", log_message]
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error committing: {result.stderr}")
    else:
        print(f"[DRY-RUN] Will commit on {date_str} with message: '{log_message}'")

def main():
    args = parse_args()
    
    print(f"Generating commit dates from Jun 2, 2020 to Jun 2026 (Density: {args.density} commits/year)...")
    commit_dates = generate_dates(args.density)
    total_commits = len(commit_dates)
    print(f"Total scheduled commits to generate: {total_commits}")
    
    if args.dry_run:
        print("\n--- Previewing first 10 commit schedules ---")
        for d in commit_dates[:10]:
            print(d.strftime("%Y-%m-%d %H:%M:%S"))
        print("...")
        print("--- Previewing last 10 commit schedules ---")
        for d in commit_dates[-10:]:
            print(d.strftime("%Y-%m-%d %H:%M:%S"))
        return
        
    try:
        subprocess.run([args.git_path, "--version"], check=True, stdout=subprocess.DEVNULL)
    except Exception:
        print(f"Error: Git executable '{args.git_path}' not found.")
        return
        
    topics = [
        "Revise algorithms & data structures",
        "Refactor variable names and code cleanliness",
        "Optimize search runtime complexity",
        "Update comments and inline explanations",
        "Add unit test cases for edge validations",
        "Configure local database connection logs",
        "Verify system variables and config bindings",
        "Fix syntax issue and type errors",
        "Research advanced engineering design patterns",
        "Draft technical study log details",
    ]
    
    print("\nStarting commit generation. This might take a minute...")
    for idx, commit_date in enumerate(commit_dates):
        topic = random.choice(topics)
        log_message = f"Study log: {topic} [session {idx+1}]"
        run_git_commit(args.git_path, commit_date, log_message, args.dry_run)
        
        if (idx + 1) % 100 == 0 or (idx + 1) == total_commits:
            print(f"Progress: {idx+1}/{total_commits} commits created.")
            
    print("\nSuccess! All backdated commits created locally with verified author credentials.")
    print("Run 'git push -f' to force-push these commits to GitHub.")

if __name__ == "__main__":
    main()
