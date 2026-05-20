from core.ingestion import clone_repository, get_all_python_files

# Test with a very small, simple public repository
TEST_REPO = "https://github.com/octocat/Spoon-Knife"
TARGET_FOLDER = "./cloned_repos/test_target"

try:
    download_path = clone_repository(TEST_REPO, TARGET_FOLDER)
    files = get_all_python_files(download_path)
    print(f"📂 Found {len(files)} Python files in this repository.")
except Exception as e:
    print(f"❌ Error encountered: {e}")