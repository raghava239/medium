import vertexai
from vertexai import agent_engines
from vertexai.preview import reasoning_engines

# --- 1. CONFIGURATION ---
PROJECT_ID = "YOUR_GCP_PROJECT_ID"
LOCATION = "us-central1"
STAGING_BUCKET = "gs://YOUR_BUCKET_NAME"

vertexai.init(project=PROJECT_ID, location=LOCATION, staging_bucket=STAGING_BUCKET)

# --- 2. PRECISION TOOL DEFINITION ---
def get_live_exchange_rates(base_currency: str, target_currency: str = None) -> dict:
    """
    Fetches real-time exchange rates. 
    Args:
        base_currency: The ISO code of the source currency (e.g., USD).
        target_currency: Optional ISO code of the destination currency (e.g., INR).
    """
    import requests
    # Secure your API Key: Replace the placeholder below with your actual key
    api_key = "YOUR_EXCHANGERATE_API_KEY" 
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency.upper()}"
    
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("result") == "success":
            rates = data.get("conversion_rates", {})
            
            # If the user asked for a specific target, return ONLY that to reduce noise
            if target_currency and target_currency.upper() in rates:
                return {
                    "base": base_currency.upper(),
                    "target": target_currency.upper(),
                    "rate": rates[target_currency.upper()]
                }
            return rates
        return {"error": "API Error: " + data.get("error-type", "Unknown")}
    except Exception as e:
        return {"error": str(e)}

# --- 3. ENHANCED AGENT ARCHITECTURE ---
agent = agent_engines.LangchainAgent(
    model="gemini-2.5-flash", 
    tools=[get_live_exchange_rates],
    model_kwargs={
        "system_instruction": (
            "You are a Global Currency Strategist. Use the get_live_exchange_rates tool for all requests. "
            "If a user asks for a specific conversion (e.g., INR to USD), pass BOTH the base_currency "
            "and the target_currency to the tool to get a precise result. "
            "Present your final answer clearly, and if multiple rates are returned, use a Markdown table."
        )
    }
)

# --- 4. DEPLOYMENT ---
print(f"Deploying Optimized Gemini 2.5 Flash Agent...")

remote_agent = reasoning_engines.ReasoningEngine.create(
    agent,
    requirements=[
        "google-cloud-aiplatform[reasoningengine,langchain]>=1.48.0",
        "cloudpickle==3.0.0",
        "pydantic>=2.0.0",
        "requests"
    ],
    display_name="Global_Currency_Precision_V7",
    sys_version="3.11"
)

print("-" * 30)
print(f"✅ Deployment Successful!")
print(f"Agent Resource Name: {remote_agent.resource_name}")
print("-" * 30)
