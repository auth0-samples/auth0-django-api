# Updating Dependencies

## Install the Tools

```shell
pip3 install pipreqs && pip3 install pip-tools
```

## Run the Tools

```shell
pipreqs --savepath=requirements.in && pip-compile --no-annotate --no-header --upgrade --rebuild --quiet --resolver=backtracking
```
