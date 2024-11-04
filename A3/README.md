# Introduction of Project
For this project we had to create a model from which our FastAPI backend connects to and serves the frontend as an API,
the front end is a React based frontend which visualises data used in the model as well as allows the user to enter some inputs and for the AI model to respond through a route in the FastAPI and dynamically update the line graph model predicting a house price on given parameters

# Installation

## Install Python

Visit Python downloads and preferrably install the latest version: https://www.python.org/downloads/

### Python Libraries Required:

The required libraries are as follows: 

- pandas
- fastapi
- uvicorn
- scikit-learn
- colorama
- pydantic

Run the following if you do not have all of them installed

```bash
pip install pandas fastapi uvicorn scikit-learn colorama pydantic
```

## Installing React

Firstly install Node.js from here https://nodejs.org/en/

Once installed run the following

```bash
npm install -g create-react-app  
```

This installs react globally on your system

Next navigate to the front-end folder in the terminal and run the following command

```
cd front-end
npm install
```

This installs the required react packages


# Running the Application
Firstly to run the backend API, navigate to the backend directory than you can run the following once those python packages have been installed

```bash
cd back-end
uvicorn app:app --reload
```

Once you have run the above the backend will be on

Navigate to the frontend folder than run the following to start the react application

```bash
cd front-end
npm start
```

Now the react application should be running and will be avaliable from http://localhost:3000
