# README

This is how you set up an environment for research development.

In bash, from this `README.md`'s directory:

```bash
docker compose build && MY_UID="$(id -u)" MY_GID="$(id -g)" docker compose up
```

Note: `MY_UID="$(id -u)" MY_GID="$(id -g)"` is to pass permissions to the 
Jupyter user inside the container to make changes that are persistent on the 
host side with appropriate host user permissions; e.g. a Jupyter notebook file 
that a host user can edit.

To add Python dependencies:

```bash
docker exec -it docker-bldg-grade-dev-1 bash
cd ~/work/docker
poetry add [name_of_package]
```

To do some research, you can go to the Jupyter Server link that is in the 
compose logs and paste it into your browser. Within the Jupyter GUI, navigate 
to `work/research/building_grade_eda.ipynb` for data exploration.
