import requests
import json
import pprint

payload = {
    "formula": "GFa & GFb",
    "options": ['buchi', 'state-based']
}
if __name__ == '__main__':
    print("sending requests")
    out = requests.post("http://localhost:8000/", json=payload)
    # out = requests.post("http://127.0.0.1:8000/", json=payload)

    if out.status_code == 200:
        resp = json.loads(out.text)
        pprint.pprint(resp)
    else:
        print(f"[ERROR] [{out.status_code}] {out.reason}")