git clone https://github.com/rwalker-redhat/python-app.git
cd python-app
podman build -t python-app:latest .

**IMAGE_REG=$(oc get route default-route -n openshift-image-registry --template='{{ .spec.host }}')**

podman login -u $(oc whoami) -p $(oc whoami -t) --tls-verify=false $IMAGE_REG
oc new-project scenario-1
podman tag localhost/python-app:latest $IMAGE_REG/scenario-1/python-app:latest
podman push $IMAGE_REG/scenario-1/python-app:latest
oc get is

oc create -f ocp/scenario-1/python_app_deployment.yaml
oc get pods
oc create -f ocp/scenario-1/python_app_service.yaml
oc get svc
oc create -f ocp/scenario-1/python_app_route.yaml
oc get routes
curl -X 'GET' 'https://python-app-route-scenario-1.apps.cluster.lab.com/health' -H 'accept: application/json'

**oc policy add-role-to-user monitoring-edit user1 -n scenario-1**

oc create -f ocp/scenario-1/python_app_service_monitor.yaml
oc get servicemonitors

ADMIN: oc login --token=sha256~yHyimaVv2PK6AvTue_km2ae3lEtps-kA0WvuRFM9xZc --server=https://api.cluster-gwt45.gwt45.sandbox265.opentlc.com:6443

USER: oc login --token=sha256~ocX5wsmLOQ7seFdw2I-bqZZDauvplsRAs2SM_BGHXlQ --server=https://api.cluster-gwt45.gwt45.sandbox265.opentlc.com:6443
