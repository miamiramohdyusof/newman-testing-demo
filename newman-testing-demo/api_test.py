import sys
import subprocess
import json
import os

# Load configuration from config.json
with open("config.json", "r") as config_file:
    config = json.load(config_file)

collections = config["collections"]
env_mapping = config["env_mapping"]

# Get user input for collection and environment
collection_choice = sys.argv[1] if len(sys.argv) > 1 else None
env_choice = sys.argv[2] if len(sys.argv) > 2 else "SIT"

# Validate collection choice
if collection_choice not in collections:
    print(f"❌ Invalid collection name! Choose from: {', '.join(collections.keys())}")
    sys.exit(1)

# Get collection and environment
collection = collections[collection_choice]
environment = env_mapping.get(env_choice.upper(), "sit_env.json")

# Create a folder for the collection (if it doesn't exist)
report_folder = f"reports/{collection_choice}"
os.makedirs(report_folder, exist_ok=True)

# Function to run a specific Postman collection
def run_postman_test():
    report_file = f"{report_folder}/report_{collection_choice}.json"

    print(f"🚀 Running Postman test for: {collection} on {env_choice} environment")
    print(f"📁 Saving report in: {report_file}")

    try:
        subprocess.run(
            [
                "newman", "run", collection,
                "-e", environment,
                "--reporters", "cli,json",
                "--reporter-json-export", report_file,
                "--insecure"
            ],
            check=True
        )
        print(f"✅ Postman test completed successfully for {collection}. Report saved at {report_file}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running Postman test for {collection}:", e)

# Run the script
if __name__ == "__main__":
    run_postman_test()
