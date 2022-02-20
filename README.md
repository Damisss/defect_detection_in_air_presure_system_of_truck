# Project description
This project attempts to build a classification methodology(semi supervised learning) to predict the state of scania truck engine based on the given training data ( it contains 164 columns). Firstly, we have performed different sets of validation on the given training files and then follow by inserting all file into a database. After that we have fetch all data from db into a single csv file (this action combined all validated batch files into a single file) and then perform EDA follows by some data preprocessing and 
then run some experimentation using jupyter notebook and mlflow. Finally, we have productionized the project and then trained the selected models.
Training:
<img src="/images/training.png" width="600" height="400"/>

We have packaged project to be installable so that it can be use accross different platforms. 
Prediction:
<img src="/images/prediction.png" width="600" height="400"/>

# Prerequisites
* Docker 

# Start project tests and training
* `cd build_pipeline` 
* `bash run.sh -d` build docker images
* `bash run.sh -p` starts differeent docker contaires
* `bash runs.sh -c` copy trained models and mlflow artifacts to your local machine
* `bash runs.sh -t` turn off and then remove different docker images

# Access Mlflow during taining
* `open browser and type: localhost:1234`

# Make prediction and download the results
* `cd make_preduction`
* `bash run.sh -d` build docker images
* `bash run.sh -p` starts application
* `bash runs.sh -c` copy prediction results from docker container to your local machine
* `bash runs.sh -t` turn off and then remove different docker images

The nvidia/cuda:10.2-base will only get you nvidia-smi. If you need cuDNN or nvcc --version you can pull from other NVIDIA Docker base images, namely: nvidia/cuda:10.2-devel-ubuntu18.0. (gets you nvcc cuda toolkit) andnvidia/cuda:10.2-cudnn7-devel-ubuntu18.04. (gets you cuDNN).

