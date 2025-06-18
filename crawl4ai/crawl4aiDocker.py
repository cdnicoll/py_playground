import requests

# For secured instances
def test_secured(api_token):
    headers = {"Authorization": f"Bearer {api_token}"}

    # Basic crawl with authentication
    response = requests.post(
        "http://localhost:11235/crawl",
        headers=headers,
        json={
            "urls": "https://www.nbcnews.com/business",
            "priority": 10
        }
    )
    task_id = response.json()["task_id"]
    print("Task ID:", task_id)

def get_task_status(task_id, api_token):
    headers = {"Authorization": f"Bearer {api_token}"}

    # Basic crawl with authentication
    response = requests.get(
        f"http://localhost:11235/task/{task_id}",
        headers=headers,
    )
    
    # return the response.json
    return response.json()

if __name__ == "__main__":
    task_id = test_secured("your_secret_token")
    print("Task ID:", task_id)
    # response = get_task_status(task_id, "your_secret_token")
    

    # print(response)

    if (response['status'] == 'completed'):
        print(response['result']['markdown'])
    else:
        print("Task not completed yet: ", response['status'])
