
Building and Testing LLM Agents: A Practical Guide to the Model Context Protocol (MCP)
Author: Raghu Pothula — AI and Cloud Specialist

Large Language Models (LLMs) are incredibly smart, but they are traditionally isolated from real-time data. If you ask a standard model about live database records—like available hotel listings, inventory levels, or user profiles—it hits a wall.

Enter the Model Context Protocol (MCP). MCP acts as an open-standard bridge allowing LLMs to securely interact with external data sources and tools.

In this guide, we will look at the real-world implementation experience of building an autonomous AI Hotel Agent. We will cover setting up a relational database, configuring an MCP gateway server, wrapping the agent using an Agent Development Kit (ADK), and testing everything locally before pushing it to production.

🏗️ Technical Architecture Overview
To completely decouple the application logic and maximize flexibility, our system architecture follows a distinct separation of concerns:

The Core Database Engine: A relational PostgreSQL server holding our operational business data.

The MCP Server Engine: A central configuration layer that securely translates database queries into standardized, language-model-consumable tools.

The Agent App Execution Layer: An abstract runtime environment using an Agent Development Kit (ADK) to process user prompts and orchestrate functional execution.

🛠️ Step 1: Provisioning the Environment
Before diving into configuration, prepare your runtime virtual machine (VM) with the required execution runtimes and package tooling.

Initializing System Dependencies
Ensure you have Node.js/NPX and the appropriate client runtime utilities initialized on your development VM

Bash
# Update local package definitions
sudo apt update

# Initialize structural runtime environment dependencies
sudo apt install nodejs npm -y

# Verify implementation toolchain
npx --version
🗄️ Step 2: Seeding the Relational Database
Our agent needs accurate transactional data to query against. We will spin up a PostgreSQL instance and construct an operational schema representing structural hotel data properties.

Database Schema Initialization
Connect to your relational instance database pool and run the following structural schema migration:

SQL
CREATE TABLE hotels(
 id             INTEGER NOT NULL PRIMARY KEY,
 name           VARCHAR NOT NULL,
 location       VARCHAR NOT NULL,
 price_tier     VARCHAR NOT NULL,
 checkin_date   DATE    NOT NULL,
 checkout_date  DATE    NOT NULL,
 booked         BIT     NOT NULL
);
Seeding Seed Dataset
Populate the structural tables with test listings across varying regions:

SQL
INSERT INTO hotels(id, name, location, price_tier, checkin_date, checkout_date, booked)
VALUES
 (1, 'Hilton Basel', 'Basel', 'Luxury', '2024-04-20', '2024-04-22', B'0'),
 (2, 'Marriott Zurich', 'Zurich', 'Upscale', '2024-04-14', '2024-04-21', B'0'),
 (3, 'Hyatt Regency Basel', 'Basel', 'Upper Upscale', '2024-04-02', '2024-04-20', B'0'),
 (4, 'Radisson Blu Lucerne', 'Lucerne', 'Midscale', '2024-04-05', '2024-04-24', B'0'),
 (5, 'Best Western Bern', 'Bern', 'Upper Midscale', '2024-04-01', '2024-04-23', B'0'),
 (6, 'InterContinental Geneva', 'Geneva', 'Luxury', '2024-04-23', '2024-04-28', B'0'),
 (7, 'Sheraton Zurich', 'Zurich', 'Upper Upscale', '2024-04-02', '2024-04-27', B'0'),
 (8, 'Holiday Inn Basel', 'Basel', 'Upper Midscale', '2024-04-09', '2024-04-24', B'0'),
 (9, 'Courtyard Zurich', 'Zurich', 'Upscale', '2024-04-03', '2024-04-13', B'0'),
 (10, 'Comfort Inn Bern', 'Bern', 'Midscale', '2024-04-04', '2024-04-16', B'0');

⚙️ Step 3: Architecting the MCP Gateway
Instead of exposing our database directly to an LLM, we use an MCP Toolbox Server. This component reads an explicit definition layout file (tools.yaml) and securely packages parameterized queries as discoverable APIs for our core AI agent.

Binary Installation
Initialize the working workspace and pull down the platform-native server binary engine:

Bash
mkdir mcp-toolbox && cd mcp-toolbox

# Set release target version string
export VERSION=1.1.0
curl -L -o toolbox https://storage.googleapis.com/mcp-toolbox-for-databases/v$VERSION/linux/amd64/toolbox
chmod +x toolbox

# Validate binary integrity
./toolbox -v
Exposing Secure Queries via tools.yaml
Create a structure map named tools.yaml using your system editor (nano tools.yaml). This mapping instructs the MCP server on how to authenticate against data sources and structure natural-language tool parameters:

YAML
kind: source
name: my-cloud-db-source
type: cloud-sql-postgres
project: SYSTEM_INFRA_PROJECT_ID
region: us-central1
instance: hoteldb-instance
database: postgres
user: postgres
password: SECURE_DATABASE_PASSWORD
---
kind: tool
name: search-hotels-by-name
type: postgres-sql
source: my-cloud-db-source
description: Search for hotels based on name.
parameters:
  - name: name
    type: string
    description: The explicit name of the hotel.
statement: SELECT * FROM hotels WHERE name ILIKE '%' || $1 || '%';
---
kind: tool
name: search-hotels-by-location
type: postgres-sql
source: my-cloud-db-source
description: Search for hotels based on location. Result is sorted by price from least to most expensive.
parameters:
  - name: location
    type: string
    description: The geographical location or city.
