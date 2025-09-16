# Intermediate Steps

## Cert Manager Installation
1. Install Cert-Manager

```sh
helm repo add jetstack https://charts.jetstack.io
helm repo update
```

```sh
helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --set crds.enabled=true
```

>[!IMPORTANT]
>Since ESO was not working with a self-signed certificate we are having to get our 'valid' certificate with the dns-01 challenge

2. Create secret in cluster
```sh
kubectl create secret generic cloudflare-api-token \
  --from-literal=api-token=<your-cloudflare-token> \
  -n cert-manager
```

2. Create ClusterIssuer
```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-stg
spec:
  acme:
    email: "edwin.soto03@gmail.com"
    server: "https://acme-staging-v02.api.letsencrypt.org/directory"
    privateKeySecretRef:
      name: cloudflare-key
    solvers:
      - dns01:
          cloudflare:
            email: "edwin.soto03@gmail.com"
            apiTokenSecretRef:
              name: cloudflare-api-token
              key: api-token
```


4. Create Wildcard Certificate
```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: wildcard-cert
  namespace: cert-manager
spec:
  secretName: wildcard-cert-tls
  issuerRef:
    name: letsencrypt-stg
    kind: ClusterIssuer
  commonName: "*.rubberduckops.com"
  dnsNames:
    - "*.rubberduckops.com"
    - rubberduckops.com
```


## External Secrets Operator


3. Create cert for the sdk server
Namespace 'external-secrets' may not exist just yet.

```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: bitwarden-sdk-server-cert
  namespace: external-secrets
spec:
  secretName: bitwarden-tls-certs
  dnsNames:
    - bitwarden-sdk-server.external-secrets.svc.cluster.local
  issuerRef:
    name: selfsigned-cluster-issuer
    kind: ClusterIssuer
```

## External Secrets Setup

1. Create ns for external-secrets

```sh
kubectl create ns external-secrets-system
```

2. Create a self-signed issuer

```yaml
apiVersion: cert-manager.io/v1
kind: Issuer
metadata:
  name: selfsigned-issuer
  namespace: external-secrets-system
spec:
  selfSigned: {}
```

3. Create CA Certificate using slef-signed issuer
```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: ca-cert
  namespace: external-secrets-system
spec:
  secretName: ca-secret
  isCA: true
  commonName: "Bitwarden SDK Server CA"
  subject:
    organizationalUnits:
    - "Bitwarden SDK Server"
    organizations:
    - "External Secrets"
  duration: 8760h # 1 year
  renewBefore: 720h # 30 days
  issuerRef:
    name: selfsigned-issuer
    kind: Issuer
```

4. Create a CA Issuer that uses the CA certificate
```yaml
apiVersion: cert-manager.io/v1
kind: Issuer
metadata:
  name: ca-issuer
  namespace: external-secrets-system
spec:
  ca:
    secretName: ca-secret
```

5. Ccreate Certificate the bitwarden sdk server can use
```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: bitwarden-sdk-server-cert
  namespace: external-secrets-system
spec:
  secretName: bitwarden-tls-certs
  issuerRef:
    name: ca-issuer
    kind: Issuer
  dnsNames:
    - bitwarden-sdk-server
    - bitwarden-sdk-server.external-secrets-system
    - bitwarden-sdk-server.external-secrets-system.svc
    - bitwarden-sdk-server.external-secrets-system.svc.cluster.local
  commonName: bitwarden-sdk-server
  duration: 2160h # 90 days
  renewBefore: 360h # 15 days
  subject:
    organizationalUnits:
    - "Bitwarden SDK Server"
    organizations:
    - "External Secrets"
  usages:
  - server auth
  - client auth
```



3. Check Certificates are ready

```sh
# Check the CA certificate
kubectl get certificate ca-cert -n external-secrets-system

# Check the SDK server certificate
kubectl get certificate bitwarden-sdk-server-cert -n external-secrets-system
```

 4. Install external-secrets helm

