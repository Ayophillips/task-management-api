# Task Management API - Architecture Diagram

```mermaid
graph TB
    %% Client Layer
    Client[Client Applications<br/>Web/Mobile/API Clients]
    
    %% API Gateway/Load Balancer
    LB[Load Balancer<br/>Kubernetes Service]
    
    %% Application Layer
    subgraph "FastAPI Application"
        Main[main.py<br/>FastAPI App]
        
        subgraph "API Routes"
            AuthAPI[auth.py<br/>Authentication]
            TaskAPI[tasks.py<br/>Task Management]
        end
        
        subgraph "Core Services"
            Security[security.py<br/>JWT & Password]
            Errors[errors.py<br/>Error Handling]
            Logging[logging.py<br/>Logging Service]
        end
        
        subgraph "Data Layer"
            Models[Models<br/>SQLModel ORM]
            Schemas[Schemas<br/>Pydantic Validation]
            Database[database.py<br/>Connection Pool]
        end
    end
    
    %% Database Layer
    PostgreSQL[(PostgreSQL<br/>Primary Database)]
    
    %% Migration Service
    Migration[Migration Service<br/>MongoDB → PostgreSQL]
    MongoDB[(MongoDB<br/>Legacy Database)]
    
    %% Infrastructure
    subgraph "Kubernetes Cluster"
        subgraph "Application Pods"
            Pod1[API Pod 1]
            Pod2[API Pod 2]
            Pod3[API Pod N...]
        end
        
        subgraph "Database"
            PGPod[PostgreSQL Pod]
            PVC[Persistent Volume]
        end
        
        subgraph "Jobs"
            MigJob[Migration Job]
        end
    end
    
    %% Testing Layer
    subgraph "Testing Suite"
        UnitTests[Unit Tests<br/>pytest]
        IntegTests[Integration Tests]
        PerfTests[Performance Tests]
        ConcTests[Concurrency Tests]
    end
    
    %% Configuration & Monitoring
    Config[Configuration<br/>.env files]
    Logs[Log Files<br/>Structured Logging]
    
    %% Flow Connections
    Client --> LB
    LB --> Main
    
    Main --> AuthAPI
    Main --> TaskAPI
    Main --> Security
    Main --> Errors
    Main --> Logging
    
    AuthAPI --> Models
    TaskAPI --> Models
    Models --> Schemas
    Models --> Database
    Database --> PostgreSQL
    
    Migration --> MongoDB
    Migration --> PostgreSQL
    
    Main --> Pod1
    Main --> Pod2
    Main --> Pod3
    Pod1 --> PGPod
    Pod2 --> PGPod
    Pod3 --> PGPod
    PGPod --> PVC
    
    UnitTests -.-> Main
    IntegTests -.-> Main
    PerfTests -.-> Main
    ConcTests -.-> Main
    
    Config -.-> Main
    Main --> Logs
    
    %% Styling
    classDef client fill:#e1f5fe
    classDef api fill:#f3e5f5
    classDef core fill:#e8f5e8
    classDef data fill:#fff3e0
    classDef db fill:#ffebee
    classDef k8s fill:#f1f8e9
    classDef test fill:#fce4ec
    
    class Client client
    class AuthAPI,TaskAPI,Main api
    class Security,Errors,Logging core
    class Models,Schemas,Database data
    class PostgreSQL,MongoDB db
    class Pod1,Pod2,Pod3,PGPod,PVC,MigJob k8s
    class UnitTests,IntegTests,PerfTests,ConcTests test
```

## Architecture Components

### 1. **Client Layer**
- Web applications, mobile apps, or direct API clients
- Communicates via HTTP/HTTPS with JWT authentication

### 2. **API Gateway & Load Balancing**
- Kubernetes Service for load balancing
- Routes traffic to multiple application pods
- SSL termination and request routing

### 3. **FastAPI Application Core**
- **main.py**: Application entry point with middleware and routing
- **Authentication API**: User registration, login, JWT token management
- **Task API**: CRUD operations for task management
- **Security Layer**: JWT validation, password hashing, user authentication
- **Error Handling**: Centralized exception handling and logging
- **Logging Service**: Structured logging with file rotation

### 4. **Data Layer**
- **SQLModel Models**: ORM models for User and Task entities
- **Pydantic Schemas**: Request/response validation and serialization
- **Database Connection**: PostgreSQL connection pool with health checks
- **Relationships**: User ↔ Task one-to-many relationship

### 5. **Database Layer**
- **PostgreSQL**: Primary relational database
- **Connection Pooling**: Optimized connection management
- **Constraints**: Unique constraints and foreign key relationships

### 6. **Migration Service**
- Standalone service for migrating data from MongoDB to PostgreSQL
- Batch processing with progress tracking
- Containerized for Kubernetes deployment

### 7. **Kubernetes Infrastructure**
- **Application Pods**: Horizontally scalable FastAPI instances
- **Database Pod**: PostgreSQL with persistent storage
- **Persistent Volume**: Data persistence across pod restarts
- **Migration Job**: One-time data migration execution

### 8. **Testing Suite**
- **Unit Tests**: Individual component testing
- **Integration Tests**: End-to-end API testing
- **Performance Tests**: Load and stress testing
- **Concurrency Tests**: Multi-user scenario testing

### 9. **Configuration & Monitoring**
- Environment-based configuration (.env files)
- Structured logging with rotation
- Health check endpoints
- Database connection monitoring

## Key Features

- **Authentication**: JWT-based with token blacklisting
- **Authorization**: User-specific task access control
- **Data Validation**: Pydantic schemas for request/response validation
- **Error Handling**: Comprehensive exception handling with logging
- **Database**: PostgreSQL with connection pooling and health checks
- **Scalability**: Kubernetes-ready with horizontal pod scaling
- **Testing**: Comprehensive test suite with multiple test types
- **Migration**: MongoDB to PostgreSQL data migration support
- **Monitoring**: Health checks and structured logging

## Security Features

- Password hashing with bcrypt
- JWT token authentication
- Token blacklisting for logout
- User-specific data access control
- Input validation and sanitization
- SQL injection prevention via ORM

## Deployment Architecture

The application is designed for cloud-native deployment with:
- Container orchestration via Kubernetes
- Horizontal scaling capabilities
- Persistent data storage
- Health monitoring and logging
- Environment-based configuration management