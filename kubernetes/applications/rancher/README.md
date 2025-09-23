helm repo add rancher https://releases.rancher.com/server-charts/stable

helm show chart rancher/rancher


helm show values rancher/rancher > values.yaml