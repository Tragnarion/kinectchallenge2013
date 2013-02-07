# Telemetry Server

Telemetry server is a simple python web server that collects gameplay events within database. The data can then be recovered/processed later on.

The system supports two type of events: single or batch events. A single event is just a given event that has been pushed alone to the server while a batched event represents a collection of events that has been submited at once. For nor batched events can be only of the same type.

The communication with the server is meant to be made using JSON-RPC 2.0 [1]:

    --> {"jsonrpc": "2.0", "method": "methodName", "params": [42, 23], "id": 1}
    <-- {"jsonrpc": "2.0", "result": 19, "id": 1}

# Refernces
 - [1] JSON-RPC 2.0: http://www.jsonrpc.org/specification