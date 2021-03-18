# HTTP health checks

HTTP health checks, HHC, is a system to perform HTTP health checks and publish the results of each check to Kafka. At same time, a consumer to persist those checks in a Postgres table is provided.

The two parts of the system are named `checks` and `writer`.


## Basic usage

The easiest way to start using the  `checker` and `writer` tools can easily be run using [Docker Compose](https://docs.docker.com/compose/).

Let's run `checks` to start doing HTTP checks and publish the results to Kafka.

```
$ docker-compose run checks \
    --kafka-brokers KAFKA_HOST:KAFKA_PORT \
    --kafka-topic KAFKA_TOPIC \
    --kafka-ssl-key-path [KAFKA_SSL_KEY_PATH] \
    --kafka-ssl-cert-path [KAFKA_SSL_CERT_PATH] \
    --kafka-ssl-ca-path [KAFKA_SSL_CA_PATH]
```

In order to run `writer`:

```
docker-compose run writer \
    --db-name DB_NAME \
    --db-host DB_HOST \
    --db-port DB_PORT \
    --db-user DB_USER \
    --db-password DB_PASSWORD \
    --db-sslmode [DB_SSL_MODE] \
    --db-sslrootcert [DB_CA_PEM_PATH] \
    --kafka-brokers KAFKA_HOST:KAFKA_PORT \
    --kafka-topics KAFKA_TOPIC \
    --kafka-group-id KAFKA_GROUP_ID \
    --kafka-ssl-key-path [KAFKA_SSL_KEY_PATH] \
    --kafka-ssl-cert-path [KAFKA_SSL_CERT_PATH] \
    --kafka-ssl-ca-path [KAFKA_SSL_CA_PATH]
```

If using any of the `_PATH` options, you can put your credential files in `./data` and reference them as `/data/`, ex: `./data/kafka.key` is referenced in the command line as `/data/kafka.key`

In case you want to use the infrastructure provided by this repository you can run:

```
$ docker-compose run infra
```

It'll spawn a kafka, zookeeper and postgres instance


## Architecture

The code is organized in small classes each trying to perform a single task and all of them work together injecting them into a `Worker` class that orchestrates the work to be done.

## Checks

`checks` code is organized so the list of targets to check against is provided through a `Repository` instance. This repository implements a hardcoded repository in `checks/checks/repositories/hardcoded.py`. Other repositories can be easily added and be injected into the working logic.

A `Worker` object will orchestrate the logic to be executed by the `Repository`, `Job` and `Producer`.

HTTP GET requests are performed concurrently using `aiohttp` so the process doesn't do those checks in sequence. The logic for the HTTP check is organized in `checks/checks/jobs/http_check.py`. The design allows to add other jobs easily.

Health check results are serialized as JSON in Kafka using this schema:

```
{
  "url": string,
  "response_time": int,
  "status_code": int,
  "re_match": bool,
  "error": string
}
```

## Writer

Other `Worker` object will take care of managing the `Consumer` and `Job` objects to so the consumer will get a batch of messages, will be deserialied and those will be written to DB using a bulk `INSERT`.

## Postgres schema

First time using Postgres. I've followed a very naive approach with next schema:


```
CREATE TABLE IF NOT EXISTS http_check_result (
    url text,
    timestamp timestamp default current_timestamp,
    response_time int,
    status_code integer NULL,
    re_match bool NULL,
    error text NULL
);
```

I am using `psycopg2` since I've seen it's very widely used.

Things to improve:

1. An index on `(url, timestamp)` would be very helpful to do queries per `url` and using a time range so we can do some `response_time` aggregations per time buckets, error rates, etc...
2. We could shard the database using a `url` hash as key

## Testing

Each component, `writer` and `checks`, have tests and can be run using Docker Compose too, which is useful for the functional tests. In https://app.circleci.com/pipelines/github/jondeandres/web-checks we can see the public builds for the repository (Circleci free account is required).

In `./circleci/config.yml` can be found details about how tests can be run.
