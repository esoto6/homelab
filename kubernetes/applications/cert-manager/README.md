# Cert-Manager



## Manually Apply

```
kustomize build overlays/dev --enable-helm | kubectl apply -f -
```

## Create Secret

```
kubectl create secret generic cloudflare-api-token \
  --from-literal=api-token=your-api-token-here \
  -n cert-manager
```


# Status of clusterissuer

## Get ClusterIssuer

```
k get clusterissuer
```

```
k describe clusterissuer <name>
```



Need to install crds manually:
Not added with kustomize helm install
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.17.2/cert-manager.crds.yaml

https://github.com/cert-manager/cert-manager/releases