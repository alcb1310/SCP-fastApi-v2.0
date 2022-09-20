# SCP
## Your budgeting app focused in construction companies

### Overview

### Environment variables

The following are the required environment variables required for the app to
work

<ul>
<li>DATABASE_HOSTNAME</li> It's the host where the Postgres Database is deployed
<li>DATABASE_USERNAME</li> It's the username with access to the Postgres Database
<li>DATABASE_PASSWORD</li> It's the user's password to gain access to the database
<li>DATABASE_PORT</li> It's the port in which the database listens for connection
<li>DATABASE_NAME</li> It's the actual name of the database that we will be querying
<hr />
<li>SECRET_KEY</li> It's the secret key that we will use to sign the tokens
<li>ALGORITHM</li> It's the algorithm employed to sign the tokens
<li>ACCESS_TOKEN_EXPIRE_MINUTES</li> It's the time in minutes that will take for the token to expire
</ul>
