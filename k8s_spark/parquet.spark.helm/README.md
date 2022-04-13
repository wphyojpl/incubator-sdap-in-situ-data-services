From this directory: `/parquet_test_1/k8s_spark/parquet.spark.helm`
- Copy and update the values from `values.yaml` to another custom `values.yaml` file
- Run this to install the parquet spark

        helm install parquet-t1 . -n bitnami-spark -f ../parquet.spark.helm.values.yaml 

- Run this to uninstall the parquet spark

        helm uninstall parquet-t1 -n bitnami-spark

- Port forward the `service` to access it from outside

        kubectl port-forward service/parquet-t1-parquet-spark-helm -n bitnami-spark 9801:9801
