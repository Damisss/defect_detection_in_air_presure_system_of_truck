#!/bin/bash

while getopts ":hdptc" opt; do
  case ${opt} in
    h )
      printf -- "USAGE: ./run.sh [OPTION]... \n\n" 
      printf -- "-h for HELP, -c for copying prediction results, -d for building docker images, -p for running docker containers, or -t for TEARDOWN \n\n"  
      exit 1
      ;;
    d )
      FILE=./ml_api/prediction_results/results.csv
      if [ -f "$FILE" ]; then
        rm "$FILE"
      fi
      # build docker images
      docker-compose build --no-cache
      exit 1
      ;;
    p )
      # Spin up containers
      docker-compose up
      exit 1
      ;;
    c )
      docker cp api-image:/app/ml_api/prediction_results/results.csv ./ml_api/prediction_results/results.csv
      exit 1
      ;;
    t )
      # Turn off integration-test-image container is running.
      running_app_container=`docker ps | grep integration-test-image | wc -l`
      if [ $running_app_container -gt "0" ]
      then
        docker kill integration-test-image
      fi
      # If integration-test-image container is off then remove it.
      existing_app_container=`docker ps -a | grep integration-test-image | grep Exit | wc -l`
      if [ $existing_app_container -gt "0" ]
      then
        docker rm integration-test-image
      fi
      # Turn off api-image container is running.
      running_app_container=`docker ps | grep api-image | wc -l`
      if [ $running_app_container -gt "0" ]
      then
        docker kill api-image
      fi
      # If api-image container is off then remove it.
      existing_app_container=`docker ps -a | grep api-image | grep Exit | wc -l`
      if [ $existing_app_container -gt "0" ]
      then
        docker rm api-image
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
printf --  "-h for HELP, -c for copying prediction results, -d for building docker images, -p for running docker containers, or -t for TEARDOWN \n\n"
exit 1
;;