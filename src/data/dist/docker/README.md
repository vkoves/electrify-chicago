In bash, from this `README.md`'s directory:

```bash
docker compose build && MY_UID="$(id -u)" MY_GID="$(id -g)" docker compose up
```

Note: `MY_UID="$(id -u)" MY_GID="$(id -g)"` is to pass permissions to the 
Jupyter user inside the container to make changes that are persistent on the 
host side with appropriate host user permissions; e.g. a Jupyter notebook file 
that a host user can edit.