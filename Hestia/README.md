# Migrating Directus Instance from https://hestiaai.directus.app/ to Local Docker

This guide describes the steps to migrate a Directus instance from a remote server to a local Docker environment. We assume that you have Docker installed on your local machine and have basic knowledge of Docker and Directus.

## Prerequisites

Before you begin, make sure you have the following:

- Docker installed on your local machine.
- Directus admin credidentials to get all the data from the remote instance.

## Step 1: Set up a Local Docker Environment

First, you need to set up a local Docker environment to host the Directus instance. You can do this by creating a `docker-compose.yml` file that defines the Directus services you want to run. You can use the following `docker-compose.yml` as an example:


This `docker-compose.yml` file defines two services: the Directus application and a PostGres database for storing Directus data. A folder data will be created at the root of this project.

## Step 2: Start the Docker Containers

Start the Directus and database containers using the following command:


$ docker-compose up -d


This command will start the Directus and database services in the background. You can access the Directus instance at `http://localhost:8055/`.

## Step 3: Export the Remote Directus Instance Data

Next, you need to export the Directus data from the remote instance. You can use the `directus_getter.py` script to do this. This script retrieves the schema and data from the remote Directus instance and saves them to files.

Make sure to provide the right `email` and `password` in the terminal when you run `directus_getter.py` script.

$ python3 directus_getter.py


This command will create different files that will be used by the pushing script.

## Step 4: Import Data into the Local Directus Instance

Finally, you can import the Directus data into the local Directus instance using the `directus_push.py` script.

$ python3 directus_push.py

This command will apply the schema and data to the local Directus instance. You should see a message that says "Schema applied" if everything is successful.

## Conclusion

In this guide, we have described the steps to migrate a Directus instance from a remote server to a local Docker environment. With this approach, you can quickly and easily migrate Directus instances between environments without having to manually copy data.

This guide was created the "Projet d'Approfondissement" at HES-SO, as part of my Master's Degree in Data Sciences, followed by Orestis Malaspinas.