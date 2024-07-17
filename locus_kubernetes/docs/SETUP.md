# Setup Guide

## Prerequisites

- Kubernetes cluster
- kubectl installed and configured
- Basic understanding of Kubernetes concepts

## Steps

1. Clone the repository
2. Navigate to the repository directory

## Deploying the FastAPI Application

3. Build the Docker image for the FastAPI app:

```
docker build -t your-docker-registry/fastapi-app:latest app/
docker push your-docker-registry/fastapi-app:latest
```

4. Update `kubernetes/fastapi-deployment.yaml` with your image name
5. Deploy the FastAPI application:

6. Apply the Kubernetes manifests:

```
kubectl apply -f kubernetes/fastapi-deployment.yaml
kubectl apply -f kubernetes/fastapi-service.yaml
```

7. Verify the deployments:

```
kubectl get deployments
kubectl get pods
```

8. Check the service for the master:
