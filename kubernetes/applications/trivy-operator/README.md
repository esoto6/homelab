helm repo add aqua https://aquasecurity.github.io/helm-charts/

helm show chart aqua/trivy-operator


Install CRDS Manually

helm pull aqua/trivy-operator --version 0.30.0 --untar

k apply -f trivy-operator/crds/

rm -rf trivy-operator/


