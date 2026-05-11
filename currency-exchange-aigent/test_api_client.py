import requests
import google.auth
import google.auth.transport.requests
import sys

def query_agent():
    # 1. Capture the input from the command line
    # This turns your script into a dynamic CLI tool
    user_query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "How much is 100 EUR in USD?"

    # 2. Get Credentials from your local gcloud auth session
    try:
        credentials, project = google.auth.default()
        auth_request = google.auth.transport.requests.Request()
        credentials.refresh(auth_request)
    except Exception as e:
        print(f"Authentication Error: {e}")
        return

    # 3. Your specific Agent URL
    # Replace these placeholders with your actual Project and Agent IDs
    PROJECT_ID = "<YOUR_PROJECT_ID>"
    AGENT_ID = "<YOUR_AGENT_ID>" 
    
    url = f"https://us-central1-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/us-central1/reasoningEngines/{AGENT_ID}:query"

    headers = {
        "Authorization": f"Bearer {credentials.token}",
        "Content-Type": "application/json"
    }
    
    # The Reasoning Engine REST API expects the query wrapped in an 'input' key
    data = {
        "input": {
            "input": user_query
        }
    }

    print(f"🚀 Sending Query: '{user_query}'")
    
    try:
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ Agent Response:")
            # Extracting the 'output' string from the Gemini response
            print(result.get("output", result))
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"Network Error: {e}")

if __name__ == "__main__":
    query_agent()
