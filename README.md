
universal-datalakehouse-postgres-ingestion-deltastreamer

![Untitled Diagram drawio](https://github.com/soumilshah1995/universal-datalakehouse-postgres-ingestion-deltastreamer/assets/39345855/644128c0-1c07-4b95-b7ed-b342dd0cda38)


# Download Jar 
```
https://drive.google.com/drive/folders/1mCxcapOPbt0TujYZEyBYEz7vnzqmWoxW?usp=share_link
```



Steps:
 - Add pgadmin
 - start the cotainers : docker-compose up --build -d
 - Start minio at port 9000 , username admin , password password
 - Start trino at port 8080 username admin
 - Start pgadmin username ashraf@admin.com , password ashraf Create a server
  - hostname : localhost/metasore_db
  - maintainence database : metasore
  - port : 5432
  - username : hive
  - password : hive

 - Install spark version 3.4.2 : 
    - curl -O https://dlcdn.apache.org/spark/spark-3.4.2/spark-3.4.2-bin-hadoop3.tgz
    - tar -zxvf spark-3.4.2-bin-hadoop3.tgz
    - export SPARK_HOME=spark-3.4.2-bin-hadoop3
    - export PATH=$PATH:$SPARK_HOME/bin
 - Spark 3.4 works with java 7 , 11 not 21 ,So install java 11
    - sdk install java 11.0.22-ms

 - Start kafka develoment environment at port 3040.
  - Add postgres connector in kafka connect , copy commands from [file](./debezium/postgres) and paste.