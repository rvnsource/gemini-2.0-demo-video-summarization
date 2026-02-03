graph TD
    User((User)) -->|HTTPS/WebSocket| API[API Gateway]

    subgraph "Compute Layer"
        API -->|Long Connection| Brain[AWS Fargate: The AI Agent]
        Brain <-->|Inference| LLM[Amazon Bedrock / OpenAI]

        Brain -->|Trigger Tool| Tool[AWS Lambda: MCP GitHub Server]
    end

    subgraph "Data & Tools"
        Tool -->|API Call| GitHub[(GitHub Repo)]
        Brain -->|Read/Write| DB[(DynamoDB: Chat History)]
    end

    style Brain fill:#f96,stroke:#333,stroke-width:2px
    style Tool fill:#69f,stroke:#333,stroke-width:2px
