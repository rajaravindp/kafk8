﻿﻿# kafka on Kubernetes

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
    ![image](https://github.com/user-attachments/assets/b9f793ac-4151-48c3-ad44-df689e378bb1)
+ Verify pods
  - kubectl get pods <br>
    ![image](https://github.com/user-attachments/assets/bbb0f3f2-dc5a-4645-a8ad-640adf9b60dd)
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
    You should be able to see your topic listed here.

At this point, you have successfully deployed Kafka on Kubernetes. 

**Configure Producer and Consumer**
+ Create consumer and producer deployment YAML files and apply them.
  - kubectl apply -f consumer-deploy.yml
  - kubectl apply -f producer-deploy.yml
    
+ Verify deployments and pod creation
  - kubectl get deploy <br>
    ![image](https://github.com/user-attachments/assets/3dd51bd3-93d2-41ed-9f1a-f45ac1c5fdaa)
  - kubectl get po <br>
    ![image](https://github.com/user-attachments/assets/1d64f0e5-72ef-4dbe-8244-e8637d45a3ad) <br>
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


