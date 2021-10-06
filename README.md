# FLiP-InfluxDB

FLiP Into InfluxDB with Apache Pulsar


## Docker

```

docker pull influxdb

```

## Cloud

```
bin/pulsar-admin sink stop --name influxdb-sink-jetson --namespace default --tenant public
bin/pulsar-admin sinks delete --tenant public --namespace default --name influxdb-sink-jetson
bin/pulsar-admin sinks create --archive ./connectors/pulsar-io-influxdb-2.8.0.nar --tenant public --namespace default --name influxdb-sink-jetson --sink-config-file conf/influxcloud.yml --inputs iotjetsonjson --parallelism 1


bin/pulsar-admin sinks get --tenant public --namespace default --name influxdb-sink-jetson
bin/pulsar-admin sinks status --tenant public --namespace default --name influxdb-sink-jetson


```


## Resources

* https://docs.influxdata.com/influxdb/v2.0/write-data/no-code/third-party/
* https://hub.docker.com/_/influxdb
* https://pulsar.apache.org/docs/en/io-influxdb-sink/
* https://github.com/influxdata/nifi-influxdb-bundle
