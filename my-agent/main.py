import vertexai
from vertexai import agent_engines
from vertexai.preview import reasoning_engines

# --- 1. CONFIGURATION ---
# Redacted: Use your specific Google Cloud Project ID and Region
PROJECT_ID = "YOUR_PROJECT_ID"
LOCATION = "us-central1"
# Redacted: Ensure this bucket exists in your project
STAGING_BUCKET = "gs://YOUR_BUCKET_NAME"

# Initialize Vertex AI with your project and staging bucket
vertexai.init(
    project=PROJECT_ID, 
    location=LOCATION, 
    staging_bucket=STAGING_BUCKET
)

# --- 2. TOOL DEFINITION ---
def get_exchange_rate(currency_from: str, currency_to: str) -> str:
    """
    Fetches the current exchange rate between two currencies.
    Args:
        currency_from: The ISO code of the base currency (e.g., USD).
        currency_to: The ISO code of the target currency (e.g., EUR).
    """
    # Mock logic for the exercise
    rates = {
        ("USD", "EUR"): "0.92",
        ("EUR", "USD"): "1.08",
        ("GBP", "USD"): "1.27"
    }
    return rates.get((currency_from.upper(), currency_to.upper()), "Rate not found.")

# --- 3. AGENT ARCHITECTURE ---
# Using the stable Gemini 1.5 Flash model
agent = agent_engines.LangchainAgent(
    model="gemini-2.5-flash",
    tools=[get_exchange_rate],
    model_kwargs={
        "system_instruction": "You are a professional currency assistant. Use tools for rates."
    }
)

# --- 4. DEPLOYMENT TO REGISTRY ---
print(f"Deploying agent to Reasoning Engine Registry...")

# Note: service_account is managed via IAM roles on the 
# Reasoning Engine Service Agent, not passed as a parameter here.
remote_agent = reasoning_engines.ReasoningEngine.create(
    agent,
    requirements=[
        "google-cloud-aiplatform[reasoningengine,langchain]>=1.48.0",
        "cloudpickle==3.0.0",
        "pydantic>=2.0.0",
        "requests"
    ],
    display_name="Currency_Agent_Final_V4",
    sys_version="3.11"
)

print("-" * 30)
print(f"✅ Deployment Successful!")
print(f"Agent Resource Name: {remote_agent.resource_name}")
print("-" * 30)
