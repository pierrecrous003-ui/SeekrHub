import os
import shutil

ROOT = os.path.join(os.getcwd(), "people")

def main():
    deleted = 0

    for root, dirs, files in os.walk(ROOT):
        if "insights" in dirs:
            insight_path = os.path.join(root, "insights")

            print(f"🗑️  Deleting: {insight_path}")
            shutil.rmtree(insight_path)

            deleted += 1

    print("\n==============================")
    print(f"🔥 Deleted {deleted} insight folders")
    print("==============================")

if __name__ == "__main__":
    main()
