resource "docker_network" "todo_net" {
  name = "todo-net"
}

resource "docker_volume" "todo_data" {
  name = "todo-data-tf"
}

resource "docker_image" "todo_app" {
  name         = "todo-app:latest"
  keep_locally = true
}

resource "docker_container" "todo_web" {
  count   = var.container_count
  name    = "todo-web-tf-${count.index}"
  image   = docker_image.todo_app.name
  restart = "unless-stopped"

  env = ["DB_PATH=/data/todo.db"]

  networks_advanced {
    name = docker_network.todo_net.name
  }

  ports {
    internal = 8000
    external = var.app_port + count.index
  }

  mounts {
    type   = "volume"
    target = "/data"
    source = docker_volume.todo_data.name
  }
}

output "container_names" {
  description = "Daftar nama container yang dibuat"
  value       = docker_container.todo_web[*].name
}

output "web_urls" {
  description = "URL untuk mengakses aplikasi"
  value       = [for i in range(var.container_count) : "http://localhost:${var.app_port + i}"]
}
