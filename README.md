# jt.py

`jt.py` turns a JSON list into a table

## Example

To get a list of kubernetes deployments, their namespace and the containers in them

```
$ k get deployments --all-namespaces -o json | jq .items | \
   env/bin/python jt.py main --columns "metadata.name=deployment_name, metadata.namespace=namespace, spec.template.spec.containers.name=containers"
```

output:

```
| deployment_name                       | namespace          | containers                                  |
|---------------------------------------+--------------------+---------------------------------------------|
| akuity-agent                          | akuity             | akuity-agent                                |
| argocd-application-controller         | akuity             | syncer, argocd-application-controller       |
| argocd-applicationset-controller      | akuity             | argocd-applicationset-controller            |
| argocd-image-updater                  | akuity             | argocd-image-updater                        |
```

Here `spec.template.spec.containers` is a list, and when requesting its `name`, `jt.py` puts them into a row separated with a comma.

## Features

- nested data
- outputs lists as comma separated values in row
- column filtering
- column renaming

## Other

- use `list-columns` to print out all possible column names.
