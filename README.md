# wedpy
basic tool for packaging and building microservices for development. Using this will enable you to define a 
service once in its own Github repository and then use it in multiple projects. This is useful for developers
who want to spin up a project with dependencies. 

## Installation
```wedpy``` can be installed using pip:
```bash
pip install git+https://github.com/yellow-bird-consult/wedpy.git
```

## Packaging a Service
In order for your service to be used by other projects, it must be packaged. This is done by defining a 
```wedding_invite.yml``` file in the root of your service's repository. Wedding invite files will checked by the
```wedpy``` tool when it is run so ```wedpy``` knows how to build and run the service. This file should contain the 
information like the example below:
```yaml
package_name: cerberus
builds:
  - name: cerberus
    default_image_name: cerberus
    default_container_name: cerberus
    git_url: https://github.com/yellow-bird-consult/cerberus.git
    image_url: yellowbirdconsulting/taxonomy-server
    branch: development
    default_image_tag: cerberus
    build_root: "."
    outside_port: 8001
    inside_port: 8001
    main: true
    config:
      DB_URL: postgres://username:password@cerberus_postgres:5432/auth
      SECRET_KEY: secret
      EXPIRE_MINUTES: "60"
      ORG_EMAIL: "@yellowbirdconsulting.co.uk"
      PRODUCTION: false
      TAXONOMIST_URL: taxonomist:8012
      EMAIL_URL: email_server:5003
    build_args:
      ENV: NOT_PRODUCTION
    build_files:
      x86_64: builds/Dockerfile.x86_64
      arm: builds/Dockerfile.aarch64

  - name: cerberus_postgres
    default_image_name: postgres
    default_container_name: cerberus_postgres
    image_url: "postgres"
    default_image_tag: postgres
    outside_port: 5434
    inside_port: 5432
    config:
      POSTGRES_USER: username
      POSTGRES_DB: auth
      POSTGRES_PASSWORD: password

init_builds:
  - name: cerberus
    default_image_name: cerberus_db_init
    default_container_name: cerberus_db_init
    git_url: https://github.com/yellow-bird-consult/cerberus.git
    image_url: yellowbirdconsulting/cerberus-migrations
    branch: development
    default_image_tag: cerberus_db_init
    build_root: "./database"
    config:
      DATABASE_URL: postgres://username:password@cerberus_postgres:5432/auth
    build_args:
      ENV: NOT_PRODUCTION
    build_files:
      x86_64: builds/Dockerfile.x86_64
      arm: builds/Dockerfile.aarch64
```
Here is a breakdown of the fields in the ```wedding_invite.yml``` file:

| Field | Description                                                                                      |
| --- |--------------------------------------------------------------------------------------------------|
| package_name | The name of the package. This is used to identify the package when it is used in other projects. |
| builds | A list of builds that will be run when the package is built.                                     |
| name | The name of the build. This is used to identify the build when it is used in other projects.     |
| default_image_name | The default name of the image that will be built.                                                |
| default_container_name | The default name of the container that will be built.                                            |
| git_url | The url of the git repository that contains the code for the service.                            |
| image_url | The url of the image that will be built if remote is set the ```True```.                         |
| branch | The branch of the git repository that will be used to build the service.                         |
| default_image_tag | The default tag of the image that will be built.                                                 |
| build_root | The root of the build. This is the directory that will be used to build the service.             |
| outside_port | The port that will be used to access the service from outside the container.                    |
| inside_port | The port that will be used to access the service from inside the container.                     |
| main | A boolean value that determines if the service is the main service.                              |
| config | A dictionary of environment variables that will be used to build the service.                    |
| build_args | A dictionary of build arguments that will be used to build the service.                          |

# Using wedpy locally
Prerequisites:

1. Open the target repository and have docker desktop running in the background.

2. From the repository root in your IDE, create two empty folders. One being ```sandbox``` and one being ```post_office```.

3. Assuming wedpy is installed in your virtual environment, and your virtual environment is activated, navigate to the repository root in terminal and you're ready to begin.

Running wedpy:

1. Run the command ```wedpy-install```.

2. Run the command ```wedpy-post```.

3. Run the command ```wedpy-build -dev -no_pool```.

4. Run the command ```wedpy-run -dev```.

Your docker images and containers will now be created, and you can stop and start them as needed in docker desktop from now on.

Troubleshooting:

If you get errors, or run wedpy incorrectly, it might be worth wiping everything and starting again. To do this, wipe all your docker images and containers, and wipe both the ```sandbox``` and ```post_office``` folders. Then repeat the steps above.












