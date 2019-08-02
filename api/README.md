# API Project

API for Recommendation system

## Docker

### Development

- Use GitBash to run these commands below 

```
cd docker
docker build -t hoanglt705/movie-recommendation-system:0.1 .
docker run -d -p 5000:5000 hoanglt705/movie-recommendation-system:0.1
cd ..
curl localhost:5000/top_trend -H "Content-Type: application/json"
```

### Usage

- Download the docker image from Docker Hub

```
docker pull hoanglt705/mlproject01:0.1
docker run -d -p 5000:5000 hoanglt705/movie-recommendation-system:0.1
curl localhost:5000/top_trend -H "Content-Type: application/json"
```
