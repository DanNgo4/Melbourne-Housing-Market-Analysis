import { FormControl, InputLabel, Select, MenuItem } from "@mui/material";

const DropdownInput = ({ label, value, onChange, options }) => {
    return (
        <FormControl fullWidth variant="outlined" className="bg-white rounded">
            <InputLabel>{label}</InputLabel>
            <Select value={value} onChange={onChange} label={label}>
                <MenuItem value="">All</MenuItem>
                {options.map((option, index) => (
                    <MenuItem key={index} value={option.value}>
                        {option.label}
                    </MenuItem>
                ))}
            </Select>
        </FormControl>
    );
};

export default DropdownInput;
