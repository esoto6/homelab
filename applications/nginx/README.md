# Nginx

This app is used as a test to learn how to utilize kustomize.



# Test overlays

1. cd to applications/nginx. Then run
```
kustomize build overlays/dev
```

# Apply with kustomize
```
k apply -k overlays/dev
```



# misc

1. Get certificate status
```
k get certificates -n nginx
```