# API Project

API for Recommendation system

## Docker

### Development

- Use GitBash to run these commands below 

```
cd docker
docker build -t hoanglt705/movie-recommendation-system-api:0.1 .
docker run -d -p 5000:5000 hoanglt705/movie-recommendation-system-api:0.1

curl localhost:5000/top_trend
curl -X POST -H "Content-Type: application/json" -d '{"title":"Mean Girls"}' http://localhost:5000/content-based
```

### Usage

- Download the docker image from Docker Hub

```
docker pull hoanglt705/movie-recommendation-system-api:0.1
docker run -d -p 5000:5000 hoanglt705/movie-recommendation-system-api:0.1
curl localhost:5000/top_trend
```
