import json
import requests
import os
import time

url = "http://localhost:8055"
project = "directus"
email = "admin@example.com"
password = "d1r3ctu5"

# Authenticate with the Directus instance
response = requests.post(f"{url}/auth/login", json={"email": email, "password": password})
api_token = response.json()["data"]["access_token"]
headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_token}"}

def postItem(collections):
    for collection_file in collections:
        collection_name = os.path.splitext(os.path.basename(collection_file))[0]

        with open(collection_file, "r") as f:
            data = json.load(f)

        # Insert the data into the corresponding collection in your local Directus
        for item in data:
            try:
                response = requests.post(
                    f"{url}/items/{collection_name}",
                    headers=headers,
                    json=item,
                )
                response.raise_for_status()
                print(f"Posted item in {collection_name}: {item['id']}")
            except Exception as e:
                print(f"Error posting item in {collection_name}: {e}")

def patchItem(collections):
    for collection_file in collections:
        collection_name = os.path.splitext(os.path.basename(collection_file))[0]
    
        # Load the data from the saved JSON file
        with open(collection_file, "r") as f:
            data = json.load(f)

        # Insert the data into the corresponding collection in your local Directus
        for item in data:
            try:
                response = requests.patch(
                    f"{url}/items/{collection_name}/{item['id']}",
                    headers=headers,
                    json=item,
                )
                response.raise_for_status()
                print(f"Updated item in {collection_name}: {item['id']}")
            except Exception as e:
                print(f"Error patching item in {collection_name}: {e}")

def createCollection():
    with open("collections.json", "r") as f:
        data = json.load(f)

    for collection in data:
        try:
            response = requests.post(
                f"{url}/collections",
                headers=headers,
                json=collection,
            )
            response.raise_for_status()
            print(f"Collection {collection['collection']} imported")
        except Exception as e:
            try:
                requests.patch(
                f"{url}/collections/{collection['collection']}",
                headers=headers,
                json=collection,
            )
            except:
                print(f"Error importing collection: {e}")

def import_or_update_items(collection, data):
    errors = 0
    for item in data:
        if 'id' in item:
            try:
                response = requests.get(
                    f"{url}/items/{collection}/{item['id']}",
                    headers=headers,
                )
                if response.status_code == 200:
                    response = requests.patch(
                        f"{url}/items/{collection}/{item['id']}",
                        headers=headers,
                        json=item,
                    )
                else:
                    response = requests.post(
                        f"{url}/items/{collection}",
                        headers=headers,
                        json=item,
                    )
                response.raise_for_status()
            except Exception as e:
                errors += 1
    print(f"{len(data)} items imported/updated in {collection} with {errors} errors")

# Import schema
with open("schema.json") as f:
    schema = json.load(f)
    diff = requests.post(f"{url}/schema/diff?force", headers=headers, json=schema['data'])
    try:
        #push the changes to the database
        if(diff.status_code != 204):
            response = requests.post(f"{url}/schema/apply", headers=headers, json=diff.json()['data'])
        if response.status_code == 200 or response.status_code == 204:
            print("Schema applied")
        else:
            print(f"Error applying schema: {response.json()}")
    except Exception as e:
        print(f"Error applying schema: {e}")
        exit()


time.sleep(5)
print("Importing Users")
#get all users
with open('users.json') as f:
    users = json.load(f)

#add users to directus
for user in users:
    user_id = user['id']
    user['role'] = None
    user['city'] = None
    
    #check if user exists
    user_response = requests.get(f"{url}/users/{user_id}", headers=headers)
    if user_response.status_code == 200:
        print(f"User {user_id} already exists")
        continue
    #create user
    user_response = requests.post(f"{url}/users", headers=headers, json=user)
    if user_response.status_code == 200:
        print(f"Created user {user_id}")
    else:
        print(f"Error creating user {user_id}: {user_response.json()}")

time.sleep(5)

print("Importing Files")
#get all files in the folder files
files = os.listdir('files')
data = []
for file in files:
    with open(f'files/{file}') as f:
        data.append(json.load(f))
        
#save the distinct folders
folders = []
for file in data:
    if file['folder'] != None:
        folders.append(file['folder'])
