provider "aws" {
  region = var.region
}

data "aws_vpc" "default" {
  default = true
}

## Instance SG
resource "aws_security_group" "kind_cluster_sg" {
  name        = "kind-cluster-security-group"
  description = "Allow Kind Cluster traffic"
  vpc_id      = data.aws_vpc.default.id

  # For SSH
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Adjust as per your requirement.
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


## Get the latest image 
data "aws_ami" "latest_ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-*-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
  owners = ["099720109477"]
}


## Role for EC2
resource "aws_iam_role" "ec2_ssm_role" {
  name = "ec2-ssm-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })
}

## Permission to send message and receive message from SQS

resource "aws_iam_policy" "sqs_policy" {
  name        = "SQSSendMessagePolicy"
  description = "Allows sending messages to all SQS queues"
  policy      = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = [
          "sqs:SendMessage",
          "sqs:ReceiveMessage",
          "sqs:DeleteMessage",         
          "sqs:GetQueueAttributes" 
        ]
        Resource = "arn:aws:sqs:us-west-2:014337110715:*"
      }
    ]
  })
}

resource "aws_iam_policy" "ssm_policy" {
  name        = "ec2-ssm-policy"
  description = "Allows EC2 to use SSM"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = [
        "ssm:StartSession",
        "ssm:TerminateSession",
        "ssm:SendCommand",
        "ssm:GetCommandInvocation"
      ]
      Resource = "*"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "attach_sqs_policy" {
  role       = "aws_iam_role.ec2_ssm_role.name"
  policy_arn = aws_iam_policy.sqs_policy.arn
}

resource "aws_iam_role_policy_attachment" "attach_ssm_policy" {
  role       = aws_iam_role.ec2_ssm_role.name
  policy_arn = aws_iam_policy.ssm_policy.arn
}

resource "aws_iam_role_policy_attachment" "attach_ssm_managed_policy" {
  role       = aws_iam_role.ec2_ssm_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

resource "aws_iam_instance_profile" "ec2_instance_profile" {
  name = "ec2-ssm-instance-profile"
  role = aws_iam_role.ec2_ssm_role.name
}

## EC2 Instance for running kind cluster
resource "aws_instance" "kind_cluster" {
  ami                    = data.aws_ami.latest_ubuntu.id
  instance_type          = "t3.medium"
  iam_instance_profile   = aws_iam_instance_profile.ec2_instance_profile.name
  vpc_security_group_ids = [aws_security_group.kind_cluster_sg.id]
  user_data = file("${path.module}/../scripts/install.sh")
  
  root_block_device {
    volume_size = 50
    volume_type = "gp2"
  }
  
  tags = {
    Name = "kind-cluster"
  }
}

## SQS Queue

resource "aws_sqs_queue" "kind_cluster_queue" {
  name                      = "kind-cluster-sqs-queue"
  delay_seconds             = 0
  visibility_timeout_seconds = 30
  message_retention_seconds = 345600  # 4 days
  max_message_size          = 262144  # 256 KB
  receive_wait_time_seconds = 10
}

output "queue_url" {
  value = aws_sqs_queue.kind_cluster_queue.url
}

output "queue_arn" {
  value = aws_sqs_queue.kind_cluster_queue.arn
}