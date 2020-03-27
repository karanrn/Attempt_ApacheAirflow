# ApacheAirflow
Exploring and creating workflows in Apache Airflow workflows

Apache Airflow is python-based workflow based management system developed by Airbnb.<br>
Workflows can be used to automate the pipelines, ETL process. It uses Directed Acyclic Graphs (DAGs) to define worfklows.<br>
A brief understanding of [Airflow DAGs](https://www.astronomer.io/guides/dags/).

**Note**:<br>
* Airflow scheduler runs the DAGs for the given/scheduled time, if the DAG run is successfull we cannot trigger for the same timestamp.
* Airflow SubDAGs are recommended not be used because SubDagOperator and tasks are independent of parent DAG.

**Further reading can be done here** - <br>
[1]: https://airflow.apache.org/docs/stable/index.html <br>
[2]: [Airflow Operators and Hooks](https://github.com/lowks/Airflow/blob/master/docs/tutorial.rst) <br>
[3]: [Snowflake connector](https://docs.snowflake.net/manuals/user-guide/python-connector.html) <br>
[4]: [Connecting to Snowflake using Airflow](https://itnext.io/connect-apache-airflow-to-snowflake-data-warehouse-37936a9edfa1) <br>
[5]: [Airflow SubDAGs](https://www.astronomer.io/guides/subdags/) <br>
[6]: [Slack integration](https://medium.com/datareply/integrating-slack-alerts-in-airflow-c9dcd155105)

---
## For monitoring the DAGs and tasks
Airflow can send metrics to [StatsD](https://github.com/statsd/statsd).<br>
StatsD can send data to backend service for further visualisation and analysis (ex. Datadog). StatsD is composed of three components - client, server and backend. <br>
It sends metrics in UDP packets, if metrics are very important one needs to use TCP connection/client for sending metrics (recently added to StatsD).

**Useful commands:**
To listen to StatsD connection on port 8125
```
while true; do nc -l localhost 8125; done
```

**Further reading on StatsD** - <br>
[1]: [Setup Metrics for Airflow using StatsD](https://airflow.apache.org/docs/stable/metrics.html) <br>
[2]: https://thenewstack.io/collecting-metrics-using-statsd-a-standard-for-real-time-monitoring/ <br>
[3]: [Python StatsD documentation](https://statsd.readthedocs.io/en/v3.3/index.html) <br>
[4]: https://sysdig.com/blog/monitoring-statsd-metrics/ <br>
[5]: https://www.scalyr.com/blog/statsd-measure-anything-in-your-system/ <br>