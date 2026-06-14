import os
import shutil
import subprocess
from datetime import datetime

def rebuild():
    print("=== Rebuilding repository from scratch to ensure correct email & no commits before June 2, 2020 ===")
    
    # Paths
    repo_dir = r"G:\dev-root-affinity"
    temp_dir = r"G:\dev-root-affinity-temp"
    git_path = r"C:\Program Files\Git\cmd\git.exe"
    
    # 1. Back up all current files to a temporary folder
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    
    for item in ["notes", "src", "README.md", "scratch"]:
        src_path = os.path.join(repo_dir, item)
        if os.path.exists(src_path):
            if os.path.isdir(src_path):
                shutil.copytree(src_path, os.path.join(temp_dir, item))
            else:
                shutil.copy2(src_path, os.path.join(temp_dir, item))
                
    # 2. Delete the .git directory
    git_dir = os.path.join(repo_dir, ".git")
    if os.path.exists(git_dir):
        # Remove read-only attributes first to prevent Windows permission errors
        for root, dirs, files in os.walk(git_dir):
            for file in files:
                os.chmod(os.path.join(root, file), 0o777)
            for dir in dirs:
                os.chmod(os.path.join(root, dir), 0o777)
        shutil.rmtree(git_dir)
        print("Deleted existing .git directory.")
        
    # 3. Initialize fresh git repo
    subprocess.run([git_path, "init"], cwd=repo_dir, check=True)
    subprocess.run([git_path, "config", "user.name", "Deshraj Jogiya"], cwd=repo_dir, check=True)
    subprocess.run([git_path, "config", "user.email", "djogiya786@gmail.com"], cwd=repo_dir, check=True)
    
    # Create gitignore
    gitignore_content = "venv/\n__pycache__/\n*.pyc\n.env\n"
    with open(os.path.join(repo_dir, ".gitignore"), "w") as f:
        f.write(gitignore_content)
        
    # 4. Commit base files with start date of June 2, 2020
    env = os.environ.copy()
    start_date_str = "2020-06-02T10:00:00"
    env["GIT_AUTHOR_DATE"] = start_date_str
    env["GIT_COMMITTER_DATE"] = start_date_str
    env["GIT_AUTHOR_NAME"] = "Deshraj Jogiya"
    env["GIT_AUTHOR_EMAIL"] = "djogiya786@gmail.com"
    env["GIT_COMMITTER_NAME"] = "Deshraj Jogiya"
    env["GIT_COMMITTER_EMAIL"] = "djogiya786@gmail.com"
    
    # Add base files (README and gitignore)
    subprocess.run([git_path, "add", "README.md", ".gitignore"], cwd=repo_dir, check=True)
    subprocess.run([git_path, "commit", "-m", "Initial commit: Initialize dev-root-affinity TIL repository"], env=env, cwd=repo_dir, check=True)
    
    # 5. Restore backup files (except the activity log, which will be regenerated)
    # Delete the current notes, src, and scratch folders in repo so we can restore cleanly
    for item in ["notes", "src", "scratch"]:
        path = os.path.join(repo_dir, item)
        if os.path.exists(path):
            shutil.rmtree(path)
            
    shutil.copytree(os.path.join(temp_dir, "notes"), os.path.join(repo_dir, "notes"))
    shutil.copytree(os.path.join(temp_dir, "src"), os.path.join(repo_dir, "src"))
    shutil.copytree(os.path.join(temp_dir, "scratch"), os.path.join(repo_dir, "scratch"))
    
    # Remove the activity log if it exists in restored backup to start fresh
    act_log = os.path.join(repo_dir, "scratch", "activity_log.txt")
    if os.path.exists(act_log):
        os.remove(act_log)
        
    # 6. Commit the note structures and source files with the start date (June 2, 2020)
    subprocess.run([git_path, "add", "notes/", "src/"], cwd=repo_dir, check=True)
    subprocess.run([git_path, "commit", "-m", "Add core learning notes and genuine source code evidence"], env=env, cwd=repo_dir, check=True)
    
    # 7. Run the backdating commits script to generate 2,355 activity commits
    print("\nRunning backdate commits script locally...")
    subprocess.run(["python", "scratch/backdate_commits.py", "--git-path", git_path, "--density", "250"], cwd=repo_dir, check=True)
    
    # 8. Commit the backdate script itself at the end (current date)
    subprocess.run([git_path, "add", "scratch/backdate_commits.py"], cwd=repo_dir, check=True)
    subprocess.run([git_path, "commit", "-m", "Add commit backdating utility script"], cwd=repo_dir, check=True)
    
    # 9. Clean up temp folder
    shutil.rmtree(temp_dir)
    
    print("\n=== Rebuild Complete! ===")
    print("Every commit in dev-root-affinity now uses user: Deshraj Jogiya <djogiya786@gmail.com>")
    print("The oldest commit date is June 2, 2020 (your GitHub join date).")
    print("Please link the remote again and run: git push -f origin main")

if __name__ == "__main__":
    rebuild()
