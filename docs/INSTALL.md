# Installing project for developing on local PC

You have to have the following tools installed prior initializing the project:

- [docker](https://docs.docker.com/engine/installation/)
- [docker-compose](https://docs.docker.com/compose/install/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

## Backend

### Task runner

For easier running of everyday tasks, like:

- run dev server
- run all tests
- run linters
- run celery workers
- ...

We use [invoke](https://pypi.org/project/invoke/).

It provides shortcuts for most of the tasks, so it's like collection of bash scrips
or makefile or `npm scripts`.

To enable autocompletion of invoke commands add this line to your `~/.zshrc`

```bash
source <(inv --print-completion-script zsh)
```

### Python interpreter

Also `invoke` abstract "python interpreter", so you can use both `virtual env`
and `dockerized` python interpreter for working with project
(see `tasks.py` file).

- `virtualenv` is the default approach that requires python interpreter,
virtualenv, etc.
- `dockerized` is simpler for quick starting project and for experienced
developers

Suggested approach is using `virtualenv`

### Services

Project may use external services like Database (postgres), message broker,
cache (redis). For easier set up they are defined in `compose.yaml` file,
and they are automatically prepared / started when using `invoke`.

### Prepare python env

Create separate python virtual environment if you are going to run it in
local:

```bash
uv venv --prompt english-flashcards --seed
uv sync --all-groups && source .venv/bin/activate
```

Set up aliases for docker hosts in `/etc/hosts`:

```text
127.0.0.1 postgres
127.0.0.1 redis
127.0.0.1 mailpit
127.0.0.1 s3.rustfs.localhost
```

Start project initialization that will set up docker containers,
python/system env:

```bash
inv project.init
```

Run the project and go to `localhost:8000` page in browser to check whether
it was started:

```bash
inv django.run
```

That's it. After these steps, the project will be successfully set up.

Once you run `project.init` initially you can start web server with
`inv django.run` command without executing `project.init` call.

## Frontend

You can run frontend application for debugging or testing by simply using
`inv frontend.run`. This command clones frontend repository and puts it in the
parent dir, then installs node packages and runs application. Please, ensure you
installed [volta](https://docs.volta.sh/guide/getting-started) to manage node versions.

**Note**: You can change link/path to frontend app repository in
[invocations/frontend.py](../invocations/frontend.py).

## Access to the deployed application

You will need:

- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [teleport](https://goteleport.com/docs/installation/)
   It's required to use 15.x.x version (that used on server), it could be
   installed with
  - Linux

    ```bash
    curl https://cdn.teleport.dev/install.sh | bash -s 15.5.4 oss

    # On Arch-based distro there may be a problem with `sudo shasum`, in that
    # case just make a symlink and try again
    # sudo ln -s /usr/bin/core_perl/shasum /usr/bin/shasum
    ```

  - MacOS

    ```bash
    curl -O https://cdn.teleport.dev/teleport-15.5.4.pkg
    sudo installer -pkg teleport-15.5.4.pkg -target /
    rm -rf teleport-15.5.4.pkg
    ```

- [pack-cli](https://buildpacks.io/docs/tools/pack/)

Most of needed shortcuts can be called via invoke `inv k8s.###`.

Login and selection of proper k8s cluster performed automatically based on `K8SSettings`
that defined in `tasks.py`. So you can simply start executing tasks, for example:

```bash
inv k8s.python-shell
```

You could select k8s cluster (environment) using:

```bash
# when no `--env` passed - will be used `dev`
inv k8s.set-context --env {env name}
```

To `exec` to deployed application use command `inv k8s.execute`. Also it
provide ability to run any command with proper environment, for example:

```bash
inv k8s.execute --command "python manage.py createsuperuser"
```
