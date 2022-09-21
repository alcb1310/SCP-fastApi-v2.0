# <center style="font-size: 3rem;">**SCP API**</center>
## Your budgeting api focused in construction companies
![Freelancer](https://img.shields.io/badge/Freelancer-29B2FE?style=for-the-badge&logo=Freelancer&logoColor=white)\
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)
\
![50%](https://progress-bar.dev/15)
## Overview
This is the backend of SCP, it is build in Python using fast-api

## Installation Instructions

- Clone the project
- run `pip install` to install all the libraries required
- Configure your .env file with the variables shown in the Environment variables section 
- Install postgres
- Inside your project directory run `alembic upgrade heads` this will create all the tables in the database 

### Environment variables

The following are the required environment variables required for the app to
work

- **DATABASE_HOSTNAME**: It's the host where the Postgres Database is deployed
- **DATABASE_USERNAME**:  It's the username with access to the Postgres Database
- **DATABASE_PASSWORD**:  It's the user's password to gain access to the database
- **DATABASE_PORT**:  It's the port in which the database listens for connection
- **DATABASE_NAME**: It's the actual name of the database that we will be querying
---
- **SECRET_KEY**: It's the secret key that we will use to sign the tokens
- **ALGORITHM**: It's the algorithm employed to sign the tokens
- **ACCESS_TOKEN_EXPIRE_MINUTES**: It's the time in minutes that will take for the token to expire

