# Student Information App — Docker and Kubernetes

## 1. Project Overview

The Student Information App is a simple Python web application built using Flask. The application is containerized using Docker and deployed on a Kubernetes cluster using a Deployment and a NodePort Service.

This project demonstrates the basic concepts of containerization, Docker image creation, container execution, Kubernetes deployment, and service exposure.

## 2. Technologies Used

- **Python 3.11** — Application development
- **Flask 3.1.2** — Python web framework
- **Docker Desktop** — Building and running containers
- **Kubernetes** — Application orchestration
- **kubectl** — Managing Kubernetes resources
- **Visual Studio Code** — Writing and editing project files

## 3. Project Structure

```text
student-info-app/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── README.md
│
├── k8s/
│   ├── deployment.yaml
│   └── service.yaml
│
└── screenshots/
    └── Project execution screenshots
```

### File Descriptions

- **app.py:** Contains the Flask application and defines the web page.
- **requirements.txt:** Specifies the Python dependencies required by the application.
- **Dockerfile:** Contains instructions for building the Docker image.
- **k8s/deployment.yaml:** Defines the Kubernetes Deployment and the application container.
- **k8s/service.yaml:** Defines the Kubernetes NodePort Service for accessing the application.
- **screenshots/:** Contains screenshots demonstrating project execution.

## 4. Application Dependencies

The `requirements.txt` file contains:

```text
Flask==3.1.2
```

Flask is required to run the Python web application.

## 5. Dockerfile

The Dockerfile contains the following instructions:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip --default-timeout=300 --retries=10 install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
```

### Explanation

- `FROM python:3.11-slim` selects the Python base image.
- `WORKDIR /app` sets the working directory inside the container.
- `ENV PYTHONDONTWRITEBYTECODE=1` prevents Python from writing bytecode files.
- `ENV PYTHONUNBUFFERED=1` allows Python output to appear immediately.
- `COPY requirements.txt .` copies the dependency file into the image.
- `RUN pip ... install` installs the required Python packages.
- `COPY app.py .` copies the application code into the image.
- `EXPOSE 5000` documents the port used by the application.
- `CMD ["python", "app.py"]` starts the Flask application.

The pip installation command includes a longer timeout and additional retries to handle network delays during dependency installation.

## 6. Building the Docker Image

The following command was used to build the Docker image:

```powershell
docker build -t student-info-app:1.0 .
```

### Explanation

- `docker build` builds an image using the Dockerfile.
- `-t student-info-app:1.0` assigns the image name and version.
- `.` specifies the current directory as the build context.

**Result:** The image was successfully built and tagged as `student-info-app:1.0`.

## 7. Running the Docker Container

The following command starts the application container:

```powershell
docker run -d --name student-app -p 5000:5000 student-info-app:1.0
```

### Explanation

- `-d` runs the container in the background.
- `--name student-app` assigns a name to the container.
- `-p 5000:5000` maps host port 5000 to container port 5000.
- `student-info-app:1.0` specifies the image to run.

### Verifying the Container

```powershell
docker ps
```

This command lists running containers and displays their status and port mappings.

**Result:** The `student-app` container was running successfully.

### Testing the Application

Open the following address in a web browser:

```text
http://localhost:5000
```

The Student Information App page was displayed successfully.

## 8. Setting Up the Kubernetes Cluster

Docker Desktop was used to create a single-node Kubernetes cluster.

The current Kubernetes context was checked using:

```powershell
kubectl config current-context
```

The context displayed:

```text
docker-desktop
```

The cluster nodes were checked using:

```powershell
kubectl get nodes
```

The node `desktop-control-plane` showed the status `Ready`, confirming that the cluster was operational.

## 9. Kubernetes Deployment

The Kubernetes Deployment configuration is stored in:

```text
k8s/deployment.yaml
```

The Deployment defines how the application container runs inside Kubernetes.

### Applying the Deployment

```powershell
kubectl apply -f k8s/deployment.yaml
```

This command creates or updates the Deployment using the configuration file.

### Verifying the Deployment

```powershell
kubectl get deployments
```

This command displays the Deployment status and the number of available replicas.

### Verifying the Pods

```powershell
kubectl get pods
```

This command displays the Pods created by Kubernetes.

**Result:** The application Pod reached the `Running` state, and the Deployment showed one available replica.

## 10. Kubernetes Service

The Kubernetes Service configuration is stored in:

```text
k8s/service.yaml
```

The Service uses the `NodePort` type to expose the application through a port on the Kubernetes node.

### Applying the Service

```powershell
kubectl apply -f k8s/service.yaml
```

### Verifying the Service

```powershell
kubectl get services
```

The Service was displayed with the following configuration:

| Property | Value |
|---|---|
| Service name | `student-info-service` |
| Service type | `NodePort` |
| Cluster IP | `10.96.30.173` |
| Service port | `5000` |
| NodePort | `30080` |

The NodePort configuration was verified successfully.

## 11. Accessing the Application Through Kubernetes

Port forwarding can be used to access the application through the Kubernetes Service.

Run:

```powershell
kubectl port-forward service/student-info-service 8080:5000
```

Keep this terminal running while testing the application.

Open the following address in a browser:

```text
http://localhost:8080
```

The port-forward command maps local port `8080` to port `5000` on the Kubernetes Service.

If the command reports that local port `8080` is already in use, select another available local port, for example:

```powershell
kubectl port-forward service/student-info-service 8081:5000
```

Then open `http://localhost:8081`.

