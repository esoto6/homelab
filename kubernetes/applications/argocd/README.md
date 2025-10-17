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


Get Applicationset
```sh
k get applicationset kustomize-apps -n argocd -o yaml
```


## Force remove argocd
Get the namespace JSON
```sh
kubectl get namespace argocd -o json > argocd-ns.json
```
Edit it to remove finalizers
```sh
cat argocd-ns.json | jq '.spec.finalizers = []' > argocd-ns-clean.json
```
Replace the namespace spec
```sh
kubectl replace --raw "/api/v1/namespaces/argocd/finalize" -f argocd-ns-clean.json
```


Creating Homepage user for API:
argocd login argocd.rubberduckops.com

argocd account generate-token --account homepage

Copy output and update secret in bitwarden. Need to automate. 