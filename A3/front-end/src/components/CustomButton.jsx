import { Button } from "@mui/material";

const CustomButton = ({ variant = "contained", color = "primary", onClick, type = "button", children, disabled = false, className = "" }) => (
  <Button
    variant={variant}
    color={color}
    onClick={onClick}
    type={type}
    disabled={disabled}
    className={`w-full mt-2 ${className}`}
  >
    {children}
  </Button>
);

export default CustomButton;
