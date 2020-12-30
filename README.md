# challenge-evolux
Repository for the [evolux challenge backend](https://github.com/EvoluxBR/back-end-test/blob/master/README.md)

The DER of application can be found [here](https://github.com/diegodiogenes/challenge-evolux/blob/master/der.png)

## Setup

For use this project, you should have installed [Docker](https://docs.docker.com/engine/install/) and [Docker Compose]

## Running

For start the application, just run the follow command at the project root :

```shell script
docker-compose up -d --build
```

The application will be running at http://localhost:8000

## Running tests

To execute tests, run this command:

```shell script
docker-compose -f docker-compose/development.yml run hercules-web ./init_config.sh
```

## Routes

You can test this routes with Postman, just import the [environment](https://github.com/diegodiogenes/challenge-evolux/blob/master/Evolux.postman_collection.json)

The application has these routes:
- Auth
  - Login: `[POST] /user/login`
- User
  - Register: `[POST] /user/`
- Currency
  - Index: `[GET] /currency`
  - Store: `[POST] /currency`
  - Update: `[PUT] /currency/:id`
  - Show: `[PUT] /currency/:id`
  - Delete: `[DELETE] /currency/:id`
- Phones
  - Index: `[GET] /phone`
  - Store: `[POST] /phone`
  - Update: `[PUT] /phone/:id`
  - Show: `[PUT] /phone/:id`
  - Delete: `[DELETE] /phone/:id`
