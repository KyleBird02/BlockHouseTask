# BlockHouseTask - Backend Service

This project is a simple FastAPI application that exposes REST APIs for managing trade orders. It is containerized using Docker and deployed on an AWS EC2 instance with a CI/CD pipeline using GitHub Actions.

---

## Table of Contents
1. [Clone the Repository](#1-clone-the-repository)
2. [Install Dependencies](#2-install-dependencies)
3. [Running Locally](#3-running-locally)
4. [Running with Docker](#4-running-with-docker)
5. [Deploying to AWS EC2 (CI/CD)](#5-deploying-to-aws-ec2-cicd)
6. [Stopping the Service](#6-stopping-the-service)
7. [API Documentation](#api-documentation)

---
## Overview

This project is a backend service built using Python's FastAPI framework. It provides a set of RESTful APIs for managing tasks in the BlockHouse application. The service is containerized with Docker, deployed on an AWS EC2 instance, and follows CI/CD practices using GitHub Actions.

## Features

- **FastAPI** for building high-performance APIs
- **Docker** for containerization
- **GitHub Actions** for CI/CD pipeline
- **AWS EC2** for hosting the service

## Requirements

- Python 3.8+
- Docker
- AWS EC2 instance
- GitHub repository with secrets set up for CI/CD (SSH private key, EC2 IP, etc.)

## Getting Started

### 1. Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/your-username/BlockHouseTask.git
cd BlockHouseTask
```

### 2. Install Dependencies

Install the required dependencies from requirements.txt:

```bash
pip install -r requirements.txt
```

### 3. Running Locally
To run the API locally, use Uvicorn:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at http://localhost:8000.

### 4. Running with Docker
To run the service in a container, build and run the Docker container:

```bash
docker-compose up --build
```

### 5. Deploying to AWS EC2 (CI/CD)
The project uses GitHub Actions for CI/CD. Upon pushing changes to the main branch, the app will be automatically deployed to an AWS EC2 instance using Docker.

### 6. Stopping the Service
To stop the service, you can either stop the Docker container:

``` bash
docker-compose down
```
Or stop the FastAPI server if running locally.

# API Endpoints

### 1. Create Order

**Endpoint: POST /orders**

Description: Creates a new trade order.

Request Body:
```json
{
  "symbol": "AAPL",
  "price": 150.5,
  "quantity": 10,
  "order_type": "buy"
}
```
Response:
```json
{
  "message": "Order created"
}
```
### 2. Retrieve All Orders

Endpoint: GET /orders

Description: Retrieves all stored trade orders.

Response:

```json
{
  "orders": [
    {
      "id": 1,
      "symbol": "AAPL",
      "price": 150.5,
      "quantity": 10,
      "order_type": "buy"
    }
  ]
}
```
### 3. Delete All Orders

Endpoint: DELETE /orders

Description: Deletes all trade orders.

Response:

```json
{
  "message": "All orders deleted"
}
```

### 4. Drop and Recreate Orders Table

Endpoint: DELETE /drop-table

Description: Deletes the orders table and recreates it.

Response:
```json
{
  "message": "Table deleted and recreated"
}
```

# Deployment (Docker & AWS EC2)

The application is deployed using Docker on an AWS EC2 instance via GitHub Actions CI/CD.

### 1. Build & Run Docker Container

```bash
docker-compose up -d --build
```

### 2. Access Running Container
```bash
docker ps
```
