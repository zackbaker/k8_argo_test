# k8_argo_test
Testing out Argo on k8

## Setup Instructions
- Docker
-- Go to Preferences
-- Select Kubernetes Tab
-- Check Enable Kubernetes
-- Wait for restart

- Run the following commands in terminal (MacOS)
```bash
# Install all the argo products
brew tap argoproj/tap
brew install argoproj/tap/argo
brew install argoproj/tap/argocd
brew install helm
# Come back to help installation
# helm repo add argo https://argoproj.github.io/argo-helm
# Add namespace and install Argo Workflow
kubectl create namespace argo
kubectl apply -n argo -f https://raw.githubusercontent.com/argoproj/argo/stable/manifests/install.yaml
# Add namespace and install Argo CD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

- In a seperate terminal tab/screen for each command
```bash
kubectl -n argo port-forward deployment/argo-server 2746:2746
kubectl -n argocd port-forward svc/argocd-server 8080:443
```
- Then go to [local host on port 2746](http://localhost/:2746) to access argo workflow
- And go to [local host on port 8080](http://localhost/:8080) to access argo CD

- Next we will find our password
```bash
kubectl get pods -n argocd -l app.kubernetes.io/name=argocd-server -o name | cut -d'/' -f 2
```

- Then we will login using the password found above
```bash
argocd login localhost:8080
# Change password
argocd account update-password
```

- Next let's get CD syncing with Workflow
```bash
argocd app create hello-world --repo https://github.com/zackbaker/k8_argo_test.git --path workflows --dest-server https://kubernetes.default.svc --dest-namespace argo
argocd app sync hello-world
```