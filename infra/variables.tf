variable "image" {
  description = "The public Notes API Docker image pinned to its full source commit SHA."
  type        = string
  # Lowercase owner and repository. Never :latest.
  default = "ghcr.io/sagynaliev/notes-api:6c48884f3331cecdbf1358cd1271f0d2e7328633"
}

variable "internal_port" {
  description = "The port my service listens on inside the container - the contract's PORT"
  type        = number
  default     = 8080
}

variable "host_port" {
  description = "The port on my laptop: http://localhost:<host_port>/healthz"
  type        = number
  default     = 8080
}

variable "restart_policy" {
  description = "What Docker does when my service exits: no, on-failure, always or unless-stopped"
  type        = string
  default     = "no"
}

variable "container_name" {
  description = "The Docker container name; override it when another lab container already exists."
  type        = string
  default     = "inf345-app"
}

variable "network_name" {
  description = "The Docker network name dedicated to the lab container."
  type        = string
  default     = "inf345-net"
}
