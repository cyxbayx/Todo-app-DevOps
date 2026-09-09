variable "app_port" {
  description = "Port eksternal untuk container pertama"
  type        = number
  default     = 8090
}

variable "container_count" {
  description = "Jumlah instance container yang dibuat"
  type        = number
  default     = 2
}
