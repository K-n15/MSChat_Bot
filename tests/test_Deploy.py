import sys, os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from LoreKeeper import app,TestToken

def TestHookLogic():
    client = app.test_client()
    header = {'TestToken':TestToken}
    response = client.get('/testHook',headers=header)
    if response.status_code != 200:
        print(f"Server Error: {response.status_code}")
        sys.exit(1)

    # 2. Check Content (The real fix)
    json_data = response.get_json()
    if "error" in json_data or "API Error" in str(json_data):
        print(f"AI Generation Failed: {json_data}")
        sys.exit(1)

    print("Testing Call Passed")

if __name__ == "__main__":
    TestHookLogic()