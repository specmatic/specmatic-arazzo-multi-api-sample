# **From REST to Events, gRPC, and GraphQL: API Workflow Testing and Mocking with a Single Arazzo Spec**

APIs rarely work in isolation. Real-world usage involves multiple steps across synchronous REST calls, gRPC and GraphQL APIs, and asynchronous events, where the outcome of each step determines the journey a particular interaction takes. While testing individual endpoints is necessary, it's not sufficient. It is equally important to validate how those APIs and events work together as part of a real workflow.

Enter the [Arazzo Specification](https://www.openapis.org/arazzo-specification) V1.2, which describes complete workflows including inputs, outputs, step dependencies, and success/failure criteria, across [OpenAPI](https://www.openapis.org/) (REST), [AsyncAPI](https://www.asyncapi.com/) (events), [gRPC](https://grpc.io/, and [GraphQL](https://graphql.org/). In this sample project, we'll demonstrate how you can leverage [Specmatic Arazzo](https://specmatic.io/features/author-test-arazzo-api-workflows-drag-drop-simplicity/) to drive end-to-end API workflow testing and mocking in a completely no-code manner.

You will learn how Arazzo + Specmatic enables shift-left testing of entire API journeys, spanning REST, gRPC, and GraphQL operations as well as async events. You'll see how mocking complete workflows can unblock frontend teams, simulate event-driven flows, and accelerate CI pipelines. The session will also walk through the full lifecycle of how we design a multi-step journey, author or generate an Arazzo spec to capture it, and ensure both providers and consumers adhere to the same contract; thereby enabling independent, parallel development and deployment of services and components in complex, event-driven microservice architectures.

This repository showcases a microservices-based architecture for product retrieval, order placement, inventory reservation, and order lifecycle management. The system combines synchronous REST, gRPC, and GraphQL APIs with asynchronous Kafka-based event processing to achieve scalability, resilience, and loose coupling.

---

## 📋 Prerequisites

Ensure the following are installed:

* **Specmatic Studio**
- [https://www.docker.com/products/docker-desktop/](https://hub.docker.com/r/specmatic/specmatic-studio)

* **Container Management Applications**
- [Docker Desktop, Podman Desktop, Rancher Desktop, or Colima](https://docs.specmatic.io/references/docker_images.html#docker-desktop-alternatives)

---

## 🗺 API Workflow

![API Workflow](./assets/workflow.gif)

## 🗺 Sequency Diagram

![Sequency Diagram](./assets/flow.svg)

---

## 🔧 Setup

### Clone the project

```shell
git clone https://github.com/specmatic/specmatic-arazzo-multi-api-sample
cd specmatic-arazzo-multi-api-sample
```

---

## 🚀 Running the Project

Start the full stack using Docker Compose:

```shell
docker compose up --build
```

This launches the following services:

| Service                  | Port  | Description                    |
|--------------------------|-------|--------------------------------|
| **Location gRPC**        | 50051 | Provides user location details |
| **Products GraphQL API** | 4000  | Returns products by location   |
| **Order API**            | 3002  | Handles order lifecycle        |
| **Warehouse API**        | 3003  | Manages inventory operations   |
| **Kafka**                | 9092  | Internal broker port           |
| **Postgres**             | 5432  | Shared database                |

---

## 🧩 Components

### **Location Service**

* Provides user-specific location details through the `location.v1.LocationService/GetUserLocation` gRPC method.
* Serves as the authoritative source for user–location mapping.

### **Products Service**

* Exposes a GraphQL query to fetch products by location code.
* Validates product availability before ordering.

### **Order Service**

* Consumes events from Kafka (e.g., `create-orders`).
* Manages the order lifecycle (PENDING → ACCEPTED → OUT_FOR_DELIVERY).
* Publishes order updates back to Kafka.

### **Warehouse Service**

* Reserves and confirms inventory for incoming orders.
* Sends updates back to the Order Service through Kafka.

### **Kafka**

* Backbone for event-driven communication.
* Decouples services for scalable, fault-tolerant workflows.

---

## 🔌 Communication Model

### **Synchronous gRPC Calls**

Used for immediate operations:

* Fetching user location details

### **Synchronous GraphQL Calls**

Used for immediate operations:

* Retrieving available products by location

### **Synchronous REST Calls**

Used for immediate operations:

* Getting order status
* Updating delivery status

### **Asynchronous Kafka Events**

Used for background or long-running workflows:

* Order creation
* Inventory reservation

This combination supports resilience, scalability, and eventual consistency.

---

## 📦 Kafka Topics

| Topic                     | Purpose                                    |
| ------------------------- | ------------------------------------------ |
| `create-orders`           | Initiates the order creation workflow      |
| `wip-orders`              | Orders pending inventory confirmation      |
| `accepted-orders`         | Orders successfully confirmed and reserved |

## Execute Workflow via Codex

```text
I've started all the services in docker. I would like you to take specifications/PlaceOrder.arazzo.yaml and specifications/
  PlaceOrder.arazzo_input.json and execute the workflow?
```
