# KeySafe Vault
KeySafe Vault is a dedicated GitHub repository designed to serve as your trusted digital haven. This all-inclusive vault not only shields your passwords and financial data, but also offers a secure home for your cherished photos, videos, and an array of files.

# Prerequisite
- Docker
- docker-compose

# Installation
- Clone this repository and change directory
```
git clone https://github.com/keysafe-vault/keysafe-vault
cd keysafe-vault
```
- Open ```config.env``` and change the variables. Go [here](#Variables)
- Run the following commands
```
docker-compose up -d
```
- After all the containers are up find the container name for ```backend-api``` by running the following command
```
docker ps
```
- Run the following command to create the Databases. Supposing the container name for backend-api is ```backend_backend-api```
```
docker exec -it backend_backend-api python manage.py migrate
```
- Now your application will be available at http://localhost:3000
# Variables
## Backend
- ```DB_PASS``` For PostgreSQL DB Password
- ```API_PORT``` For Backend-API port (only for debugging)
- ```DEBUG``` Put 1 for debugging mode
- ```SECRET_KEY``` Put any random string but make it secret
- ```SQL_ENGINE``` Default django.db.backends.postgresql
- ```SQL_DATABASE```Default keysafe_vault
- ```SQL_USER``` Put PostgreSQL username
- ```SQL_PASSWORD``` Put PostgreSQL password
- ```SQL_HOST``` backend-db (don't change)
- ```SQL_PORT``` 5432 (don't change)
## PostgreSQL
- ```POSTGRES_USER``` Put PostgreSQL username
- ```POSTGRES_PASSWORD``` Put PostgreSQL password
- ```POSTGRES_DB``` keysafe_vault (don't change)
## Middleend
- ```PORT``` Final Application Port (Default=3000)
- ```BACKEND_HOST``` 'http://backend-api' (don't change)
- ```BACKEND_PORT``` 8000 (don't change)
- ```MONGO_URI``` mongodb://mongo-db:27017/ (don't change)
- ```MONGO_DB``` 'usersDB' (don't change)
