import requests
import google.auth
import google.auth.transport.requests

def query_agent():
    # 1. Get Credentials from your gcloud login environment
    try:
        credentials, project = google.auth.default()
        auth_request = google.auth.transport.requests.Request()
        credentials.refresh(auth_request)
    except Exception as e:
        print(f"Authentication Error: {e}")
        return

    # 2. Your specific Agent URL
    url = "https://us-central1-aiplatform.googleapis.com/v1/projects/<gcp-project-id>/locations/us-central1/reasoningEngines/<agent-id>:query"

    # 3. Prepare Payload
    # The REST API requires 'input' to be a Struct (dictionary)
    headers = {
        "Authorization": f"Bearer {credentials.token}",
        "Content-Type": "application/json"
    }
    
    # Corrected structure: The API expects an 'input' key 
    # containing a dictionary of arguments.
    data = {
        "input": {
            "input": "How much is 100 EUR in USD?"
        }
    }

    # 4. Execute the Request
    print(f"Connecting to Agent Registry at: {url}\n")
    
    try:
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            print("✅ Success!")
            result = response.json()
            # The output usually resides in result['output']
            print("\nAgent Response:")
            print(result.get("output", result))
        else:
            print(f"❌ Error {response.status_code}")
            print("Response details:")
            print(response.text)
            
    except requests.exceptions.RequestException as e:
        print(f"Network Error: {e}")

if __name__ == "__main__":
    query_agent()
