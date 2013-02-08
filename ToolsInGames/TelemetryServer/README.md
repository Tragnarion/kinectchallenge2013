# Telemetry Server

Telemetry server is a simple python web server that collects gameplay events within database. The data can then be recovered/processed later on.

The system supports two type of events: single or batch events. A single event is just a given event that has been pushed alone to the server while a batched event represents a collection of events that has been submited at once. For nor batched events can be only of the same type.

The communication with the server is meant to be made using JSON-RPC 2.0 [1]:

    --> {"jsonrpc": "2.0", "method": "methodName", "params": [42, 23], "id": 1}
    <-- {"jsonrpc": "2.0", "result": 19, "id": 1}

## API

### addGameplayEvent

Add a single event to the telemetry system.

    {"jsonrpc": "2.0", "method": "addGameplayEvent", "params": {"type":1, "tag":"playername", "data": {}}, "id": 1}

 * params: JSON input parameter object
 * type: integer used to specify the event type
 * tag: String tag, can be used to group events using a string such as the player name, etc...
 * data: JSON object that represents the event data. Each event can handle it's own data

### addBatchedGameplayEvent

Add a batched event containing a collection of events to the telemetry system.

    {"jsonrpc": "2.0", "method": "addBatchedGameplayEvent", "params": {"type":1, "data": [{}]}, "id": 1}

 * params: JSON input parameter object
 * type: integer used to specify the event type
 * tag: String tag, can be used to group events using a string such as the player name, etc...
 * data: Array of JSON objects that represents the event data. Each event can handle it's own data

# Refernces
 - [1] JSON-RPC 2.0: http://www.jsonrpc.org/specification
