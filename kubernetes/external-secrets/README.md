Example: https://external-secrets.io/latest/examples/bitwarden/
Video: https://www.youtube.com/watch?v=nchDkWJHem4

helm repo add external-secrets https://charts.external-secrets.io

helm install external-secrets external-secrets/external-secrets -n external-secrets --create-namespace -f values.yaml

