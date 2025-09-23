# ArgoCD

List all available chart versions
```
helm search repo argo/argo-cd --versions
```

Get the version of a chart from local
```sh
helm show chart argo/argo-cd
```

Generate values.yaml
```sh
helm show values argo/argo-cd > values.yaml
```


Generate chart with kustomize
```sh
kubectl kustomize --enable-helm applications/argocd/overlays/dev
```

Deploy manually
```sh
kustomize build applications/argocd/overlays/dev --enable-helm | kubecctl apply -f -
```