// Custom hook to log errors to the console on client side

import { useCallback } from "react";

const useErrorLog = () => {
  return useCallback((error, info) => {
    console.error("Error occurred:", error, info);
  }, []);
};

export default useErrorLog;
