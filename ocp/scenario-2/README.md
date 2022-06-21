podman pull docker.io/grafana/grafana:8.5.5
IMAGE_REG=$(oc get route default-route -n openshift-image-registry --template='{{ .spec.host }}')
podman login -u $(oc whoami) -p $(oc whoami -t) --tls-verify=false $IMAGE_REG
oc new-project scenario-2

podman tag localhost/python-app:latest $IMAGE_REG/scenario-2/python-app:latest
podman tag docker.io/grafana/grafana:8.5.5 $IMAGE_REG/scenario-2/grafana:latest
podman push $IMAGE_REG/scenario-2/python-app:latest
podman push $IMAGE_REG/scenario-2/grafana:latest

oc get is
oc create -f ocp/scenario-2/python_app_deployment.yaml
oc create -f ocp/scenario-2/python_app_service.yaml
oc create -f ocp/scenario-2/python_app_route.yaml

oc policy add-role-to-user monitoring-edit user1 -n scenario-2

oc create -f ocp/scenario-2/python_app_service_monitor.yaml

oc create -f ocp/scenario-2/grafana_deployment.yaml
oc create -f ocp/scenario-2/grafana_service.yaml
oc create -f ocp/scenario-2/grafana_route.yaml

oc get serviceaccounts
oc serviceaccounts get-token default
	Grafana Data Source Error reading Prometheus: client_error: client error: 403

oc adm policy add-cluster-role-to-user cluster-monitoring-view -z default
oc policy add-role-to-user monitoring-edit user1 -n scenario-2

ADMIN: oc login --token=sha256~yHyimaVv2PK6AvTue_km2ae3lEtps-kA0WvuRFM9xZc --server=https://api.cluster-gwt45.gwt45.sandbox265.opentlc.com:6443

USER: oc login --token=sha256~ocX5wsmLOQ7seFdw2I-bqZZDauvplsRAs2SM_BGHXlQ --server=https://api.cluster-gwt45.gwt45.sandbox265.opentlc.com:6443
