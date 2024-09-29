# Installation

### Install Python

Visit Python downloads and preferrably install the latest version: https://www.python.org/downloads/

### Libraries Required:

The required libraries are as follows: 

- colorama 
- pandas
- numpy
- sklearn
- xgboost
- imblearn
- matplotlib

To install any of these run the below command to install the ones you are missing:

"pip install -r  requirements.txt"

# Running the models

To run it, do the following command "python ./main.py --model X" 

replace 'X' with any of the following letters to choose your model

Model types: 
- 'P' for Polynomial Regression
- 'RR' for Random Forest Regression
- 'RC' for Random Forest Classification
- 'X' for XGBoost Classification

To see the above choices in the terminal run the following command

"python ./main.py --help"

Once it has been run it will visualize the performance of the model as well as print to the terminal the uncleaned and cleaned datasets for easy visualisation of seeing the exact changes that have occured