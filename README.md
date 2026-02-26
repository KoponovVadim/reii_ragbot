# LLM Chat Assistant with RAG Search

A production-ready REST API for building intelligent chat assistants powered by Large Language Models and Retrieval-Augmented Generation (RAG). The system indexes content from WordPress news websites and provides semantic search capabilities through vector embeddings.

## Project Overview

This project implements a conversational AI assistant that combines the capabilities of Large Language Models with domain-specific knowledge retrieval. The system is designed to handle multi-turn dialogues, maintain conversation history, and augment LLM responses with relevant information retrieved from a vector database of news articles.

### Core Capabilities

- Multi-turn conversational interface with persistent dialogue history
- Vector database integration for semantic search across indexed content
- Asynchronous request handling for high-performance concurrent operations
- Scalable architecture built on cloud-native technologies
- Email validation and contact information management
- System health monitoring and diagnostics

## Technical Architecture

The application follows a clean, layered architecture pattern:

```
REST API Layer (FastAPI)
        ↓
Business Logic Layer (Services)
        ↓
Data Access Layer (Repositories)
        ↓
Database Layer (PostgreSQL with pgvector)
```

## Project Structure

```
rag_train/
├── api/
│   └── endpoints/
│       └── contact.py              REST endpoint for contact and conversation handling
├── core/
│   └── config.py                   Application configuration management
├── database/
│   ├── connections.py              Database connection lifecycle management
│   └── repositories/
│       └── contact.py              Data access operations for conversations
├── schemas/
│   └── contact.py                  Pydantic models for request/response validation
├── services/
│   └── contact.py                  Core business logic and conversation processing
├── main.py                         FastAPI application and route definitions
├── init.sql                        Database schema initialization and indices
├── Dockerfile                      PostgreSQL image with pgvector extension
├── docker-compose.yml              Container orchestration configuration
└── README.md
```

## Technical Stack

- **Python 3.11+** - Core language runtime
- **FastAPI** - Modern, high-performance web framework
- **PostgreSQL 16+** - Relational database with vector support
- **pgvector** - PostgreSQL extension for vector similarity search
- **asyncpg** - High-performance asynchronous PostgreSQL driver
- **Pydantic** - Data validation and serialization
- **Uvicorn** - ASGI application server
- **Docker** - Containerization

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Docker and Docker Compose
- PostgreSQL 16+ (if running without Docker)

### Installation and Run

**Using Docker Compose (Recommended)**

```bash
docker-compose up -d
```

The application will be available at `http://localhost:8000`

**Local Development Setup**

```bash
python -m venv venv_311
source venv_311/bin/activate  # On Windows: venv_311\Scripts\activate
pip install fastapi uvicorn pydantic pydantic-settings databases[postgresql] asyncpg email-validator
python -m uvicorn main:app --reload
```

### API Documentation

Interactive API documentation is automatically generated and available at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Health Check

**GET /health**

Verifies application and database connectivity.

Response:
```json
{
  "status": "ok",
  "message": "Database connection available"
}
```

### Conversation Management

**POST /api/contact**

Processes multi-turn conversations and stores them in the database. This endpoint accepts dialogue history and persists it for retrieval and analysis.

Request:
```json
{
  "email": "user@example.com",
  "messages": [
    {
      "role": "user",
      "content": "What is the latest news about artificial intelligence?"
    },
    {
      "role": "assistant",
      "content": "Based on recent articles, there have been significant developments in transformer architectures..."
    }
  ]
}
```

Response:
```json
{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "reply": "Thank you for your message. We will follow up shortly."
}
```

Request validation:
- Email must be valid format (RFC 5321 compliant)
- Message list must contain at least one message
- Content length: 1-5000 characters per message
- Role must be either "user" or "assistant"

## Database Schema

### Conversations Table
Stores conversation metadata and participant information.

```sql
id              UUID           Primary key, automatically generated
email           TEXT           Participant contact information
created_at      TIMESTAMPTZ    Conversation creation timestamp
updated_at      TIMESTAMPTZ    Last activity timestamp
```

### Messages Table
Maintains the complete message history for each conversation.

```sql
id              BIGSERIAL      Primary key
conversation_id UUID           Foreign key referencing conversations
role            TEXT           Message sender role (user|assistant)
content         TEXT           Message body
created_at      TIMESTAMPTZ    Message creation timestamp
```

Indices:
- `idx_messages_conversation_id` - Optimizes queries filtering by conversation
- `idx_messages_created_at` - Supports time-range queries

### Document Chunks Table
Vector database for RAG indexing of WordPress news content.

```sql
id              BIGSERIAL      Primary key
source_url      TEXT           Origin URL from WordPress site
chunk_index     INT            Segment identifier for multi-part documents
content         TEXT           Article text segment
embedding       vector(384)    Semantic embedding (pgvector format)
```

