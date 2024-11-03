import React from "react";

//This is the ErrorBoundary Class to catch errors in a react components lifecycle
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  //update hasError to true
  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  //Log after an error is thrown
  componentDidCatch(error, errorInfo) {
    console.log(error, errorInfo);
  }

  //Check if it has an error else display the component
  render() {
    if (this.state.hasError) {
      return <h1>Something went wrong.</h1>;
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
