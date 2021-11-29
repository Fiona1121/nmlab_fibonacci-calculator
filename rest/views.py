from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
import json

import os.path as osp
import sys
BUILD_DIR = osp.join(osp.dirname(osp.abspath(__file__)), "../build/service/")
sys.path.insert(0, BUILD_DIR)

import grpc
import fib_pb2
import fib_pb2_grpc
import log_pb2
import log_pb2_grpc

import paho.mqtt.client as mqtt

# Create your views here.
class EchoView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        return Response(data={ 'echo': 'hello world' }, status=200)

class FibView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        FibIP = "127.0.0.1"
        FibPORT = 8080
        FibHOST = f"{FibIP}:{FibPORT}"
        
        MqttIP = "127.0.0.1"
        MqttPORT = 1883
        
        try:
            client = mqtt.Client()
            client.connect(host=MqttIP, port=MqttPORT)
            client.loop_start()
        except ConnectionRefusedError:
            return Response(data={ 'msg': 'ERROR: MQTT is not up' }, status=503)
        
        try:
            req_order = json.loads(request.body)['order']
            client.publish(topic='log', payload=req_order)
            print("PUBLISH [log]:", req_order)
        except KeyError:
            return Response(data={ 'msg': 'ERROR: incorrect POST body' }, status=422)
        
        try:
            with grpc.insecure_channel(FibHOST) as channel:
                stub = fib_pb2_grpc.FibCalculatorStub(channel)
                request = fib_pb2.FibRequest()
                request.order = req_order
                response = stub.Compute(request)
        except:
            return Response(data={ 'msg': 'ERROR: connecting to fib-server failed' }, status=422)
            
        return Response(data={ 'result': response.value }, status=200)
    
class LogView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        LogIP = "127.0.0.1"
        LogPORT = 8888
        LogHOST = f"{LogIP}:{LogPORT}"
        
        try:
            with grpc.insecure_channel(LogHOST) as channel:
                stub = log_pb2_grpc.LogServiceStub(channel)
                request = log_pb2.LogRequest()
                response = stub.Log(request).value[:]
                # print(response)
        except:
            return Response(data={ 'msg': 'ERROR: connecting to fib-server failed' }, status=422)
        
        return Response(data={'history': response}, status=200)