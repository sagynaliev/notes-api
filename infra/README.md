# INF345 Week 11 infrastructure

Based on https://github.com/inf345/inf345-week11-lab.
All seven Terraform blanks and all three Ansible blanks are completed.

## Terraform

From the repository root:

```bash
# macOS with Docker Desktop only:
export DOCKER_HOST="$(docker context inspect --format '{{.Endpoints.docker.Host}}')"

cd infra
terraform fmt -check
terraform init -input=false
terraform validate
terraform plan
terraform apply
curl --fail --retry 15 --retry-delay 1 --retry-all-errors "$(terraform output -raw healthz_url)"
terraform destroy
```

The default image is the project's public M3 image:
`ghcr.io/sagynaliev/notes-api:6c48884f3331cecdbf1358cd1271f0d2e7328633`.
An anonymous pull succeeded. Both image and container use `linux/amd64` for
compatibility with the CI build and Apple Silicon emulation.

The application reads `PORT`, so the container listens on `internal_port` (8080
by default), regardless of the Dockerfile's `EXPOSE 9000` metadata. The host port
also defaults to 8080. The Docker health check calls `/healthz` with Python's
standard library, which is already present in the image.

If another lab is using the default container name or port, set these variables
consistently for **every** plan, apply and destroy in that terminal:

```bash
export TF_VAR_container_name=inf345-notes-week11-test
export TF_VAR_network_name=inf345-notes-week11-test-net
export TF_VAR_host_port=18080
```

`docker_image.app.image_id` and `docker_network.app.name` create dependencies:
Terraform creates the image and network before the container. `~> 4.6` permits
4.6 and later 4.x releases, but excludes 5.0. The committed lock file records
provider 4.7.0 and verified checksums. State, cached providers, private variable
files and saved plans stay ignored; there is no remote backend or cloud block.

## Ansible

From the repository root:

```bash
ansible-playbook -i ansible/inventory.ini ansible/site.yml --syntax-check
ansible-playbook -i ansible/inventory.ini ansible/site.yml
ansible-playbook -i ansible/inventory.ini ansible/site.yml
ansible-playbook -i ansible/inventory.ini ansible/site.yml --check --diff -e app_port=9090
```

The default destination is `~/inf345-app`. For an isolated test, add
`-e app_dir=/absolute/path/to/a/new/test-directory` to every invocation.
The `file` and `copy` modules compare the current state with the desired state.
Only a changed config notifies `Restart the app`; the lab handler records a
simulated restart in `restarts.log` rather than restarting a real service.

## Verified locally on 23 November 2026

- Terraform 1.17.2, Docker provider 4.7.0.
- `fmt`, `init`, `validate` and default fresh-state `plan`: passed; 3 resources to add.
- Apply with the isolated names above: 3 added; HTTP `/healthz` returned
  `{"status":"ok"}`; Docker health status became `healthy`.
- A subsequent plan with the same inputs: no changes.
- Restart-policy plan: 0 add, 1 change, 0 destroy.
- Host-port plan: 1 add, 0 change, 1 destroy (container replacement).
- Deleted only the test container: drift plan proposed 1 add, 0 change, 0 destroy.
  Apply recreated it and `/healthz` succeeded again.
- Ansible syntax check passed. With an isolated `app_dir`, first run:
  `ok=4 changed=3 unreachable=0 failed=0`; second run:
  `ok=3 changed=0 unreachable=0 failed=0`. Restart log contained exactly one line.
- Ansible `--check --diff -e app_port=9090`: predicted `changed=1`, while the
  actual file remained `PORT=8080` and the restart log stayed unchanged.
- Existing Flask tests: 5 passed.
- Instructor's checker on committed configuration:
  `python3 ../assignment/check_iac.py --path . --tool terraform`: **25/25**,
  including the history checks for state, provider cache and credentials.

The isolated Terraform container and network are destroyed after verification;
`keep_locally = true` retains the downloaded image. Existing application files,
workloads and Kubernetes configuration are unchanged.

The supplied Terraform and Ansible workflows also validate pull requests.
The Terraform workflow's manual run additionally applies, calls `/healthz` and
always attempts cleanup. CI results are separate from the local results above.

M6's marker grades the default branch, not an unmerged feature branch. The
`infra` pull request must be reviewed and merged by the owner before the course
deadline (6 December 2026, 23:59 Almaty time). This change does not merge itself.
