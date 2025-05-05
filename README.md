# Task Management API

A RESTful API for a Task Management System built with FastAPI, initially using MongoDB and later migrated to PostgreSQL, deployed on Google Kubernetes Engine (GKE).

## Features

[...existing features...]
- Database migration support (MongoDB to PostgreSQL)
- Kubernetes deployment
- Google Cloud Platform integration
- Container orchestration with GKE

## Tech Stack

- **Backend**: FastAPI 0.100.0+
- **Database**: 
  - PostgreSQL 15+ (primary database)
  - MongoDB (legacy data source)
- **Authentication**: JWT tokens
- **Documentation**: Swagger UI (built-in with FastAPI)
- **Container Orchestration**: Kubernetes (GKE)
- **Container Registry**: Google Container Registry (GCR)
- **SSL**: TLS 1.3

[...existing Prerequisites and Installation sections...]

## Database Migration

### MongoDB to PostgreSQL Migration

1. Build the migration container:
```bash
cd migration
docker build -t gcr.io/your-project/mongo-migrator:latest .
docker push gcr.io/your-project/mongo-migrator:latest
```

2. Create Kubernetes secrets for database credentials:
```bash
kubectl create secret generic migration-secrets \
  --from-literal=mongo-uri='mongodb+srv://user:pass@cluster.mongodb.net' \
  --from-literal=pg-host='postgres-service' \
  --from-literal=pg-database='task_management' \
  --from-literal=pg-user='postgres' \
  --from-literal=pg-password='your-password'
```

3. Run the migration job:
```bash
kubectl apply -f k8s/migrate-job.yaml
```

4. Monitor migration progress:
```bash
kubectl logs -f job/mongo-postgres-migration
```

## Production Deployment

### Google Kubernetes Engine (GKE) Deployment

1. Set up Google Cloud project and enable required APIs:
```bash
gcloud projects create your-project-id
gcloud config set project your-project-id
gcloud services enable container.googleapis.com
```

2. Create GKE cluster:
```bash
gcloud container clusters create task-mgmt-cluster \
  --num-nodes=3 \
  --machine-type=e2-standard-2 \
  --region=us-central1
```

3. Build and push container image:
```bash
docker build -t gcr.io/your-project/task-mgmt-api:latest .
docker push gcr.io/your-project/task-mgmt-api:latest
```

4. Deploy PostgreSQL database:
```bash
kubectl apply -f k8s/postgres-pvc.yaml
kubectl apply -f k8s/postgres-deployment.yaml
kubectl apply -f k8s/postgres-service.yaml
```

5. Create database secrets:
```bash
kubectl create secret generic db-secrets \
  --from-literal=username=postgres \
  --from-literal=password=your-secure-password
```

6. Deploy the application:
```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

7. Get the external IP:
```bash
kubectl get service task-api-service
```

### Verifying Deployment

1. Check deployment status:
```bash
kubectl get deployments
kubectl get pods
kubectl get services
```

2. Check application health:
```bash
curl http://<EXTERNAL-IP>/health
```

3. Monitor logs:
```bash
kubectl logs -f deployment/task-api
```

### Scaling

Scale the deployment:
```bash
kubectl scale deployment task-api --replicas=3
```

### Monitoring

- Health checks available at `/health`
- Kubernetes dashboard metrics
- Google Cloud Monitoring
- Google Cloud Logging

## Infrastructure Layout

```
k8s/
├── deployment.yaml      # Main application deployment
├── service.yaml        # Load balancer service
├── postgres-pvc.yaml   # Persistent volume claim for PostgreSQL
├── postgres-deployment.yaml  # PostgreSQL deployment
├── postgres-service.yaml    # PostgreSQL service
└── migrate-job.yaml    # Database migration job
```

[...rest of the existing sections...]