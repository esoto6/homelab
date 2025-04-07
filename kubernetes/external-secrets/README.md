Example: https://external-secrets.io/latest/examples/bitwarden/
Video: https://www.youtube.com/watch?v=nchDkWJHem4

helm repo add external-secrets https://charts.external-secrets.io

helm install external-secrets external-secrets/external-secrets -n external-secrets --create-namespace -f values.yaml

Create dockerfile for bitwarden-cli
Releases located here https://github.com/bitwarden/clients/releases



Create secret.yaml
```yaml
apiVersion: v1
data:
  BW_HOST: ...
  BW_USERNAME: ...
  BW_PASSWORD: ...
kind: Secret
metadata:
  name: bitwarden-cli
  namespace: bitwarden
type: Opaque
```
https://hub.docker.com/r/ppatlabs/bitwarden-cli

Create bitwarden-cli.yaml

Update image with image found on dockerhub or built from doc


# Create CRD for retrieveing data
Created cluster-secret-stores.yaml
kubectl apply -f cluster-secret-stores.yaml


# As a developer trying to use the external-secert

Created an app-example-secert.yaml

Create an entry in bitwarden of 'test-with-secrets'

Apply file to kubernetes

This file was created in the default namespace

# check secret
Check to see if your secret has synced
kubectl get externalsecrets

If it has synced you can then check a regular kubernetes secret

kubectl get secret

Describe secret to see values.
You can see the data and the bytes containing for your fields

# Get Values from your fields and decode to view
kubectl get secret testing.external.secrets.operator -o jsonpath="{.data.username}" | base64 -d
kubectl get secret testing.external.secrets.operator -o jsonpath="{.data.password}" | base64 -d



> [!IMPORTANT] 
> New passwords created during testing was resulting in a not found error.
> 

# Port Forward to test api
kubectl port-forward service/bitwarden-cli 8087:8087 -n external-secrets

in a new terminal:
curl 127.0.0.1:8087/object/item/{{name you are searching}}


# Not detecting new identities in bitwarden
Some forum threads state to logout and login again. 

kubectl get all -n external-secrets

kubectl delete pod bitwarden-cli-xxxx -n external-secrets

kubectl get all -n external-secrets

kubectl logs -f bitwarden-cli-xxx -n external-secrets