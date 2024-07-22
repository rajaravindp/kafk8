﻿# kafka on Kubernetes

**Prerequisites**
- Software Setup
  * Docker Desktop
  * Minikube
  * kubectl
- Docker Hub account 

**Docker Setup**
+ Get Docker Desktop
 - [Download Docker Desktop](https://www.docker.com/products/docker-desktop/) and follow the installation instructions for your operating system.
+ Start Docker Desktop
  Verify installation using following commands <br>
   - docker --version
   - docker info

**MiniKube Setup**
+ Get Minikube <br>
  - [Download Minikube](https://minikube.sigs.k8s.io/docs/start/?arch=%2Fwindows%2Fx86-64%2Fstable%2F.exe+download)
  - or use a package manager.
+ Start Minikube
  - minikube start --cpus=4 --memory=6144 --driver=docker
  - Check status:
    * minikube status
  - Configure kubectl to use minikube
    * kubectl config use-context minikube

**Kafka Setup in Kubernetes**
Make sure to navigate to the appropriate dir before apply the configurations. 
+ Create your own / customize the YAML files provided in the repo.
+ Apply Kafka and Zookeeper configurations
  - kubectl apply -f zookeeper-deployment.yaml
  - kubectl apply -f kafka-deployment.yaml
  - kubectl apply -f zookeeper-service.yaml
  - kubectl apply -f kafka-service.yaml
+ Verify Kafka and Zookeeper deployments
  - kubectl get deploy <br>
    ![image](https://github.com/user-attachments/assets/de227646-6861-42ba-a185-e09bbaa76576)
+ Verify pods
  - kubectl get pods <br>
    ![image](https://github.com/user-attachments/assets/9e45bc5a-54e0-4cef-89c4-c9fb20388e0c)
+ Similarly verify services
+ Create Kafka topic
  - Get Kafka deployment pod name
    kubectl get pods
  - Access Kafka deployment pod
    kubectl exec <kafka-deployment-pod> -it -- bash
  - Create topic
    kafka-topics --create --topic <your-topic-name> --bootstrap-server localhost:29092 --partitions 1
  - Verify topic creation
    kafka-topics --list --bootstrap-server localhost:9092 <br>
    ![image](https://github.com/user-attachments/assets/cb001f2b-139f-4400-85a2-49b09cc275da)
    You should be able to see your topic listed here.

At this point, you have successfully deployed Kafka on Kubernetes. 

**Configure Producer and Consumer**
+ Create consumer and producer deployment YAML files and apply them.
  - kubectl apply -f consumer-deploy.yml
  - kubectl apply -f producer-deploy.yml
+ Verify deployments and pod creation
  - kubectl get deploy <br>
    ![image](https://github.com/user-attachments/assets/b2d92cf3-c886-4d39-8db5-35706ecf849b)
  - kubectl get po <br>
    ![image](https://github.com/user-attachments/assets/3c44b4fd-75fb-465a-9561-6c4afe462aef) <br>
You should be able to see your pods up and running.

**Create Repo on Docker Hub** <br>
Navigate to https://hub.docker.com/repositories/<your-user-name> and create a repository. 

**Build and Push Docker Images**
+ Ensure you have Dockerfile for consumer
+ Build docker image
  Build docker image for consumer and push it to Docker registry. You do not require a docker image for producer as the image already exists on the registry.
  * To build <br>
    - Navigate to Consumer Dir <br>
      cd consumer <br>
    - To Build Image <br>
      docker build -t consumer . <br>
  * Tag Docker Images <br>
    docker tag consumer <your-username>/<your-repo-name>:latest <br>
  * Push to Hub <br>
    docker push <your-username>/<your-repo-name>:latest <br>
  * cd out <br>
    cd .. <br>

![image](https://github.com/user-attachments/assets/0314a4cd-92cc-4bf0-a1bb-a502648027b2)

**Testing**
+ Access kafka deployment pod <br>
  kubectl exec <kafka-deployment-pod-name> -it -- bash <br>
+ Verify <br>
  kafka-console-consumer --bootstrap-server localhost:29092 --topic <your-topic-name> <br>
  If you cannot see any messages being produced, it is possible that the producer is not currently producing any messages currently. <br>
  Try: kafka-console-consumer --bootstrap-server localhost:29092 --topic <your-topic-name> --from-beginning <br>

**Troubleshooting**
+ Docker Daemon Issues
  * Ensure Docker Desktop is running.
  * Check Docker logs for errors.
+ Minikube Issues
  * minikube stop
  If you encounter errors while stopping
  * minikube delete
  * minikube start
+ Kafka Issues
  Check logs
  * kubectl logs <kafka-pod-name>
  * kubectl logs <zookeeper-pod-name>
+ Network Issues
  * Ensure all services are correctly exposed and reachable.
  * Verify Minikube IP and port mappings if you encounter connectivity issues.


