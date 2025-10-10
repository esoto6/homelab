

# Apply with kustomize

```sh
k apply -k kubernetes/applications/homepage/base
```

# Get output from secret
```sh
k get secret -n homepage homepage-secrets -o json | jq '.data | map_values(@base64d)'
```


