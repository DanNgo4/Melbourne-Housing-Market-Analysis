// Custom hook to manipulate state for Dropdown + Text inputs 

import { useState } from "react";

const useFormInput = (initialValues = {}) => {
  const [values, setValues] = useState({
    priceRangeInput: "",
    houseTypeInput: "",
    squareMetres: "",
    distance: "",
    rooms: "",
    cars: "",
    ...initialValues, // allows for passing default values
  });

  const handleChange = (key) => (event) => {
    setValues((prevValues) => ({
      ...prevValues,
      [key]: event.target.value,
    }));
  };

  const resetForm = (fieldsToReset = null) => {
    setValues((prevValues) => {
      if (fieldsToReset) {
        // Reset only specified fields
        const updatedValues = { ...prevValues };
        fieldsToReset.forEach((field) => {
          updatedValues[field] = ""; 
        });
        return updatedValues;
      }
      
      // Reset all fields to default by default
      return {
        priceRangeInput: "",
        houseTypeInput: "",
        squareMetres: "",
        distance: "",
        rooms: "",
        cars: "",
      };
    });
  };

  return {
    values,
    handleChange,
    resetForm,
  };
};

export default useFormInput;
