import os
import os.path as osp
import sys
BUILD_DIR = osp.join(osp.dirname(osp.abspath(__file__)), "build/service/")
sys.path.insert(0, BUILD_DIR)
import argparse
import threading

import grpc
from concurrent import futures
import log_pb2
import log_pb2_grpc

import paho.mqtt.client as mqtt

history = []

class LogServiceServicer(log_pb2_grpc.LogServiceServicer):

    def __init__(self):
        pass

    def Log(self, request, context):
        response = log_pb2.LogResponse()
        for h in history:
            response.value.append(h)
        return response

class Subscriber():

    def __init__(self) -> None:
        self.MqttIP = '127.0.0.1'
        self.MqttPORT = 1883
        self.client = mqtt.Client()
        
    def run(self):
        self.client.on_message = self.on_message
        self.client.connect(host=self.MqttIP, port=self.MqttPORT)
        self.client.subscribe('log', 0)
        try:
            self.client.loop_forever()
        except KeyboardInterrupt as e:
            pass
    
    def on_message(self, client, obj, msg):
        history.append(int(msg.payload))



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="0.0.0.0", type=str)
    parser.add_argument("--port", default=8888, type=int)
    args = vars(parser.parse_args())

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servicer = LogServiceServicer()
    subscriber = Subscriber()
    log_pb2_grpc.add_LogServiceServicer_to_server(servicer, server)
    try:
        server.add_insecure_port(f"{args['ip']}:{args['port']}")
        server.start()
        print(f"Run gRPC Server at {args['ip']}:{args['port']}")
        subscriber.run()
        server.wait_for_termination()
    except KeyboardInterrupt:
        pass