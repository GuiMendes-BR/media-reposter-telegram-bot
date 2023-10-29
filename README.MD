# Python Dev Environment

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Contributing](../CONTRIBUTING.md)

## About <a name = "about"></a>

This is a basic dev environment using Docker and Docker Compose.

## Getting Started <a name = "getting_started"></a>

After cloning this project you need to ensure that the docker-compose.yml file is configured to your necessities and run the following commands.

Spin environment:
```
docker-compose up -d
```

Recreate a environment (useful when you make changes to the requirements.txt):
```
docker-compose up --build -d
```

Stop environment:
```
docker-compose down
```

You can connect to the container created using VsCode to develop. You can also use debugpy to debug your code running on the container.

Aditionally, if you don't want to use docker-compose and simply create a new container you can use the following commands:

Create an image using:
```
docker build -t image-name .
```

Create a container using:
```
docker run --name container-name -p 80:80 -d -v /$(pwd):/code image-name
```


### Prerequisites

You need to have Docker installed on machine.


