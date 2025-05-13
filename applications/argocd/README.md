kustomize build --enable-helm ./applications/argocd | kubectl apply -f -
