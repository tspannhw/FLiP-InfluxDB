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

## Generate Edge AI IoT Data

```
#!/bin/bash

while :
do

        DATE=$(date +"%Y-%m-%d_%H%M")
        python3 -W ignore /home/nvidia/nvme/minifi-jetson-xavier/demo.py --camera /dev/video0 --network googlenet /home/nvidia/nvme/images/$DATE.jpg  2>/dev/null

        java -jar IoTProducer-1.0-jar-with-dependencies.jar --serviceUrl pulsar://192.168.1.181:6650 --topic 'iotjetsonjson' --message "`tail -1 /home/nvidia/nvme/logs/demo1.log`"

done
```

## Resources

* https://docs.influxdata.com/influxdb/v2.0/write-data/no-code/third-party/
* https://hub.docker.com/_/influxdb
* https://pulsar.apache.org/docs/en/io-influxdb-sink/
* https://github.com/influxdata/nifi-influxdb-bundle
* https://github.com/tspannhw/minifi-xaviernx
* https://www.datainmotion.dev/2020/06/unboxing-most-amazing-edge-ai-device.html
