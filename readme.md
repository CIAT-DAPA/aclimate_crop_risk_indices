# AClimate crop risk module

![GitHub release (latest by date)](https://img.shields.io/github/v/release/CIAT-DAPA/aclimate_crop_risk_indices) ![](https://img.shields.io/github/v/tag/CIAT-DAPA/aclimate_crop_risk_indices)

This repository contains all related to crop risk indices module for AClimate

## Features

- Generates statistics based on weekly periods, for agroclimatic indicators in perennial crops
- Include data for case use in **data** folder
- Include modules to configure the env in **modules** folder

## Prerequisites

- Python 3.x

## Configure DEV Enviroment

You should create a env to run the code and install the requeriments. Run the following commands in the prompt

````bash
pip install virtualenv
venv env
pip install -r requirements.txt
````

## Install

This module can be used as a library in other Python projects. You can install this module using pip:

````bash
pip install git+https://github.com/CIAT-DAPA/aclimate_crop_risk_indices
````

If you want to download a specific version of orm you can do so by indicating the version tag (@v0.0.0) at the end of the install command 

````bash
pip install git+https://github.com/CIAT-DAPA/aclimate_crop_risk_indices@v0.2.0
````

## Run

You can run the module using the command aclimate_crop_risk followed by the required parameters:

````bash
aclimate_resampling -C PERU -p "D:\\aclimate_crop_risk\\data\\" -s 12 -c frutales 
````

### Params
- -C, --country: Name of the country to be processed.
- -p, --path: Root path where the forecast is running (default: current directory).
- -s, --station: Number of stations to be executed in parallel.
- -c, --crop: Crop name to be processed.