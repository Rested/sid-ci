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