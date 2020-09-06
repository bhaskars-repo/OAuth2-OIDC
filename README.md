### Understanding OAuth2 and OpenID Connect (OIDC)

Sample code that demonstrates the working of the different OAuth2 flows.

The instructions below assume that we are in a directory called `OAuth2`.

### Starting/Stopping the Database (Postgres) and the Keycloak IAM Server

Ensure that both `docker` and `docker-compose` are installed in the system.

- To start, open a terminal and execute the following:

```
docker-compose --env-file ./docker/vars.env -f ./docker/postgres-keycloak.yml up
```

- To stop, open a terminal and execute the following:

```
docker-compose --env-file ./OAuth2/docker/vars.env -f ./OAuth2/docker/postgres-keycloak.yml down
```

### Testing the OAuth2 flows

- For the `Authorization Code` flow, open a terminal and execute the following:

```
python ./AuthCode.py
```

Launch a web browser and type the URL `http://localhost:5000`

- For the `Resource Owner Password` flow, open a terminal and execute the following:

```
python ./OwnerPass.py
```

Launch a web browser and type the URL `http://localhost:5000`

- For the `Client Credentials` flow, open a terminal and execute the following:

```
python ./ClientCredential.py
```

Launch a web browser and type the URL `http://localhost:5000`

### Article(s)

* [Understanding OAuth2 and OpenID Connect](https://www.polarsparc.com/xhtml/OAuth2-OIDC.html)
