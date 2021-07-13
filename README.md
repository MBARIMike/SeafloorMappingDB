# Seafloor Mapping Database

*Make MBARI seafloor mapping datasets more accessible and useful*

### Text from the proposal

MBARI has now conducted hundreds of Mapping AUV missions and several dozen 
low altitude survey ROV dives. Much of the resulting data have value to others 
in the MBARI community, but the survey data and data products are only 
accessible to those with both knowledge of where the data are stored, how they 
are organized, and how to run the software used to process the data in maps, 
images, and GIS objects. In order to make the Mapping AUV and LASS survey data 
more accessible, we propose to capture metadata such as geographic location and 
server storage paths in a relational database with a queryable web interface. 
The envisioned system will utilize the same approach and open-source software 
tools as the MBARI STOQS database for water-column data. This system can be 
developed without changing the current file-based structure on the 
SeafloorMapping share or impacting the work-flow for processing the sensor 
data. The data will remain as files on the SeafloorMapping share on Titan. 
Because the Titan server is web-accessible, metadata and data products can be 
mined for populating the database and viewed through the query interface.

### Install a local development system using Docker

#### First time
Install [Docker](https://docker.io) and change directory to a location where 
you will clone this repository. Clone the repo and start the services with
these commands:

```
# cd to a development directory, e.g. ~/dev
mkdir docker_smdb_vol 
git clone git@github.com:mbari-org/SeafloorMappingDB.git
cd SeafloorMappingDB
export SMDB_HOME=$(pwd)
export COMPOSE_FILE=$SMDB_HOME/smdb/local.yml
docker-compose up -d
docker-compose run --rm django python manage.py makemigrations
docker-compose run --rm django python manage.py migrate
docker-compose run --rm django python manage.py createsuperuser
```

Then navigate to http://localhost:8000 to see the web application in local 
development mode.  Log into the admin interface using the credentials you
created in the last step above.

#### Thereafter

```
cd ${SMDB_HOME}
export COMPOSE_FILE=$SMDB_HOME/smdb/local.yml
docker-compose up -d
```


### Deploy a production instance of smdb

1. Clone the repository in a location on your production server with an account that can run docker, e.g.:

```
sudo -u docker_user -i
cd /opt
mkdir docker_smdb_vol && chown docker_user docker_smdb_vol
git clone git@github.com:mbari-org/SeafloorMappingDB.git
cd /opt/SeafloorMappingDB
export SMDB_HOME=$(pwd)
```

2. Acquire certificate files, name them smdb.crt, and smdb.key and place them in `${SMDB_HOME}/compose/production/traefik`

3. Start the app:

```
sudo -u docker_user -i
cd /opt/SeafloorMappingDB
export SMDB_HOME=$(pwd)
export COMPOSE_FILE=$SMDB_HOME/smdb/production.yml
docker-compose up -d
```

4. Navigate to https://smdb.shore.mbari.org to see the production web application (for example).