- Create `values.yaml` file:
```yaml
bitwarden-sdk-server:
  enabled: true
  tls:
    enabled: true
    secretName: bitwarden-tls-certs
```

- Install via helm
```sh
helm install external-secrets \
   external-secrets/external-secrets \
   -n external-secrets-system \
   --create-namespace \
   -f external-secrets-values.yaml
```

5. Get the CA Bundle for ClusterSecretStore
```sh
# Get the CA certificate
kubectl get secret ca-secret -n external-secrets-system -o jsonpath='{.data.tls\.crt}' | base64 -d > ca.crt

# Convert to base64 for use in ClusterSecretStore
CA_BUNDLE=$(kubectl get secret ca-secret -n external-secrets-system -o jsonpath='{.data.tls\.crt}')
echo "Your CA Bundle:"
echo $CA_BUNDLE
```

6. Create secret for bitwarden sdk access

```sh
kubectl create secret generic bitwarden-access-token \
	--from-literal=token=<token>
```

6. Create `ClusterSecretStore`
```yaml
apiVersion: external-secrets.io/v1
kind: ClusterSecretStore
metadata:
  name: bitwarden-cluster-secretstore
spec:
  provider:
    bitwardensecretsmanager:
      apiURL: https://api.bitwarden.com
      identityURL: https://identity.bitwarden.com
      auth:
        secretRef:
          credentials:
            key: token
            name: bitwarden-access-token
            namespace: default
      bitwardenServerSDKURL: https://bitwarden-sdk-server.external-secrets-system.svc.cluster.local:9998
      organizationID: <add org id>
      projectID: <add proj id>
      caBundle: <ca-bundle>
```

7. Test Secret Retireval
```yaml
apiVersion: external-secrets.io/v1
kind: ExternalSecret
metadata:
  name: new-test
  namespace: default
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: bitwarden-cluster-secretstore
    kind: ClusterSecretStore
  target:
    name: new-test
    creationPolicy: Owner
    template:
      type: Opaque
  data:
    - secretKey: new-test
      remoteRef:
        key: "new-test"
```

8. Verify everything is running correctly
- Check certificate status
```sh
kubectl describe certificate bitwarden-sdk-server-cert -n external-secrets-system
```

- Check if external-secrets pods are running
```sh
kubectl get pods -n external-secrets-system
```

 - Check if `bitwarden-sdk-server` is running and using the certificate
```sh
kubectl get pods -n external-secrets-system -l app.kubernetes.io/name=bitwarden-sdk-server
```

- Check `ClusterSecretStore` status
```sh
kubectl get clustersecretstore bitwarden-cluster-secretstore -n external-secrets-system
```

 - Check `ExternalSecret` status
```sh
kubectl get externalsecret new-test
```

- Check if the secret was created
```sh
kubectl get secret new-test -n
```

 - Check secret is working
```sh
kubectl get secret new-test -o jsonpath='{.data.new-test}' | base64 -d
```


## Install Traefik

1. Add helm repository

```sh
helm repo add traefik https://traefik.github.io/charts
helm repo update
```

2. Create traefik namespace
```sh
kubectl create namespace traefik
```

3. Install via helm
```sh
helm install traefik traefik/traefik \
  --namespace traefik \
  --set kubernetes.ingressClass=traefik \
  --set kubernetes.ingressClassResource.name=traefik \
  --set kubernetes.ingressClassResource.enabled=true \
  --set deployment.replicas=1 \
  --set service.type=LoadBalancer
```

4. Get the external ip to use for cloudflare
```sh
kubectl get svc -n traefik
```

5. Create middleware

Check IP is resolving for domain address
```sh
# nslookup
nslookup rubberduckops.com

# dig
dig rubberduckops.com
```

## Install Argo CD Manually

[Argo CD Steps](/applications/argocd/README.md)