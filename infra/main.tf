# The Docker daemon on this machine. WHERE it is (a Unix socket, a Windows
# named pipe, DOCKER_HOST) is a fact about your machine, so it is not written here.
provider "docker" {}

resource "docker_image" "app" {
  name         = var.image
  platform     = "linux/amd64" # what your CI builds (Week 6); Apple-silicon Macs emulate it
  keep_locally = true          # destroy removes the container, not the downloaded image
}

resource "docker_network" "app" {
  name = var.network_name
}

resource "docker_container" "app" {
  name = var.container_name
  # This one line tells Terraform: the image first, then the container.
  image   = docker_image.app.image_id
  restart = var.restart_policy
  env     = ["PORT=${var.internal_port}"]

  # The same platform as the image. Without it, Docker on an Apple-silicon Mac may look
  # for an arm64 copy that was never pulled ("content digest ... not found").
  platform = "linux/amd64"

  lifecycle {
    # Docker reports the platform back as just "linux": without this, every plan
    # would want to replace the container.
    ignore_changes = [platform]
  }

  # Python is available in the Notes API image; no curl installation is needed.
  healthcheck {
    test = [
      "CMD", "python", "-c",
      "import urllib.request; urllib.request.urlopen('http://127.0.0.1:${var.internal_port}/healthz', timeout=2)"
    ]
    interval     = "10s"
    timeout      = "3s"
    start_period = "5s"
    retries      = 3
  }

  ports {
    internal = var.internal_port
    external = var.host_port
  }

  networks_advanced {
    name = docker_network.app.name
  }
}
