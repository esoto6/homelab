helm repo add prometheus-community https://prometheus-community.github.io/helm-charts

helm show chart prometheus-community/kube-prometheus-stack

kubectl create namespace monitoring

helm repo update

Show Values;
helm show values oci://ghcr.io/prometheus-community/charts/kube-prometheus-stack > kubernetes/applications/monitoring/base/values.yaml


helm upgrade --install prometheus prometheus-community/kube-prometheus-stack -n monitoring -f kubernetes/applications/monitoring/base/values.yaml


https://technotim.live/posts/kube-grafana-prometheus/
https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack
https://github.com/timothystewart6/launchpad/blob/master/kubernetes/kube-prometheus-stack/values.yml






kubectl kustomize kubernetes/apps/monitoring/base --enable-helm


kubectl kustomize kubernetes/applications/monitoring/base --enable-helm | kubectl apply -f -


Note:
- Need CRDS first

helm pull prometheus-community/kube-prometheus-stack --version 77.11.1 --untar
kubectl apply --server-side -f kube-prometheus-stack/charts/crds/crds/