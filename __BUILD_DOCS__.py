import subprocess
import os
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


# Add the generated HTML files to the staging area
html_dir = "Docs/"
subprocess.run(["git", "add", html_dir], check=True)
print(f"Added {html_dir} to staging area.")

# Step 5: Commit the changes
commit_message = "Updated documentation"
subprocess.run(["git", "commit", "-m", commit_message], check=True)
print("Committed the changes.")

# Step 6: Push the changes to the remote repository
subprocess.run(["git", "push"], check=True)
print("Pushed the changes to the remote repository.")

