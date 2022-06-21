cd ocp/scenario-3/prometheus-image
wget https://github.com/prometheus/prometheus/releases/download/v2.36.0/prometheus-2.36.0.linux-amd64.tar.gz
podman build -t prometheus:latest .
podman tag localhost/prometheus:latest $IMAGE_REG/scenario-3/prometheus:latest
podman tag localhost/python-app:latest $IMAGE_REG/scenario-3/python-app:latest
podman tag docker.io/grafana/grafana:8.5.5 $IMAGE_REG/scenario-3/grafana:latest
oc new-project scenario-3
podman push $IMAGE_REG/scenario-3/prometheus:latest
podman push $IMAGE_REG/scenario-3/python-app:latest
podman push $IMAGE_REG/scenario-3/grafana:latest
oc create -f ocp/scenario-3/python_app_deployment.yaml
oc create -f ocp/scenario-3/python_app_service.yaml
oc create -f ocp/scenario-3/python_app_route.yaml
oc create -f ocp/scenario-3/grafana_deployment.yaml
oc create -f ocp/scenario-3/grafana_service.yaml
oc create -f ocp/scenario-3/grafana_route.yaml
oc create -f ocp/scenario-3/prometheus_deployment.yaml
oc create -f ocp/scenario-3/prometheus_service.yaml
oc create -f ocp/scenario-3/prometheus_route.yaml
oc get pvc

