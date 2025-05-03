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