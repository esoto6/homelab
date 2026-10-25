# External Secrets

List all available chart versions
```sh
helm search repo external-secrets/external-secrets --versions
```

Get the version of a chart from local
```sh
helm show chart external-secrets/external-secrets
```

Generate values.yaml
```sh
helm show values external-secrets/external-secrets > values.yaml
```