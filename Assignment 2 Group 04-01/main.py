import argparse
import polynomial_model
import rf_regression
import rf_classifier

#main function
def main(model_type):
    if model_type.upper() == 'P':
        polynomial_model.run_poly()
    elif model_type.upper() == 'R':
        rf_regression.main()
    elif model_type.upper() == 'RC':
        rf_classifier.main()
        pass
    
if __name__ == "__main__":
    #initalize the argparser
    parser = argparse.ArgumentParser(description="Run models on Housing Data")
    # Add argument for model type
    parser.add_argument("--model", type=str, choices=['P', 'p', 'R', 'r', 'RC', 'rc'], required=True, help="Model type: 'P' for Polynomial Regression, 'R' for Random Forest")
    args = parser.parse_args()
    main(args.model)