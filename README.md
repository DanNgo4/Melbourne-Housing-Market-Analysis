# Melbourne Housing Market Analysis
## University Project, Second Year Semester 2
Demonstration video: https://www.youtube.com/watch?v=2dRjzrbKD_E 
Overview: This is a team project where we design Machine Learning models related to the Housing Market in Melbourne topic, there were 4 models implemented (2 regression & 2 classification). After that, we developed a full-stack application using React.js and FastAPI to interact with these models using different visualisation tools. 

## Part 1: Building Machine Learning Models
This part involved designing **Machine Learning (ML) models** to analyze and predict features of houses in the Greater Melbourne area. The goal was to identify key attributes that most accurately predict a house's **price** or **type**, providing insights for homebuyers, investors, and market analysts.

Full detailed report: https://docs.google.com/document/d/1zrJn4v9s492xh3V0HwMdBe3EWhmtTHea3MLzxkMdpag/edit?usp=sharing

### Datasets Used
1. **House Sales Data**  
   - **Source**: Kaggle (Melbourne_housing_FULL.csv, 2016-2018).  
   - **Attributes**: Sale price, sale date, council area, property type, land size, etc.  
   - **Records**: 34,857.  
   - **Scope**: Housing sales across Greater Melbourne.

2. **Crime Data**  
   - **Source**: Victorian Government (Crime Statistics Agency, 2024).  
   - **Attributes**: Annual crime records for council areas from 2015-2024.  
   - **Records**: 870.  
   - **Relevance**: Evaluated the impact of crime on housing prices.

3. **Population Data**  
   - **Source**: Australian Bureau of Statistics (2017-18).  
   - **Attributes**: Population growth, migration, and population density by council areas.  
   - **Relevance**: Analyzed housing prices in relation to population trends.

### ML Models Implemented
- **Regression Models**:  
  1. **Random Forest (RF)**: Best-performing regression model with a higher R² score (+6%) and lower Mean Absolute Error (MAE) compared to Polynomial Regression. Its robustness to handle non-linear relationships, noisy data, and outliers made it highly accurate.
![image](https://github.com/user-attachments/assets/d1038236-eb45-431a-8493-9b11bec47834)
![image](https://github.com/user-attachments/assets/d0e6d46b-2d18-497b-a8df-9ca98c6e3a68)
  2. **Polynomial Regression**: Performed moderately but was less effective in managing complex relationships.
![image](https://github.com/user-attachments/assets/171f5f3c-0e14-4575-a364-f4a438d80199)
![image](https://github.com/user-attachments/assets/fbfc1ab2-8576-4f25-b5b2-87dbfbd1dec7)

- **Classification Models**:  
  1. **Random Forest (RF)**: Best-performing classification model, particularly in predicting the minority class (townhouse), with higher precision and F1 scores. It handled imbalanced data effectively.
![image](https://github.com/user-attachments/assets/d7cc6c3a-c913-4e34-9ca7-4678eeda4064)
![image](https://github.com/user-attachments/assets/1df92d63-b3f2-419c-8d22-27b3d6c11d90)
  2. **XGBoost**: Struggled with overfitting and imbalanced data, resulting in lower accuracy than RF.
![image](https://github.com/user-attachments/assets/ebfb2c8f-1cc2-4198-ae12-c47d7114dcc7)

### Key Results
- **Best Model**: Random Forest for both regression and classification tasks.  
- **Conclusion**: Random Forest’s ability to handle complex relationships, noisy data, and class imbalances made it the most effective model for analyzing the Melbourne housing market.

---

## Part 2: Full-Stack Housing Market Prediction System
![image](https://github.com/user-attachments/assets/ff040afa-8edc-4b81-8f94-3afb277f5139)

### Introduction
The housing market in Greater Melbourne is influenced by a myriad of factors that affect property prices. To navigate this complexity, we developed a **Housing Market Prediction System** using Random Forest (RF) Regression and Classification models. These models predict house prices based on historical data and features like location, land size, number of bedrooms, and other attributes.

To enhance usability, we integrated the models into a **full-stack web application** using FastAPI (backend) and React.js (frontend). This setup allows users to input property details and receive instant predictions, along with interactive visualisations.

Full detailed report: https://docs.google.com/document/d/1HUCZsj1-Ldi-AX1dGmQvDOVWd3IDz9_U9Aqr13sGpNQ/edit?usp=sharing

### Visualisation Features:
1. **Line Chart:** Displays trends in median house prices over time across Melbourne council areas.  
2. **Donut Chart:** Shows distribution of median prices across property types, helping users compare housing categories.  
3. **Heatmap:** Geographically visualizes median house prices to explore price variations across Melbourne.

### System Architecture
![image](https://github.com/user-attachments/assets/faa53d90-2a25-4f29-92fc-e369062cd4f5)

### Front-End Implementation
#### Data Visualisations
1. **Line Graph:** Displays predicted price trends over time.  
![image](https://github.com/user-attachments/assets/d928af62-b814-4412-9049-8d34c55f90e2)

2. **Donut Chart:** Visualises price differences and ranges.  
![image](https://github.com/user-attachments/assets/ab6f2d55-6e77-4467-afff-675a960ab183)

3. **Heatmap:** Visualises geographical median house prices.  
![image](https://github.com/user-attachments/assets/64cabbf4-1b06-48d6-8a44-497ad95b41c9)

### Back-End Implementation
#### FastAPI Setup
- **CORS Middleware:** Ensures secure communication between the React.js front-end and FastAPI backend.  
![image](https://github.com/user-attachments/assets/b6b4c663-e39a-4c63-bb7e-39bbda24414d)

- **Uvicorn Server:** Runs the backend on `localhost:8000`.  

#### API Documentation:
| **API Name**            | **URL**                          | **Method** | **Description**                                                                 |
|-------------------------|----------------------------------|------------|---------------------------------------------------------------------------------|
| Predict Price           | `/predict_price/{params}`        | GET        | Returns predicted house price based on inputs.                                 |
| Predict House Type      | `/predict_type/{params}`         | GET        | Returns predicted property type (house/townhouse/unit).                        |
| Save Prediction         | `/add-predicted-values/`         | POST       | Saves prediction data to CSV for reference.                                    |
| Donut Chart Data        | `/donut-data`                   | GET        | Fetches clean data for donut chart visualisation.                              |
| Heatmap Data            | `/geojson/`                     | GET        | Fetches GeoJSON data for creating geographical heatmaps.                       |

### AI Model Integration
#### Random Forest Regression
- Trained on 4 key features and saved into a `.pkl` file for deployment.  

#### Random Forest Classification
- Implemented as a Python class with a `classify()` function that interacts with the `.pkl` model.  

### Conclusion
The **Housing Market Prediction System** effectively addresses the complexities of Melbourne’s housing market. By integrating advanced Random Forest ML models into a user-friendly web app, users can:
1. Input property details and receive instant price predictions.
2. Access visualisations (line charts, donut charts, heatmaps) for market analysis.

This application is a valuable tool for homebuyers, investors, and real estate professionals looking to make informed decisions.
