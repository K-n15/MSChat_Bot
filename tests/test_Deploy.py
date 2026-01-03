import sys, os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from MSChat_Bot.LoreKeeper import app,TestToken

def TestHookLogic():
    client = app.test_client()
    header = {'TestToken':TestToken}
    response = client.get('/testHook',headers=header)
    if response.status_code == 200:
        print("Testing Call Passed")
    else:
        print(f"Testing Call Failed : {response.status_code}")
        sys.exit(1)

if __name__ == "__main__":
    TestHookLogic()