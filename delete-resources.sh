#!/bin/bash

set -e

echo "Deleting Deployment and Service..."
kubectl delete deployment main-deployment
kubectl delete service main-service

echo "Deleting PostgreSQL Persistent Volume and Persistent Volume Claim..."
kubectl delete pv postgres-pv
kubectl delete pvc postgres-pvc --grace-period=0 --force

echo "Deleting ConfigMap..."
kubectl delete configmap postgres-config

echo "All resources have been deleted successfully."