#!/bin/bash

while getopts ":hdptc" opt; do
  case ${opt} in
    h )
      printf -- "USAGE: ./run.sh [OPTION]... \n\n" 
      printf -- "-h for HELP, -c for copying trained models, -d for building docker images, -p for running docker images, or -t for TEARDOWN \n\n"  
      exit 1
      ;;
    d )
      FILE=./mlflow.db
      DIRECTORY=./scania_truck_air_presure_fault_detector/models
      if [ -f "$FILE" ]; then
        rm ./mlflow.db
      fi

      if [ -d "$DIRECTORY" ]; then
        rm -r ./scania_truck_air_presure_fault_detector/models
      fi
      # build train test and mlflow image
      docker-compose build --no-cache
      exit 1
      ;;
    p )
      # Spin up container
      docker-compose up
      exit 1
      ;;
    c )
      FILE=./mlflow.db
      DIRECTORY=./scania_truck_air_presure_fault_detector/models
      if [ -f "$FILE" ]; then
        rm ./mlflow.db
      fi

      if [ -d "$DIRECTORY" ]; then
        rm -r ./scania_truck_air_presure_fault_detector/models
      fi

      docker cp train-pipeline-image:/app/scania_truck_air_presure_fault_detector/models ./scania_truck_air_presure_fault_detector
      docker cp train-pipeline-image:/app/artifacts ./
      docker cp mlflow-image:/app/mlflow.db .
      exit 1
      ;;
    t )
      # Turn off mlflow-image container is running.
      running_app_container=`docker ps | grep mlflow-image | wc -l`
      if [ $running_app_container -gt "0" ]
      then
        docker kill mlflow-image
      fi
    
      # If mlflow-image container is off then remove it.
      existing_app_container=`docker ps -a | grep mlflow-image | grep Exit | wc -l`
      if [ $existing_app_container -gt "0" ]
      then
        docker rm mlflow-image
      fi

      # Turn off test-image container is running.
      running_app_container=`docker ps | grep test-image | wc -l`
      if [ $running_app_container -gt "0" ]
      then
        docker kill test-image
      fi
      # If test-image container is off then remove it.
      existing_app_container=`docker ps -a | grep test-image | grep Exit | wc -l`
      if [ $existing_app_container -gt "0" ]
      then
        docker rm test-image
      fi
      # Turn off train-pipeline-image container is running.
      running_app_container=`docker ps | grep train-pipeline-image | wc -l`
      if [ $running_app_container -gt "0" ]
      then
        docker kill train-pipeline-image
      fi
      # If train-pipeline-image container is off then remove it.
      existing_app_container=`docker ps -a | grep train-pipeline-image | grep Exit | wc -l`
      if [ $existing_app_container -gt "0" ]
      then
        docker rm train-pipeline-image
      fi
      exit 1
      ;;
    \? )
      printf "Invalid option: %s" "$OPTARG" 1>&2
      exit 1
      ;;
  esac
done
shift $((OPTIND -1))

printf -- "USAGE: ./run.sh [OPTION]... \n\n" 
printf -- "-h for HELP, -c for copying trained models, -d for building docker images, -p for running docker images, or -t for TEARDOWN \n\n"  
exit 1
;;