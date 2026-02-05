docker_tool publish -f common/webapps/live_semantic_map/web/docker-config.docker.json.jsonnet
k8s_cli apply -f common/kubernetes/apps/live-semantic-map-react/gz/dev.yaml.jsonnet -n map-dev