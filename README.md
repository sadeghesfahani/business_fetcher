# setup

```shell script
pip install -e ".[dev]"
pre-commit install
python manage.py migrate
python manage.py createsuperuser
```


# Deploy with Docker

## Install Docker

    - curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    - sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    - sudo apt-get update
    - sudo apt-get install -y docker-ce
    - sudo service docker start
    - sudo service docker status


##  Run docker command without sudo
    - sudo groupadd docker
    - sudo usermod -aG docker $USER
    - Restart the system.


## Install Docker Compose
    - sudo curl -L "https://github.com/docker/compose/releases/download/1.23.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    - sudo chmod +x /usr/local/bin/docker-compose



## Run the Docker Compose to start the system
    - docker-compose up -d --force-recreate --build
    - docker-compose exec rikfetcherapp bash -c "cd /opt/services/app/src && python manage.py migrate"

#### create superuser for public schema
    - docker-compose exec rikfetcherapp bash -c "cd /opt/services/app/src && python manage.py createsuperuser"
    - username: hhhhhh
    - email: ceo@hhhh.com
    - password: hhhhh@123

#### To view admin
    go to localhost:9999/admin
    go to http://ip:9999/admin