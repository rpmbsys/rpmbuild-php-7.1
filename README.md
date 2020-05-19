## Build process setup

Sections `Prerequisites` and `Setup` should be done only once per build host

### Requirements

* Docker CE 17.12.0+ (https://docs.docker.com/install/)
* Docker Compose 1.10+ (https://github.com/docker/compose/releases/)

### Prerequisites

1. `Docker` should be installed on build host following these instructions:

    https://docs.docker.com/install/linux/docker-ce/centos/#set-up-the-repository

    and

    https://docs.docker.com/install/linux/docker-ce/centos/#install-docker-ce-1

2. `Docker Compose` should be installed on build host following instructions:

    https://docs.docker.com/compose/install/#install-compose

3. Add your build user into docker group (required to manage docker):

    ```
    usermod -aG docker <username>
    ```

    and relogin

4. Start Docker daemon

    ```
    systemctl enable docker
    systemctl start docker
    ```

5. Port 80 on build host should be free (stop nginx/httpd or move to different
port)

### Setup

1. Clone build repo with submodules (php-7.1 is just an example - it could be
any build repo):

    ```
    git clone --recursive https://github.com/aursu/rpmbuild-php-7.1.git
    cd rpmbuild-php-7.1
    ```

2. Setup build environment:

    2.1. Setup rpmbuild base images

    ```
    docker-compose -f rpmbuild/docker-compose.yml pull
    ```

### Build process


1. Build images

    ```
    docker-compose build
    ```

2. Build packages

    ```
    docker-compose up -d
    ```

    command above will start all build services in background. But it is possible
to run any of them or run in foreground etc

3. Wait until command `docker-compose ps` returns all services in state 'Exit 0'

### Access RPM packages

1. RPM packages is in volumes `rpm6`, `rpm7` and `rpm8`

### Complete build

To complete all build processes run commands:

```
docker-compose down
docker-compose -f rpmbuild/docker-compose.yml down
```

These commands will stop and remove all containers but not build images (see
`docker images` and `docker rmi` commands manuals)
