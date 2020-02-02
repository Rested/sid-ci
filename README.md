# Simple Distributed CI

## Why?

Whether due to resource or network limitations, your server may not always be able to do what your dev machines can.

## How it works

1. `daemon` polls github and says "are there any updates to master"
2. If there are then these are added to a `FIFO` (first in first out) redis queue.
3. `client` polls `server` to check the queue for it. It authenticates with a shared token.
4. `client` receives job and code at the revision
5. `client` attempts to build image and push
6. `client` reports back to `server`.
   - log and status is returned to `server`
   - `server` requeues abandoned jobs and stores 
7. All this can be obsvered from the ui

## Skaffold dev

1. Get skaffold
    ```bash
    curl -Lo skaffold https://storage.googleapis.com/skaffold/releases/latest/skaffold-linux-amd64
    chmod +x skaffold
    sudo mv skaffold /usr/local/bin   
    ```
2. Get k3d
    ```bash
    wget -q -O - https://raw.githubusercontent.com/rancher/k3d/master/install.sh | bash
    k3d create --enable-registry
    ```
1. Add `127.0.0.1 registry.local` to `/etc/hosts/`
3. Use k3 registry
    ```bash
    #add to .zshenv/.profile or similar
    export SKAFFOLD_DEFAULT_REPO=registry.local:5000
    ```
4. Develop!   
```bash
k3d shell --shell zsh
skaffold dev
```


## TODO list

1. Client
1. WebUI
1. Auth - see https://github.com/jtattermusch/grpc-authentication-kubernetes-examples - mtls daemon - jwt ui/client


   
