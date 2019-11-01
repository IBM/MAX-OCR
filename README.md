[![Build Status](https://travis-ci.com/IBM/MAX-OCR.svg?branch=master)](https://travis-ci.com/IBM/MAX-OCR) [![Website Status](https://img.shields.io/website/http/max-ocr.max.us-south.containers.appdomain.cloud/swagger.json.svg?label=api+demo)](http://max-ocr.max.us-south.containers.appdomain.cloud/)  
[<img src="docs/deploy-max-to-ibm-cloud-with-kubernetes-button.png" width="400px">](http://ibm.biz/max-to-ibm-cloud-tutorial) 

# IBM Developer Model Asset Exchange: Optical Character Recognition

This repository contains code to instantiate and deploy an optical character recognition model. This model takes an
image of text as an input and returns the predicted text. This model was trained on 20 samples of 94 characters from 8
different fonts and 4 attributes (regular, bold, italic, bold + italic) for a total of 60,160 training samples. Please
see the paper [An Overview of the Tesseract OCR Engine](https://storage.googleapis.com/pub-tools-public-publication-data/pdf/33418.pdf)
for more detailed information about how this model was trained.

The code in this repository deploys the model as a web service in a Docker container. This repository was developed as
part of the [IBM Code Model Asset Exchange](https://developer.ibm.com/code/exchanges/models/) and the public API is
powered by [IBM Cloud](https://ibm.biz/Bdz2XM).

## Model Metadata

| Domain        | Application                   | Industry | Framework  | Training Data          | Input Data Format |
|---------------|-------------------------------|----------|------------|------------------------|-------------------|
| Image & Video | Optical Character Recognition | General  | n/a        | Tesseract Data Files   | Image (PNG/JPG)   |


## References

* _Smith, Ray._ ["An overview of the Tesseract OCR engine."](https://storage.googleapis.com/pub-tools-public-publication-data/pdf/33418.pdf)
    Ninth International Conference on Document Analysis and Recognition (ICDAR 2007). Vol. 2. IEEE, 2007.

## Licenses

| Component | License | Link  |
| ------------- | --------  | -------- |
| This repository | [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) | [LICENSE](LICENSE) |
| Model Code (3rd party) | [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) | [Tesseract OCR Repository](https://github.com/tesseract-ocr/tesseract/blob/master/LICENSE) |
| Test Samples | [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) | [Sample README](samples/README.md)

## Prerequisites

* `docker`: The [Docker](https://www.docker.com/) command-line interface. Follow the
[installation instructions](https://docs.docker.com/install/) for your system.
* The minimum recommended resources for this model is 2GB Memory and 2 CPUs.

# Deployment options

* [Deploy from Docker Hub](#deploy-from-docker-hub)
* [Deploy on Red Hat OpenShift](#deploy-on-red-hat-openshift)
* [Deploy on Kubernetes](#deploy-on-kubernetes)
* [Run Locally](#run-locally)

## Deploy from Docker Hub

To run the docker image, which automatically starts the model serving API, run:

```bash
$ docker run -it -p 5000:5000 codait/max-ocr
```

This will pull a pre-built image from Docker Hub (or use an existing image if already cached locally) and run it.
If you'd rather checkout and build the model locally you can follow the [run locally](#run-locally) steps below.

## Deploy on Red Hat OpenShift

You can deploy the model-serving microservice on Red Hat OpenShift by following the instructions for the OpenShift web
console or the OpenShift Container Platform CLI [in this
tutorial](https://developer.ibm.com/tutorials/deploy-a-model-asset-exchange-microservice-on-red-hat-openshift/),
specifying `codait/max-ocr` as the image name.

## Deploy on Kubernetes

You can also deploy the model on Kubernetes using the latest docker image on Docker Hub.

On your Kubernetes cluster, run the following commands:

```bash
$ kubectl apply -f https://raw.githubusercontent.com/IBM/MAX-OCR/master/max-ocr.yaml
```

The model will be available internally at port `5000`, but can also be accessed externally through the `NodePort`.

A more elaborate tutorial on how to deploy this MAX model to production on [IBM Cloud](https://ibm.biz/Bdz2XM) can be
found [here](http://ibm.biz/max-to-ibm-cloud-tutorial).

## Run Locally

To build and deploy the model to a REST API using Docker, follow these steps:

1. [Build the Model](#1-build-the-model)
2. [Deploy the Model](#2-deploy-the-model)
3. [Use the Model](#3-use-the-model)
4. [Development](#4-development)
5. [Cleanup](#5-cleanup)


### 1. Build the Model

Clone the `MAX-OCR` repository locally. In a terminal, run the following command:

```bash
$ git clone https://github.com/IBM/MAX-OCR.git
```

Change directory into the repository base folder: 

```bash
$ cd MAX-OCR
```

To build the docker image locally, run:

```bash
$ docker build -t max-ocr .
```

All required model assets will be downloaded during the build process. _Note_ that currently this docker image is CPU
only (we will add support for GPU images later).


### 2. Deploy the Model

To run the docker image, which automatically starts the model serving API, run:

```bash
$ docker run -it -p 5000:5000 max-ocr
```

By default, Cross-Origin Resource Sharing (CORS) is disabled. To _enable_ CORS support, include the following -e flag
with your run command:

```bash
$ docker run -it -e CORS_ENABLE='true' -p 5000:5000 max-ocr
```


### 3. Use the Model

The API server automatically generates an interactive Swagger documentation page. Go to `http://localhost:5000` to load
it. From there you can explore the API and also create test requests.

Use the `model/predict` endpoint to load a test image (you can use one of the test images from the `samples` folder) and
get the predicted text for the image from the API.

![pic](/docs/swagger-screenshot.png "Swagger Screenshot")

You can also test it on the command line, for example:

_(using this scanned text image)_

<img src="/samples/quick_start_watson_studio.jpg" width="527" height="209" alt="Sample Image">

```bash
$ curl -F "image=@samples/quick_start_watson_studio.jpg" -XPOST http://localhost:5000/model/predict
```

You should see a JSON response like that below:

```json
{
  "status": "ok",
  "text": [
    [
      "Quick Start with Watson Studio"
    ],
    [
      "Watson Studio is IBM’s hosted notebook service, and you can create",
      "a free account at https://www.ibm.com/cloud/watson-studio. Other",
      "hosted notebook services can be used to run the noteooks as well,",
      "but Watson Studio offers all of the frameworks and languages that",
      "are used for this book’s examples. Once you have created an account",
      "and logged in, you can begin by creating a project and notebook."
    ]
  ]
}
```

### 4. Development

To run the Flask API app in debug mode, edit `config.py` to set `DEBUG = True` under the application settings. You will
then need to rebuild the Docker image (see [step 1](#1-build-the-model)).

### 5. Cleanup

To stop the Docker container, type `CTRL` + `C` in your terminal.
