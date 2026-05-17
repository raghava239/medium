digraph GCP_Architecture {
    // Graph styling
    rankdir=LR;
    fontname="Helvetica,Arial,sans-serif";
    node [fontname="Helvetica,Arial,sans-serif", shape=box, style="rounded,filled", fillcolor="#e3f2fd", color="#1565c0", margin=0.2];
    edge [fontname="Helvetica,Arial,sans-serif", fontsize=10, color="#555555"];

    // External entities
    subgraph cluster_external {
        label="External Internet";
        style=dashed;
        color="#9e9e9e";
        fillcolor="#f9f9f9";
        
        Users [label="Internet Users", shape=oval, fillcolor="#eeeeee", color="#999999"];
        DNS [label="Cloud DNS Zone\n(mcp.example.com)", shape=cylinder, fillcolor="#eeeeee", color="#999999"];
    }

    // GCP Project
    subgraph cluster_gcp {
        label="Google Cloud Platform (Project: gcp-project-name-redacted)";
        style=solid;
        color="#4285f4";
        penwidth=2;

        // Global Resources
        subgraph cluster_global {
            label="Global Resources";
            style=dotted;
            color="#5f6368";

            ARecord [label="A Record\n(mcptest)"];
            CNAMERecord [label="CNAME Record\n(_acme-challenge)"];
            StaticIP [label="Static External IP"];
            GLB [label="Global External HTTP/S\nLoad Balancer", shape=component, fillcolor="#c3e8cb", color="#137333"];
            
            CertMap [label="Certificate Map"];
            CertMgr [label="Certificate Manager", shape=component];
            DNSAuth [label="DNS Authorization"];
        }

        // VPC Network
        subgraph cluster_vpc {
            label="VPC Network: dev-vpc";
            style=solid;
            color="#34a853";
            penwidth=1.5;

            // Region
            subgraph cluster_region {
                label="Region: us-central1";
                style=dashed;
                color="#0f9d58";

                // Regional Proxy Subnet
                subgraph cluster_proxy_subnet {
                    label="Proxy-Only Subnet (10.129.0.0/23)";
                    color="#f29900";
                    Proxy [label="Regional Managed Proxy", fillcolor="#fce8b2", color="#f29900"];
                }

                // Primary Subnet
                subgraph cluster_primary_subnet {
                    label="Primary Subnet (10.10.0.0/24)";
                    color="#1a73e8";
                    
                    MIG [label="Managed Instance Group\n(dev-apache-mig)", shape=folder, fillcolor="#d2e3fc", color="#1a73e8"];
                    VM1 [label="Apache VM 1"];
                    VM2 [label="Apache VM 2"];
                }

                Router [label="Cloud Router"];
                NAT [label="Cloud NAT Gateway", shape=cds];
            }
        }
    }

    // Flow & Connections
    Users -> StaticIP [label="HTTPS Traffic"];
    DNS -> StaticIP [label="Resolves to", style=dashed];
    ARecord -> DNS [style=dashed];
    CNAMERecord -> DNS [style=dashed];

    StaticIP -> GLB;
    GLB -> Proxy [label="Terminates SSL"];
    Proxy -> MIG [label="Proxies Traffic"];

    // MIG internal grouping
    MIG -> VM1 [dir=none, style=dotted];
    MIG -> VM2 [dir=none, style=dotted];

    // Outbound flow
    VM1 -> NAT [label="Outbound Internet"];
    VM2 -> NAT [label="Outbound Internet"];
    NAT -> Router;
    Router -> Users [label="Internet", style=dashed];

    // Certificate Manager connections
    GLB -> CertMap [dir=none, style=dotted];
    CertMap -> CertMgr [dir=none, style=dotted];
    CertMgr -> DNSAuth [dir=none, style=dotted];
    DNSAuth -> CNAMERecord [label="Validates", style=dashed];
}
