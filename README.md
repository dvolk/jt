# jt.py

jt.py turns a JSON list into a table

eg to get a list of k8s deployments, their namespace and the containers in them
```
$ k get deployments --all-namespaces -o json | jq .items | env/bin/python jt.py main --columns "metadata.name=deployment_name, metadata.namespace=namespace, spec.template.spec.containers.name=containers"
```

output:
```
| deployment_name                                     | namespace          | containers                                          |
|-----------------------------------------------------+--------------------+-----------------------------------------------------|
| akuity-agent                                        | akuity             | akuity-agent                                        |
| argocd-application-controller                       | akuity             | syncer, argocd-application-controller               |
| argocd-applicationset-controller                    | akuity             | argocd-applicationset-controller                    |
| argocd-image-updater                                | akuity             | argocd-image-updater                                |
```

features:
- nested data
- outputs lists as comma separated values in row
- column filtering
- column renaming

use `list-columns` to print out all possible column names.
