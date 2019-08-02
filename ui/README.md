# UI project for Recommendation System

## Development
Before doing steps bellow, please <code>install nodejs in Window</code> and <code>start api docker</code>

```
cd ui
npm install
npm start
curl localhost:3000
```

## Build docker
```
docker build -t hoanglt705/movie-recommendation-system-ui:0.1 .
docker run -d -p 3000:3000 hoanglt705/movie-recommendation-system-ui:0.1
```
