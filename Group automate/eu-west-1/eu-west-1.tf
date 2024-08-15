terraform {
    required_providers {
        aws = {
            source = "hashicorp/aws"
        }
    }
}

provider "aws" {
  region = "eu-central-1"
}

# VPC
resource "aws_vpc" "my_vpc" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "<replace>"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "my_igw" {
  vpc_id = aws_vpc.my_vpc.id
}

# Subnets
resource "aws_subnet" "subnet_az1" {
  vpc_id                  = aws_vpc.my_vpc.id
  cidr_block             = "10.0.1.0/24"
  availability_zone       = "eu-central-1a"
  map_public_ip_on_launch = true
}

resource "aws_subnet" "subnet_az2" {
  vpc_id                  = aws_vpc.my_vpc.id
  cidr_block             = "10.0.2.0/24"
  availability_zone       = "eu-central-1b"
  map_public_ip_on_launch = true
}

# Route Table for Public Subnet
resource "aws_route_table" "public_subnet_rt" {
  vpc_id = aws_vpc.my_vpc.id
}

# Associate Public Subnets with Route Table
resource "aws_route_table_association" "subnet_az1_association" {
  subnet_id      = aws_subnet.subnet_az1.id
  route_table_id = aws_route_table.public_subnet_rt.id
}

resource "aws_route_table_association" "subnet_az2_association" {
  subnet_id      = aws_subnet.subnet_az2.id
  route_table_id = aws_route_table.public_subnet_rt.id
}

# Default Route for Public Subnet to Internet Gateway
resource "aws_route" "public_subnet_default_route" {
  route_table_id         = aws_route_table.public_subnet_rt.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.my_igw.id
}

# Security Group (Example)
resource "aws_security_group" "my_sg" {
  name = "my-sg"  
  vpc_id = aws_vpc.my_vpc.id
  
  ingress {
      from_port = 80
      to_port = 80
      protocol = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
      from_port = 22
      to_port = 22
      protocol = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
      from_port = 443
      to_port = 443
      protocol = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
      from_port = 0
      to_port = 0
      protocol = "tcp"
      cidr_blocks = [ "0.0.0.0/0" ]
  }
  tags = {
    Name = "<replace>"
  }

}

# Network Interface Cards (NICs)
resource "aws_network_interface" "nic_az1" {
  subnet_id       = aws_subnet.subnet_az1.id
  security_groups = [aws_security_group.my_sg.id]
  tags = {
    Name = "<replace>"
  }
}

resource "aws_network_interface" "nic_az2" {
  subnet_id       = aws_subnet.subnet_az2.id
  security_groups = [aws_security_group.my_sg.id]
  tags = {
    Name = "<replace>"
  }
}

# EC2 Instances
resource "aws_instance" "instance_az1" {
  ami           = "ami-04e601abe3e1a910f"
  instance_type = "t2.micro"
  #subnet_id     = aws_subnet.subnet_az1.id
  availability_zone = "eu-central-1a"
  network_interface {
    device_index = 0
    network_interface_id = aws_network_interface.nic_az1.id
  }
  tags = {
    Name = "<replace>"
  }
}

resource "aws_instance" "instance_az2" {
  ami           = "ami-04e601abe3e1a910f"
  instance_type = "t2.micro"
  #subnet_id     = aws_subnet.subnet_az2.id
  availability_zone = "eu-central-1b"
  network_interface {
    device_index = 0
    network_interface_id = aws_network_interface.nic_az2.id
  }
  tags = {
    Name = "<replace>"
  }
}

# Target Group (Example)
resource "aws_lb_target_group" "my_target_group" {
  name        = "my-target-group"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = aws_vpc.my_vpc.id

  health_check {
    path = "/"
  }
}

# Application Load Balancer (Example)
resource "aws_lb" "my_alb" {
  name               = "my-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.my_sg.id]
  subnets            = [aws_subnet.subnet_az1.id, aws_subnet.subnet_az2.id]

  enable_deletion_protection = false
  enable_http2              = true
  enable_cross_zone_load_balancing = true
}

# target group attachment
resource "aws_lb_target_group_attachment" "my_target_group_attachment" {
  target_group_arn = aws_lb_target_group.my_target_group.arn
  target_id        = aws_instance.instance_az1.id
  port             = 80
}

# target group attachment
resource "aws_lb_target_group_attachment" "my_target_group_attachment2" {
  target_group_arn = aws_lb_target_group.my_target_group.arn
  target_id        = aws_instance.instance_az2.id
  port             = 80
}

#associate load balancer with target group
resource "aws_lb_listener" "my_alb_listener" {
  load_balancer_arn = aws_lb.my_alb.arn
  port              = "80"
  protocol          = "HTTP"
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.my_target_group.arn
  }
}

data "aws_route53_zone" "hosted_zone" {
    name = "doctorsonthemove.org"  
}

resource "aws_route53_record" "site_domain" {
  zone_id = data.aws_route53_zone.hosted_zone.zone_id
  name    = "central"
  type    = "A"

  alias {
    name                   = aws_lb.my_alb.dns_name
    zone_id                = aws_lb.my_alb.zone_id
    evaluate_target_health = true
  }
}

# DynamoDB Table from S3 Data
resource "aws_dynamodb_table" "test-import-table" {
  name             = "my-imported-table"
  hash_key         = "id"

  billing_mode   = "PROVISIONED"
  write_capacity = 5
  read_capacity  = 5

  attribute {
    name = "id"
    type = "S"
  }

  ttl {
    attribute_name = "date"
    enabled        = true
  }

  import_table {
    input_compression_type = "GZIP"
    input_format          = "DYNAMODB_JSON"

    s3_bucket_source {
      bucket     = "doctorsdatainfrag7"
      key_prefix = "AWSDynamoDB/01705325702701-e16f979b/"
    }
  }

  tags = {
    Name = "<replace>"
  }
}
