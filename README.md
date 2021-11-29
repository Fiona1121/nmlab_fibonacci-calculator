# gRPC-with-protobuf

## How to run

-   Install project dependencies

```bash
# Install protobuf compiler
$ sudo apt-get install protobuf-compiler

# Install buildtools
$ sudo apt-get install build-essential make

# Install grpc packages
$ pip3 install -r requirements.txt
```

-   Compile protobuf schema to python wrapper

```bash
$ make
```

-   Start the gRPC service

```bash
$ python3 server.py --ip 0.0.0.0 --port 8080
```

-   Start the gRPC client

```bash
# You will get 55 value computed by the grpc service
$ python3 client.py --ip localhost --port 8080 --order 10
```

# django-rest-tutorial

## How to run

-   Install project dependencies

```bash
$ pip3 install -r requirements.txt
```

-   Migrate database tables

```bash
$ cd mysite/
$ python3 manage.py migrate
```

-   Run the backend server

```bash
$ python3 manage.py runserver 0.0.0.0:8000
```

## Using `curl` to perform client request

```bash
$ curl http://localhost:8000/rest/tutorial
```

Or you can use `http` to send request

```bash
$ sudo apt-get install httpie
$ http --json http://localhost:8000/rest/tutorial
```

# eclipse-mosquitto

## Environment

```
- Linux thinkpad-t480 5.4.0-81-generic #91~18.04.1-Ubuntu SMP Fri Jul 23 13:36:29 UTC 2021 x86_64 x86_64 x86_64 GNU/Linux
- Docker version 20.10.8, build 3967b7d
- Python 3.7.1
```

## How to run

-   Run the eclipse mosquitto docker container

```bash
$ docker run -d -it -p 1883:1883 -v $(pwd)/mosquitto.conf:/mosquitto/config/mosquitto.conf eclipse-mosquitto
```

-   Run the CPU publisher

```bash
$ python3 publisher.py --ip localhost --port 1883 --topic cpu
```

-   Run the MEM publisher

```bash
$ python3 publisher.py --ip localhost --port 1883 --topic mem
```

-   Run the subscriber

```bash
$ python3 subscriber.py --ip localhost --port 1883
```