## 12. Errors Encountered and Solutions

### Error 1: Docker Image Build — Network Timeout

**Problem:** The initial Docker image build encountered pip network timeouts while installing Python dependencies.

**Cause:** The package installation process was taking longer than the default network timeout allowed.

**Solution:** The pip installation command in the Dockerfile was updated to include a longer timeout and additional retries:

```dockerfile
RUN pip --default-timeout=300 --retries=10 install --no-cache-dir -r requirements.txt
```

The image was rebuilt using:

```powershell
docker build -t student-info-app:1.0 .
```

**Result:** The Docker image was built successfully.

### Error 2: The `kind` Command Was Not Recognized

**Problem:** Running the following command produced a PowerShell error:

```powershell
kind load docker-image student-info-app:1.0
```

PowerShell reported that `kind` was not recognized as a command.

**Cause:** The standalone `kind` command-line tool was not available in the terminal.

**Solution:** The Kubernetes context was checked using:

```powershell
kubectl config current-context
```

The output was:

```text
docker-desktop
```

The cluster was also checked using:

```powershell
kubectl get nodes
```

The node showed the status `Ready`. The locally built Docker image was already available, and the application Deployment was subsequently created successfully without using the `kind` command.

**Result:** The Deployment was created, and the application Pod reached the `Running` state.

## 13. Useful Commands Summary

| Purpose | Command |
|---|---|
| Build Docker image | `docker build -t student-info-app:1.0 .` |
| Run Docker container | `docker run -d --name student-app -p 5000:5000 student-info-app:1.0` |
| List running containers | `docker ps` |
| Check Kubernetes context | `kubectl config current-context` |
| Check Kubernetes nodes | `kubectl get nodes` |
| Apply Deployment | `kubectl apply -f k8s/deployment.yaml` |
| Check Deployments | `kubectl get deployments` |
| Check Pods | `kubectl get pods` |
| Apply Service | `kubectl apply -f k8s/service.yaml` |
| Check Services | `kubectl get services` |
| Access Service locally | `kubectl port-forward service/student-info-service 8080:5000` |

## 14. Screenshots and Execution Evidence

The `screenshots/` directory contains the available screenshots used to document the project implementation.

The evidence covers the application code, Docker image build, running container, browser output, Kubernetes cluster, Deployment, Pod, and Service.

## 15. Conclusion

The Student Information App was successfully containerized using Docker and deployed on a Kubernetes cluster.

The Docker image was built successfully, the container ran on port 5000, and the application was accessible through a web browser. Kubernetes Deployment and Service resources were created and verified using `kubectl`.

This project demonstrates the basic workflow of developing a Python web application, packaging it into a Docker image, running a container, and deploying the application using Kubernetes.
