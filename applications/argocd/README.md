# ArgoCD

```bash
k create namespace argocd
```


```bash
k apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

Apply service file

```bash
k apply -f argocd-service.yaml -n argocd
```

Get IP address

```
k get service -n argocd
```


Get Password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d