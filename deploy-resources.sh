#!/bin/bash

set -e

K8S_DIR="./k8s"

echo "Creating configmap..."
kubectl create configmap postgres-config --from-env-file=.env

echo "Creating PostgreSQL Persistent Volume and Persistent Volume Claim..."
kubectl apply -f "$K8S_DIR/postgres-pv-pvc.yaml"

echo "Creating Deployment and Services..."
kubectl apply -f "$K8S_DIR/main.yaml"

echo "Deployment and Services have been created successfully."