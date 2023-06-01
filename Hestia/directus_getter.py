import json
import requests
import os
import getpass
# Ask for the Directus URL
url = 'https://hestiaai.directus.app'
email = input("Enter your email: ")
password = getpass.getpass("Enter your password: ")

# Authenticate with the Directus instance
responseDeployed = requests.post(f"{url}/auth/login", json={"email": email, "password": password})
#if the authentication is failed, stop the script
if responseDeployed.status_code != requests.codes.ok:
    print("Authentication failed")
    exit()

api_tokenDeployed = responseDeployed.json()["data"]["access_token"]
headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_tokenDeployed}"}

print("Importing all the datas")

# Get all users
try:
    response = requests.get(
        f"{url}/users",
        headers=headers,
    )
    response.raise_for_status()
    users = response.json()['data']
    print(f"Imported {len(users)} users")
    with open("users.json", "w") as f:
        json.dump(users, f)
except Exception as e:
    print(f"Error importing users: {e}")

folder_path = "collections/"

# Create the new folder if it doesn't exist already
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print(f"Folder '{folder_path}' created successfully")
else:
    print(f"Folder '{folder_path}' already exists")

response = requests.get(f"{url}/fields", headers=headers)

#save the schema to a file
with open('fields.json', 'w') as f:
    json.dump(response.json(), f)

response = requests.get(f"{url}/relations", headers=headers)

#save the schema to a file
with open('relations.json', 'w') as f:
    json.dump(response.json()["data"], f)

responseCollection = requests.get(f"{url}/collections", headers=headers)
#save it in a json file
with open("collections.json", "w") as outfile:
    json.dump(responseCollection.json()["data"], outfile)

response = requests.get(f"{url}/schema/snapshot", headers=headers)
#save it to a json file
with open('schema.json', 'w') as f:
    json.dump(response.json(), f, indent=2)

responseCollection = requests.get(f"{url}/collections", headers=headers)
collections = responseCollection.json()["data"]

for collection in collections:
    collection_name = collection["collection"]
    print(f"Getting collection {collection_name}...")
    response = requests.get(f"{url}/items/{collection_name}", headers=headers)
    #check if response is 200
    if response.status_code == requests.codes.ok:
        data = response.json()["data"]
        with open(f"collections/{collection_name}.json", "w") as f:
            json.dump(data, f)
    else:
        print(f"Request failed with status code {response.status_code}")

print("Importing all the files")

# Get all files
try:
    response = requests.get(
        f"{url}/files",
        headers=headers,
    )
    response.raise_for_status()
    files = response.json()['data']
    print(f"Imported {len(files)} files")
except Exception as e:
    print(f"Error importing files: {e}")

folder_path = "files/"

# Create the new folder if it doesn't exist already
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print(f"Folder '{folder_path}' created successfully")
else:
    print(f"Folder '{folder_path}' already exists")

for file in files:
    file_name = file["id"]
    print(f"Getting file {file_name}...")
    response = requests.get(f"{url}/files/{file_name}", headers=headers)
    #check if response is 200
    if response.status_code == requests.codes.ok:
        data = response.json()["data"]
        with open(f"files/{file_name}", "w") as f:
            json.dump(data, f)
    else:
        print(f"Request failed with status code {response.status_code}")

print("Done!")