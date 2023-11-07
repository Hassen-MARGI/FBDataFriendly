@echo off

IF "%~1"=="" (
    ECHO EC2 instance public IP
    GOTO :EOF
)

REM ZOOKEEPER
SET ARGUMENT=%~1
"ssh -i Margi.pem ec2-user@ec2-%ARGUMENT%.compute-1.amazonaws.com"
timeout /t 5 /nobreak
FOR /D %%D IN (kafka*) DO (
    CD "%%D"
    IF NOT ERRORLEVEL 1 (
        ECHO Changed to directory: %%D
        GOTO :DirectoryFound
    )
)
"bin/zookeeper-server-start.sh config/zookeeper.properties"


REM KAFKA-SERVER
start cmd /k "ssh -i Margi.pem ec2-user@ec2-%ARGUMENT%.compute-1.amazonaws.com
timeout /t 5 /nobreak
FOR /D %%D IN (kafka*) DO (632
+6
+3

    CD "%%D"
    IF NOT ERRORLEVEL 1 (
        ECHO Changed to directory: %%D
        GOTO :DirectoryFound
    )
)
export KAFKA_HEAP_OPTS='-Xmx256M -Xms128M'
bin/kafka-server-start.sh config/server.properties

REM KAFKA-PRODUCER
start cmd /k "ssh -i Margi.pem ec2-user@ec2-%ARGUMENT%.compute-1.amazonaws.com
timeout /t 5 /nobreak
FOR /D %%D IN (kafka*) DO (
    CD "%%D"
    IF NOT ERRORLEVEL 1 (
        ECHO Changed to directory: %%D
        GOTO :DirectoryFound
    )
)
export KAFKA_HEAP_OPTS='-Xmx256M -Xms128M'
bin/kafka-server-start.sh config/server.properties

REM KAFKA-CONSUMER
start cmd /k "ssh -i Margi.pem ec2-user@ec2-%ARGUMENT%.compute-1.amazonaws.com
timeout /t 5 /nobreak
FOR /D %%D IN (kafka*) DO (
    CD "%%D"
    IF NOT ERRORLEVEL 1 (
        ECHO Changed to directory: %%D
        GOTO :DirectoryFound
    )
)
export KAFKA_HEAP_OPTS='-Xmx256M -Xms128M'
bin/kafka-server-start.sh config/server.properties
