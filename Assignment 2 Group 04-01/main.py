import argparse
import polynomial_model
import rf_regression
import rf_classifier
import xgboost_classification


# main function to call different models
def main(model_type):
    if model_type.upper() == "P":
        polynomial_model.main()
    elif model_type.upper() == "R":
        rf_regression.main()
    elif model_type.upper() == "RC":
        rf_classifier.main()
    elif model_type.upper() == "X":
        xgboost_classification.main()
        pass
    

if __name__ == "__main__":
    # initalise the argparser
    parser = argparse.ArgumentParser(description="Run models on Housing Data")
    # Add argument for model type
    parser.add_argument("--model", type=str, choices=['P', 'p', 'R', 'r', 'RC', 'rc', "X", "x"], required=True, help="Model type: 'P' for Polynomial Regression, 'R' for Random Forest")
    args = parser.parse_args()
    main(args.model)