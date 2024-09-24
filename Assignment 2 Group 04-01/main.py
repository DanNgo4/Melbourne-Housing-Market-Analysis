import argparse
import polynomial_model

#main function
def main(model_type):
    if model_type.upper() == 'P':
        polynomial_model.run_poly()
    elif model_type.upper() == 'R':
        pass
    
if __name__ == "__main__":
    #initalize the argparser
    parser = argparse.ArgumentParser(description="Run models on Housing Data")
    # Add argument for model type
    parser.add_argument("--model", type=str, choices=['P', 'p', 'R', 'r'], required=True, help="Model type: 'P' for Polynomial Regression, 'R' for Random Forest")
    args = parser.parse_args()
    main(args.model)