Indices:
- `idx_document_chunks_source_url` - Enables document-level filtering
- Vector index (planned) - Optimizes nearest-neighbor similarity searches

## Development Workflow

### Code Organization

The project follows a modular structure enabling independent testing and scaling of components:

- **Schemas** - Pydantic models for data validation and serialization
- **Services** - Business logic, transaction management, and orchestration
- **Repositories** - SQL queries and data persistence operations
- **Endpoints** - HTTP request handling and response marshalling

### Asynchronous Processing

All I/O operations are implemented as async/await patterns:
- Non-blocking database connections managed by `asyncpg`
- Concurrent request handling through Uvicorn workers
- Transactional operations ensuring data consistency across multi-step processes

### Adding New Features

The existing architecture supports straightforward extension:

1. Define request/response schemas in `schemas/`
2. Implement business logic in `services/`
3. Add data access methods in `database/repositories/`
4. Create endpoint in `api/endpoints/`
5. Register router in `main.py`

## Development Status and Roadmap

### Current Implementation

- Core conversation management API with persistent storage
- Multi-turn dialogue support with role-based message handling
- Email validation and contact information processing
- Database health checking and monitoring
- Docker containerization for PostgreSQL with pgvector
- Clean architectural patterns for maintainability and testing

### Planned Features

**Phase 1: RAG Integration**
- WordPress content scraper for news article indexing
- Vector embedding generation using sentence transformers
- Semantic search implementation leveraging pgvector
- Augmented response generation with source attribution

**Phase 2: LLM Integration**
- Integration with large language models (OpenAI API, open-source alternatives)
- Prompt engineering for context-aware responses
- Token limit management and streaming responses
- Usage tracking and cost monitoring

**Phase 3: Enterprise Features**
- User authentication and authorization
- Rate limiting and API key management
- Conversation pagination and filtering
- Audit logging and compliance tracking
- Multi-tenant support

**Phase 4: Performance Optimization**
- Vector similarity search indexing
- Query result caching strategy
- Database query optimization
- Horizontal scaling for high-concurrency scenarios

## Performance Characteristics

### Asynchronous Architecture
- Non-blocking I/O operations throughout the stack
- Concurrent request handling via Uvicorn's worker pool
- Connection pooling for efficient database resource usage

### Database Optimization
- B-tree indices for rapid lookups on conversation and message queries
- Foreign key constraints ensuring referential integrity
- ACID transaction support for atomic multi-step operations

### Scalability Considerations
- Stateless API design enabling horizontal scaling
- PostgreSQL connection pooling via PgBouncer (production deployment)
- Vector database partitioning strategy for large-scale content indexing

## Monitoring and Debugging

### Application Health

```bash
curl -X GET http://localhost:8000/health
```

### Docker Container Management

View application logs:
```bash
docker-compose logs -f
```

Stop services:
```bash
docker-compose down
```

Restart services:
```bash
docker-compose restart
```

### Database Operations

Access database query interface:
```bash
docker-compose exec db psql -U postgres -d chat_db
```

### Example API Calls

Process a conversation:
```bash
curl -X POST http://localhost:8000/api/contact \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "messages": [
      {"role": "user", "content": "What are the latest developments in AI?"},
      {"role": "assistant", "content": "Recent advancements include transformer architecture improvements..."}
    ]
  }'
```

## Deployment Considerations

### Production Environment

- Use a dedicated PostgreSQL instance with automated backups
- Configure SSL/TLS for API endpoints
- Implement API rate limiting and DDoS protection
- Set up centralized logging and monitoring
- Use environment-based configuration management
- Enable CORS for frontend integration where needed

### Infrastructure Stack

- Docker/Kubernetes for container orchestration
- Load balancer for traffic distribution
- Redis for session management and caching (future)
- Message queue for async tasks (Celery + RabbitMQ, planned)
- Backup and disaster recovery procedures

## Technical Decisions and Rationale

**Why PostgreSQL with pgvector?**
- Native vector data type support without middleware
- ACID compliance for transactional consistency
- Mature ecosystem and extensive community support
- Performance advantages for hybrid relational and vector queries

**Why FastAPI?**
- Automatic API documentation generation (Swagger, ReDoc)
- Built-in dependency injection for clean code organization
- High performance comparable to Go and Node.js frameworks
- Excellent async/await support with Python 3.7+
- Strong type validation through Pydantic integration

**Why Asynchronous Architecture?**
- I/O-bound operations (database, external APIs) don't block request processing
- Higher throughput with same resource consumption
- Reduced context switching overhead
- Natural fit for long-running LLM operations and vector searches
## Team and Contribution

This project represents modern best practices in API development and is actively maintained for production use.

For technical inquiries or contribution proposals, please refer to the project repository.

## License

MIT License - See LICENSE file for details

## Acknowledgments

Built with:
- FastAPI framework and community
- PostgreSQL and pgvector project
- Python async ecosystem (asyncpg, databases)
- Docker and containerization patterns