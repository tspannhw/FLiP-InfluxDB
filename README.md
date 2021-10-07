# FLiP-InfluxDB

FLiP Into InfluxDB with Apache Pulsar


## Docker

```

docker pull influxdb

```

## Pulsar Setup

```
bin/pulsar-admin topics create persistent://public/default/jetsoninflux

bin/pulsar-client consume "persistent://public/default/jetsoninflux" -s "influxr" -n 0
```

## Cloud

```
bin/pulsar-admin sink stop --name influxdb-sink-jetson --namespace default --tenant public
bin/pulsar-admin sinks delete --tenant public --namespace default --name influxdb-sink-jetson
bin/pulsar-admin sinks create --archive ./connectors/pulsar-io-influxdb-2.8.0.nar --tenant public --namespace default --name influxdb-sink-jetson --sink-config-file conf/influxcloud.yml --inputs jetsoninflux --parallelism 1


bin/pulsar-admin sinks get --tenant public --namespace default --name influxdb-sink-jetson
bin/pulsar-admin sinks status --tenant public --namespace default --name influxdb-sink-jetson

# topic:  persistent public default jetsoninflux

```

## Generate Edge AI IoT Data

```

pip3 install paho-mqtt

#!/bin/bash

while :
do

        DATE=$(date +"%Y-%m-%d_%H%M")
        python3 -W ignore /home/nvidia/nvme/minifi-jetson-xavier/demo.py --camera /dev/video0 --network googlenet /home/nvidia/nvme/images/$DATE.jpg  2>/dev/null

# --serviceUrl pulsar://192.168.1.181:6650 --topic 'jetsoninflux' --message "`tail -1 /home/nvidia/nvme/logs/influx.log`"

done
```

## Resources

* https://docs.influxdata.com/influxdb/v2.0/write-data/no-code/third-party/
* https://hub.docker.com/_/influxdb
* https://pulsar.apache.org/docs/en/io-influxdb-sink/
* https://github.com/influxdata/nifi-influxdb-bundle
* https://github.com/tspannhw/minifi-xaviernx
* https://www.datainmotion.dev/2020/06/unboxing-most-amazing-edge-ai-device.html
* https://github.com/tspannhw/FLiP-edgeai
* https://github.com/tspannhw/FLiP-CloudIngest
* https://github.com/tspannhw/StreamingAnalyticsUsingFlinkSQL
* https://www.influxdata.com/blog/nvidia-jetson-series-part-1-jetson-stats/
* https://github.com/rbonghi/jetson_stats/wiki/library
