import os
from openai import OpenAI
import requests

# Load API keys from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_API_KEY")
LINKEDIN_MEMBER_URN = os.getenv("LINKEDIN_MEMBER_URN")  # Format: "urn:li:person:xxxxxxxx"

# Configure OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_gpt_response(prompt):
    """Send prompt to OpenAI GPT and return the response (new API syntax)."""
    response = client.chat.completions.create(
        model="gpt-4",  # or "gpt-3.5-turbo"
        messages=[
            {"role": "system", "content": "You are a professional LinkedIn content writer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=500
    )
    return response.choices[0].message.content.strip()

def post_to_linkedin(message):
    """Publish a post to LinkedIn."""
    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        "Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}",
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json"
    }
    payload = {
        "author": LINKEDIN_MEMBER_URN,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": message
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 201:
        print("✅ Successfully posted to LinkedIn!")
    else:
        print("❌ Failed to post:", response.status_code)
        print(response.text)

if __name__ == "__main__":
    user_prompt = input("🗨️  What would you like ChatGPT to write a LinkedIn post about?\n> ")
    gpt_output = get_gpt_response(user_prompt)

    print("\n📝 GPT-generated post:\n")
    print(gpt_output)

    confirm = input("\nPost this to LinkedIn? (y/n): ").strip().lower()
    if confirm == 'y':
        post_to_linkedin(gpt_output)