# CoinAPI

## Docker and OS Setup

1. Install the Docker Client
  - OSX: https://www.docker.com/products/docker-desktop/#/mac
  - Ubuntu
    - docker: https://docs.docker.com/engine/install/ubuntu/
    - docker-compose: https://docs.docker.com/compose/install/
  - Windows: https://www.docker.com/products/docker-desktop/#/windows

## CoinAPI Project setup

The first thing to do is to clone the repository:

```sh
$ git clone git@github.com:ernest-rakhmatulin/coinapi.git
$ cd coinapi
```

To build containers, apply migrations, and start the application run:

```sh
$ docker-compose up
```
