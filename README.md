# k8_argo_test
Testing out Argo on k8

## Setup Instructions
- Docker
- - Go to Preferences
- - Select Kubernetes Tab
- - Check Enable Kubernetes
- - Wait for restart

- Run the following commands in terminal (MacOS)
```bash
# Install all the argo products
brew tap argoproj/tap
brew install argoproj/tap/argo
brew install argoproj/tap/argocd

# install helm and add argo repo
brew install helm
helm repo add argo https://argoproj.github.io/argo-helm

# Add namespace and install Argo Workflow
kubectl create namespace argo
helm install argo argo/argo -n argo

# Add namespace and install Argo CD
kubectl create namespace argocd
helm install argocd argo/argo-cd -n argocd

# Add namespace and install Argo Events
# Note: helm for argo-events is broken
kubectl apply -f https://raw.githubusercontent.com/argoproj/argo-events/master/hack/k8s/manifests/installation.yaml -n argo-events
```
- Add storage for argo to share
```bash
kubectl create -f argo_settings/volume.yaml
```

- Add argo events events
```bash
kubectl apply -n argo-events -f argo_events/random_numbers -R
```

- Run the following commands to forward ports and access the UI and then press ctrl+a d
```bash
screen kubectl -n argo port-forward deployment/argo-server 2746:2746
screen kubectl -n argocd port-forward deployment/argocd-server 8080:8080
```

- Next we will find our password
```bash
kubectl get pods -n argocd -l app.kubernetes.io/name=argocd-server -o name | cut -d'/' -f 2
```

- Then we will login using the password found above, username is admin
```bash
argocd login localhost:8080
# Change password
argocd account update-password
```

- Next let's get CD syncing with Workflow
```bash
argocd app create workflows --repo https://github.com/zackbaker/k8_argo_test.git --path argo_crons --dest-server https://kubernetes.default.svc --dest-namespace argo
argocd app sync workflows
```

- Then go to [local host on port 2746](http://localhost:2746) to access argo workflow
- And go to [local host on port 8080](http://localhost:8080) to access argo CD