# SpotAut 

`spotaut` is a dockerized web service to translate LTL formula to automaton. 
It uses spot tool (https://spot.lrde.epita.fr/) for translation.

## Installation 

### Dependencies:
  * Docker 
  * Python3 


### Option 1: Pull docker image (Recommended) 

Pull docker image: `docker pull abhibp1993/spotaut`


### Option 2: Build from Dockerfile

1. Pull github repository `git clone https://github.com/abhibp1993/spotaut.git`
2. From `spotaut` directory, run `docker build -t spotaut .` 


## Usage 

Run the docker image (replace `abhibp1993/spotaut` with `spotaut` if installed using Option 2). 
```
docker run -p 8000:8000 abhibp1993/spotaut 
```

The terminal should show the following message:
```
Starting httpd...
Listening to ('0.0.0.0', 8000)
```

At this stage, we can send http POST requests to server. 
The request must include a JSON message containing a `formula` (string) and 
`options` (list of string). 
```python
msg = {
    "formula": "Fa & F(b & Fc)",
    "options": ["state-based", "buchi", "complete"]
}
```

Supported options: (`buchi` or `cobuchi`), `complete`, `unambiguous`/`unambig`
`state-based`/`sbacc`, (`small` or `det`/`deterministic`), `any`. 

*Remark:* For the options in brackets, only one of them should be used at a time.  
E.g. `options=['buchi', 'cobuchi']` is not acceptable. 
Whereas, `options=['buchi', 'complete', 'unambiguous']` is okay. 


Option `any` allows spot to decide which acceptance condition and options to use. 


The server will respond with one of the two response codes: 
* `200` (Success): Server returns the automaton represented as JSON. It contains the following information:
```
{
    "acceptance": <str Buchi/coBuchi>"
    "num_sets": <str number of acceptance sets in case of rabin>"
    "num_states": <int number of states in automaton>"
    "init_state": <int id of initial state>"
    "atoms": <dict atom-name:atom-id>"
    "name": <str formula>"
    "is_deterministic": <bool is automaton deterministic>"
    "is_unambiguous": <bool is automaton deterministic>"
    "is_state_based_acc": <bool is automaton deterministic>"
    "is_terminal": <bool is automaton deterministic>"
    "is_weak": <bool is automaton deterministic>"
    "is_inherently_weak": <bool is automaton deterministic>"
    "is_stutter_invariant": <bool is automaton deterministic>"
    "state2edges": <dict node-id: <dict node-id: [label, acc-sets]>>
}
```
  
    
* `500` (Error):  Any errors during translation will be included in message. 



## Example

1. Run docker container:
```shell
PS C:\Users\abhib\Downloads\DockerizedSpotServer> docker run -p 8000:8000 spotaut
Starting httpd...
Listening to ('0.0.0.0', 8000)
```

2. Define query in Python file
```python
query = {
    "formula": "Fa",
    "options": ['buchi', 'state-based']
}
```

3. Send the query to the server (Note: IP address is fixed as shown in code)
```python
import requests
import json
out = requests.post("http://localhost:8000/", json=query)
```

4. The server responds with automaton represented as JSON
```json
{'acceptance': 'Büchi',
 'atoms': {'a': 0},
 'init_state': 1,
 'is_deterministic': True,
 'is_inherently_weak': True,
 'is_state_based_acc': True,
 'is_stutter_invariant': True,
 'is_terminal': True,
 'is_unambiguous': True,
 'is_weak': True,
 'name': 'Fa',
 'num_sets': 1,
 'num_states': 2,
 'state2edges': {'0': {'0': ['1', [0]]},
                 '1': {'0': ['a', []], '1': ['!a', []]}}}
```