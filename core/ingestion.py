import os
import shutil
import stat
import git

def remove_readonly(func, path, excinfo):
    """
    Error handler for shutil.rmtree to handle Windows read-only file locks.
    """
    os.chmod(path, stat.S_IWRITE)
    func(path)

def clone_repository(repo_url: str, target_dir: str) -> str:
    """
    Clones a public GitHub repository down to a local target folder.
    Cleans up conflicting existing directories gracefully on Windows.
    """
    if os.path.exists(target_dir):
        print(f"🧹 Clearing existing folder paths: {target_dir}")
        # onerror=remove_readonly forces Windows to unlock hidden Git index packs
        shutil.rmtree(target_dir, onerror=remove_readonly)
        
    try:
        print(f"📥 Agent initiating clone for: {repo_url}...")
        git.Repo.clone_from(repo_url, target_dir, depth=1)
        print("✅ Repository cloned successfully!")
        return target_dir
    except Exception as e:
        raise RuntimeError(f"Ingestion failed while cloning repository: {str(e)}")

def get_all_python_files(directory: str):
    """
    Scans the downloaded folder recursively and collects paths to all Python files.
    """
    python_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files