statement: |
  SELECT *
  FROM hotels
  WHERE location ILIKE '%' || $1 || '%'
  ORDER BY
    CASE price_tier
      WHEN 'Midscale' THEN 1
      WHEN 'Upper Midscale' THEN 2
      WHEN 'Upscale' THEN 3
      WHEN 'Upper Upscale' THEN 4
      WHEN 'Luxury' THEN 5
      ELSE 99 
    END;
---
kind: toolset
name: my_first_toolset
tools:
  - search-hotels-by-name
  - search-hotels-by-location
Initializing the MCP Engine Gateway
Boot the database tool configuration context directly into active memory execution:

Bash
./toolbox --config "tools.yaml"
Keep a close look out for confirmation logs indicating tools are fully bound:
INFO: Initialized 2 tools: search-hotels-by-name, search-hotels-by-location
INFO: Server ready to serve!

🤖 Step 4: Structuring the Agent Application
With the database and server layers exposed via HTTP, we can now assemble our AI orchestration execution shell using the open-source Agent Development Kit (ADK) framework.

App Scaffolding Setup
Open a separate execution terminal and initialize an isolated workspace instance:

Bash
mkdir my-agents && cd my-agents
python -m venv .venv
source .venv/bin/activate

# Install the necessary underlying orchestration abstractions
pip install google-adk toolbox-core
Initialize the baseline execution layout blueprint directly from the ADK scaffolding utility command:

Bash
adk create hotel_agent_app
Follow the interactive setup engine instructions to tie it down to your current cloud infrastructure ecosystem variables.

Authoring the Agent Structure Logic
Modify the core execution wrapper definition inside your freshly generated hotel_agent_app/agent.py configuration tracking file:

Python
from google.adk.agents import Agent
from toolbox_core import ToolboxSyncClient

# Link the orchestration layer directly into our running local gateway abstraction server
toolbox = ToolboxSyncClient("http://127.0.0.1:5000")

# Pull down the functional capabilities specified in our tools file definition mapping
tools = toolbox.load_toolset('my_first_toolset')

root_agent = Agent(
    name="hotel_agent",
    model="gemini-2.5-flash",
    description="Agent to answer questions about hotels in a city or hotels by name.",
    instruction=(
        "You are a helpful agent who can answer user questions about the hotels "
        "in a specific city or hotels by name. Use the tools to answer the question."
    ),
    tools=tools,
)
🧪 Step 5: How to Test the Implementation
Testing our deployment workspace ensures that our agent can correctly route incoming intent prompts down to specific query statements.

Method A: Testing via Interactive Command-Line Interface (CLI)
From inside your my-agents root runtime directory workspace, invoke the runtime interactive cycle engine:

Bash
adk run hotel_agent_app/
This starts a direct, low-latency live chat session inside the shell terminal. You can trace step execution directly:

Plaintext
Running agent hotel_agent, type exit to exit.
[user]: I would like to search for a place to stay in Basel.
[hotel_agent]: Here are some hotels in Basel:
* Holiday Inn Basel (Upper Midscale)
* Hyatt Regency Basel (Upper Upscale)
* Hilton Basel (Luxury)
Method B: Testing via Local Web Graphical User Interface (GUI)
If you prefer validating application state behaviors through an explicit browser dashboard visual layout component, run:

Bash
adk web
This initializes a local validation panel engine dashboard at http://127.0.0.1:8000. Open this address in your browser window to test input fields, explore detailed backend runtime tracking metrics, and visualize context window data transfers.

🚀 Step 6: Deploying to Production Containers
Once local verification tests pass without error, package the configuration state layouts as standalone cloud-native microservices.

Packing and Deploying the MCP Server
Provision individual service account access privileges with strict IAM boundaries.

Bind permissions down to clear service limits: Accessing secrets and executing queries.

Deploy the container structure:

Bash
# Store sensitive structural configs into a secret manager vault
gcloud secrets create tools --data-file=tools.yaml

# Push out the running database server architecture container instance
gcloud run deploy database-toolbox-service \
  --image=us-central1-docker.pkg.dev/database-toolbox/toolbox/toolbox:latest \
  --service-account=toolbox-identity \
  --region=us-central1 \
  --set-secrets="/app/tools.yaml=tools:latest" \
  --args="--config=/app/tools.yaml","--address=0.0.0.0","--port=8080" \
  --allow-unauthenticated
Note down the resulting live production server URL returned upon completion.

Shipping the Agent App Layout
Update your local agent.py client instantiation initialization path address string from http://127.0.0.1:5000 to your newly minted production server URL.

Assemble a requirements.txt container build specification tracking dependency file inside the workspace folder:

Plaintext
google-adk
toolbox-core
Deploy the orchestrator layer globally using the ADK automation commands:

Bash
export AGENT_PATH="hotel_agent_app/"

adk deploy cloud_run \
  --project=$SYSTEM_PROJECT_ID \
  --region=us-central1 \
  --service_name=hotel-agent-service  \
  --app_name=hotel-agent-app \
  --with_ui \
  $AGENT_PATH
📈 Verification and Scale Checks

To verify your production application, use the live web dashboard URL provided at the end of the deployment script.

To ensure your environment handles data changes correctly, run a database update to see how quickly the agent adapts:

SQL
INSERT INTO hotels(id, name, location, price_tier, checkin_date, checkout_date, booked)
VALUES (11, 'Taj Falaknuma Palace', 'Hyderabad', 'Luxury', '2026-06-01', '2026-06-05', B'0');
Query the agent again about new regions like Hyderabad. Because MCP reads directly from the data source, the agent will instantly return the updated database records—with no training or fine-tuning required

