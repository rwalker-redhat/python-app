Copy prometheus binary into this directory when building image!

```
podman build -t prometheus:1.0 .
```
```
podman run -d -p 9090:9090 --user 1001 --name prometheus -v "/tmp/prometheus/:/var/lib/prometheus:z" prometheus:1.0
```

