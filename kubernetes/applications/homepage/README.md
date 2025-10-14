

# Apply with kustomize

```sh
k apply -k kubernetes/applications/homepage/overlays/dev
```

# Get output from secret
```sh
k get secret -n homepage homepage-secrets -o json | jq '.data | map_values(@base64d)'
```


## Describe interpolated config from env

Get all 
```sh
k get all -n homepage
```

Print out services.yaml
```sh
k exec -it -n homepage <pod> -- cat /app/config/services.yaml
```