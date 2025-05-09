import subprocess
import os

# Step 1: Save the current branch name
current_branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode().strip()

# Step 2: Run the Natural Docs process to generate the documentation
process = subprocess.Popen(
    ["naturaldocs", "-p", "ND Config"],
    stdout=subprocess.PIPE,  # Capture standard output
    stderr=subprocess.PIPE,  # Capture standard error
    stdin=subprocess.PIPE   # Allow sending input to the process (if needed)
)

# Read output and error
stdout, stderr = process.communicate()

# Check if there are any errors
if stderr:
    print("Error during Natural Docs execution:", stderr.decode())
else:
    print("Natural Docs completed successfully.")

# Step 3: Switch to the `Docs` branch
try:
    subprocess.run(["git", "checkout", "Docs"], check=True)
    print("Switched to Docs branch.")
except subprocess.CalledProcessError as e:
    print("Failed to switch to Docs branch:", e)

# Step 4: Add the generated HTML files to the staging area
# You might want to specify the directory where the HTML files are saved
# For example, assuming the docs are in "Docs/" folder:
html_dir = "Docs/"  # Change this to the actual directory where your HTML files are
subprocess.run(["git", "add", html_dir], check=True)
print(f"Added {html_dir} to staging area.")

# Step 5: Commit the changes
commit_message = "Updated documentation"
subprocess.run(["git", "commit", "-m", commit_message], check=True)
print("Committed the changes.")

# Step 6: Push the changes to the remote repository
subprocess.run(["git", "push"], check=True)
print("Pushed the changes to the remote repository.")

# Step 7: Switch back to the original branch
try:
    subprocess.run(["git", "checkout", current_branch], check=True)
    print(f"Switched back to the original branch: {current_branch}")
except subprocess.CalledProcessError as e:
    print(f"Failed to switch back to the original branch: {e}")
