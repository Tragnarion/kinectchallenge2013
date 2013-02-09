# Telemetry Server

Telemetry server is a simple python web server that collects gameplay events within database. The data can then be recovered/processed later on.

The system supports two type of events: single or batch events. A single event is just a given event that has been pushed alone to the server while a batched event represents a collection of events that has been submited at once. For nor batched events can be only of the same type.

The communication with the server is meant to be made using JSON-RPC 2.0 [1]:

    --> {"jsonrpc": "2.0", "method": "methodName", "params": [42, 23], "id": 1}
    <-- {"jsonrpc": "2.0", "result": 19, "id": 1}

To be able to run the server you need:

 * Python 2.7 [2]
 * Web.py [3]
 * Sqlite3 (pre-installed with python)

To make installation of python packages easier try pip [4] a tool to install python packages from the Pyhton Package Index.

## API

### addGameplayEvent

Add a single event to the telemetry system.

Request:

    {"jsonrpc": "2.0", "method": "addGameplayEvent", "params": {"type":1, "tag":"playername", "data": {}}, "id": 1}

 * params: JSON input parameter object
 * type: Integer used to specify the event type
 * tag: String tag, can be used to group events using a string such as the player name, etc...
 * data: JSON object that represents the event data. Each event can handle it's own data

Response:

    {"jsonrpc": "2.0", "result": [True|False], "id": 1}

 * result: Returns True or False in case we could not add the event

### addBatchedGameplayEvent

Add a batched event containing a collection of events to the telemetry system.

Request:

    {"jsonrpc": "2.0", "method": "addBatchedGameplayEvent", "params": {"type":1, "tag":"playername", "data": [{}]}, "id": 1}

 * params: JSON input parameter object
 * type: Integer used to specify the event type
 * tag: String tag, can be used to group events using a string such as the player name, etc...
 * data: Array of JSON objects that represents the event data. Each event can handle it's own data

Response:

    {"jsonrpc": "2.0", "result": [True|False], "id": 1}

 * result: Returns True or False in case we could not add the event

### getGameplayEvent

Gets a given collection of gameplay events that has been submitted before.

Request:

    {"jsonrpc": "2.0", "method": "getGameplayEvent", "params": {"type":1, "tag":"playername", "id": 1}

 * params: JSON input parameter object
 * type: Integer used to specify the event type
 * tag: String tag, can be used to group events using a string such as the player name, etc...

Response:

    {"jsonrpc": "2.0", "result": [{}], "id": 1}

 * result: Returns a list of gameplay events that has been submitted earlier

# Refernces
 - [1] JSON-RPC 2.0: http://www.jsonrpc.org/specification
 - [2] Python 2.7: http://python.org/
 - [3] Web.py: http://webpy.org/
 - [4] pip: http://www.pip-installer.org/en/latest/
