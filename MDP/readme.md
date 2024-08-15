# Kubernetes YAMLs Folder

This folder contains the Kubernetes YAML files necessary to deploy and manage your application using Kubernetes. Follow the steps below to run and manage your application on a Kubernetes cluster.

## Prerequisites

Before you begin, ensure you have the following prerequisites installed and configured:

- **kubectl**: Kubernetes command-line tool.
- **kubectl context**: Ensure that your `kubectl` is configured to the correct Kubernetes cluster context.
- **helm**: helm is a kubernetes package tool.

## Deployment Steps

1. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   cd <repository-folder>

## Navigate to Kubernetes yamls

1. kubectl apply -f mysql-deployment.yaml,mysql-service.yaml,pythonapp-deployment.yaml,pythonapp-service.yaml

2. cd ingress
  kubectl apply -f ingress.yaml

3. cd metrics-server
  kubectl apply -f components.yaml

## Helm treafik install packages

1. helm repo add traefik https://traefik.github.io/charts
2. helm repo update
3. helm install traefik traefik/traefik
4. more information about treafik can be found at https://doc.traefik.io/traefik/getting-started/install-traefik/#use-the-helm-chart

## Helm prometheus and grafana

1. helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
2. helm repo add stable https://kubernetes-charts.storage.      googleapis.com/
3. helm repo update
4. helm install prometheus prometheus-community/kube-prometheus-stack

5. more information can be found at https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack

6. Login Username:admin Password:prom-operator
