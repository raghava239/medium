# Role: GCP AI and Cloud Specialist

## Summary of Executed Commands & Actions

### 1. Environment Setup
* **Configuration:** Created `dev-env.json` with strict compliance rules (Class A IP ranges, environment labeling, firewall requirements).
* **Authentication:** Set up service account authentication using a JSON key file located at `/home/[USER_NAME]/keys/terraform-svc-key.json`.
* **Target Project:** Identified the target GCP Project: `[PROJECT_ID]`.

### 2. Infrastructure Provisioning (Terraform)
* **Networking:** Created a VPC (`dev-vpc`), a primary subnet (`10.10.0.0/24`), and a required regional proxy-only subnet (`10.129.0.0/23`).
* **Security:** Configured firewall rules for Health Checks and Global Load Balancer public ingress.
* **Compute:** Created an Instance Template with a startup script for Apache2 and established a Managed Instance Group (MIG).
* **Load Balancing:** Deployed a Global External Application Load Balancer with HTTP and HTTPS frontends.
* **Modern Security:** Migrated from legacy SSL certs to Google Certificate Manager using DNS Authorization (automatic CNAME validation).

### 3. DNS & Visualization
* **DNS Configuration:** Used the existing public DNS zone `[DOMAIN]`.
* **Record Creation:** Created an A record for `mcptest.[DOMAIN]`.
* **Architecture Diagrams:** Generated Graphviz (`.dot`) and Mermaid (`.mmd`) architectural diagrams.
