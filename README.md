# Notes API

A small HTTP Notes API built with Python and Flask.

## What it does

The service allows users to check its health, view notes, and create notes.

## How to run

Run the service with:

    ./scripts/run.sh

The service listens on port 8080 by default.

You can use another port with the PORT environment variable:

    PORT=9000 ./scripts/run.sh

## How to test

Run the tests with:

    ./scripts/test.sh

The tests should finish with TESTS: 3/3.

## Endpoints

- `GET /` - service information
- `GET /healthz` - health check
- `GET /notes` - list all notes
- `POST /notes` - create a new note

## Rollback

Argo CD deploys what is on the `main` branch, from the `k8s` folder.
To roll back, undo the commit that deployed the bad version, with a new commit:

    git log --oneline -- k8s/deployment.yaml
    git revert <commit>
    git push

Argo CD deploys the previous version within three minutes. Do not use
`kubectl rollout undo`: self-heal would put the bad version back.
