# Fibonacci Calculator
Homework for NMlab of National Taiwan University, 2021 Fall

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

-   Run the eclipse mosquitto docker container

```bash
$ docker run -d -it -p 1883:1883 -v $(pwd)/mosquitto.conf:/mosquitto/config/mosquitto.conf eclipse-mosquitto
```

-   Start Server 

```bash
# Start fib-calculator gRPC service
$ python3 fib-server.py

# Start logging service
$ python3 log-server.py

# Start Django server
$ python3 manage.py runserver
```

## Using `curl` to perform client request

-   [POST] - /rest/fibonacci/
```bash
$ curl -X POST http://localhost:8000/rest/fibonacci -d '{"order": {NUMBER}}
```

-   [GET] - /rest/logs/
```bash
$ sudo apt-get install httpie
$ http --json http://localhost:8000/rest/tutorial
```
## How the system work
<img width="779" alt="截圖 2021-11-29 下午2 42 50" src="https://user-images.githubusercontent.com/55495526/143820529-18251819-b284-4d65-9782-4d0b26d3ef2c.png">


https://user-images.githubusercontent.com/55495526/143828189-6c078c6b-4c8c-4745-99ee-a02e3c317287.mp4