folders = list(set(folders))

#insert the folders
for folder in folders:
    try:
        response = requests.post(
            f"{url}/folders",
            headers=headers,
            json={"name": "test","id": folder},
        )
        response.raise_for_status()
        print(f"Folder {folder} imported")
    except Exception as e:
        print(f"Error importing folder: {e}")


for file in data:
    try:
        response = requests.post(
            f"{url}/files",
            headers=headers,
            json=file,
        )
        response.raise_for_status()
        print(f"File {file['id']} imported")
    except Exception as e:
        print(f"Error importing file: {e}")

time.sleep(5)
print("Importing ALL Collections")
# Ensure that all collections exist
with open("collections.json", "r") as f:
    data = json.load(f)

for collection in data:
    try:
        response = requests.post(
            f"{url}/collections",
            headers=headers,
            json=collection,
        )
        response.raise_for_status()
        print(f"Collection {collection['collection']} imported")
    except Exception as e:
        try:
            requests.patch(
            f"{url}/collections/{collection['collection']}",
            headers=headers,
            json=collection,
        )
        except:
            print(f"Error importing collection: {e}")

time.sleep(5)
print("Importing ALL Items")
# Import collections
directory_path = "collections/"
collection_files = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.endswith(".json")]

for collection_file in collection_files:
    collection = os.path.splitext(os.path.basename(collection_file))[0]
    with open(f"collections/{collection}.json", "r") as f:
        data = json.load(f)
    import_or_update_items(collection, data)

print("Waiting 10 seconds for Directus to catch up...")
time.sleep(10)
print("Importing collections again to ensure all items are imported...")
for collection_file in collection_files:
    collection = os.path.splitext(os.path.basename(collection_file))[0]
    with open(f"collections/{collection}.json", "r") as f:
        data = json.load(f)
    import_or_update_items(collection, data)

print("Forcing Content and Page collections to be synced...")

#Load the data from the saved JSON file
name = "Content"
with open(f'collections/{name}.json', "r") as f:
    data = json.load(f)
#find the collection Content_translation
#test if there is an item id
count = 0
for item in data:
    #delete what is inside the array translations, page
    item["translations"] = []
    item["Page"] = []
    item["thumbnail"] = None
    item["tags"] = []
    item["location"] = None
    item["datasets"] = []
    item["personae_targets"] = []
    item["related_content"] = []
    item["view"] = []
    item["related_pages"] = []
    try:
        response = requests.post(
            f"{url}/items/{name}",
            headers=headers,
            json=item,
        )
        response.raise_for_status()
        print(f"Updated item in {name}: {item['id']}")
    except Exception as e:
        try:
            response = requests.patch(
                f"{url}/items/{name}/{item['id']}",
                headers=headers,
                json=item,
            )
            response.raise_for_status()
            print(f"Updated item in {name}: {item['id']}")
        except Exception as e:
            print(f"Error importing item in {name}: {e}")

name = 'Page'
with open(f'collections/{name}.json', "r") as f:
    data = json.load(f)
    #find the collection Content_translation
    #test if there is an item id
    count = 0
    for item in data:
        #delete what is inside the array translations, page
        item["translations"] = []
        item["content"] = []
        item["websites"] = []
        item["thumbnail"] = None
        try:
            response = requests.post(
                f"{url}/items/{name}",
                headers=headers,
                json=item,
            )
            response.raise_for_status()
            print(f"Updated item in {name}: {item['id']}")
        except Exception as e:
            try:
                response = requests.patch(
                    f"{url}/items/{name}/{item['id']}",
                    headers=headers,
                    json=item,
                )
                response.raise_for_status()
                print(f"Updated item in {name}: {item['id']}")
            except Exception as e:
                print(f"Error importing item in {name}: {e}")

print("Importing collections again to ensure all items are imported..., ONCE AGAIN !!")
for collection_file in collection_files:
    collection = os.path.splitext(os.path.basename(collection_file))[0]
    with open(f"collections/{collection}.json", "r") as f:
        data = json.load(f)
    import_or_update_items(collection, data)

print("Done !")