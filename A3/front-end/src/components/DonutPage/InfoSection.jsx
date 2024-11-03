import { Box, Typography, Table, TableHead, TableCell, TableRow, TableBody } from "@mui/material";

const InfoSection = () => {
    return (
        <Box className="col-span-1 p-4 bg-gray-100 rounded shadow max-w-md mx-auto">
        <Typography variant="h5" className="font-bold">About This Chart</Typography>

        <Typography className="mt-3">
          This chart displays the percentage distribution of house types across price ranges.
          Use the "House Types Distribution" form to filter and highlight specific segments based on your selections. Use the "Predict House Type" form to test out our Random Forest Classification model, which has achieved a 95% accuracy score.
        </Typography>

        <Typography className="mt-4 font-bold">Training Data Info:</Typography>

        <Box className="mt-2">
          <Typography variant="subtitle1" className="font-semibold">Before Resampling:</Typography>
          <Typography className="ml-4">Original training set size: (27723, 6)</Typography>
          <Typography className="ml-4">Class distribution: [House (h): 13943, Townhouse (t): 4242, Unit (u): 9538]</Typography>
        </Box>

        <Box className="mt-2">
          <Typography variant="subtitle1" className="font-semibold">After Resampling (Upsampling):</Typography>
          <Typography className="ml-4">Resampled training set size: (34654, 6)</Typography>
          <Typography className="ml-4">Class distribution: [House (h): 17327, Townhouse (t): 5259, Unit (u): 12068]</Typography>
        </Box>

        <Typography className="mt-4 font-bold">Model Performance Metrics:</Typography>

        <Table className="mt-3">
          <TableHead>
            <TableRow>
              <TableCell className="font-semibold text-lg">Class</TableCell>
              <TableCell align="right" className="font-semibold text-lg">Precision</TableCell>
              <TableCell align="right" className="font-semibold text-lg">Recall</TableCell>
              <TableCell align="right" className="font-semibold text-lg">F1-Score</TableCell>
              <TableCell align="right" className="font-semibold text-lg">Support</TableCell>
            </TableRow>
          </TableHead>
          
          <TableBody>
            <TableRow>
              <TableCell>House (h)</TableCell>
              <TableCell align="right">0.98</TableCell>
              <TableCell align="right">0.94</TableCell>
              <TableCell align="right">0.96</TableCell>
              <TableCell align="right">3384</TableCell>
            </TableRow>

            <TableRow>
              <TableCell>Townhouse (t)</TableCell>
              <TableCell align="right">0.85</TableCell>
              <TableCell align="right">0.90</TableCell>
              <TableCell align="right">0.87</TableCell>
              <TableCell align="right">1017</TableCell>
            </TableRow>

            <TableRow>
              <TableCell>Unit (u)</TableCell>
              <TableCell align="right">0.94</TableCell>
              <TableCell align="right">0.98</TableCell>
              <TableCell align="right">0.96</TableCell>
              <TableCell align="right">2530</TableCell>
            </TableRow>

            <TableRow>
              <TableCell className="font-semibold">Overall Accuracy</TableCell>
              <TableCell align="right" colSpan={4} className="font-bold text-center">0.95</TableCell>
            </TableRow>
          </TableBody>
        </Table>

        <Typography className="mt-4 font-bold">Confusion Matrix:</Typography>
        <Typography className="ml-4">House (h): [3168, 134, 82]</Typography>
        <Typography className="ml-4">Townhouse (t): [41, 911, 65]</Typography>
        <Typography className="ml-4">Unit (u): [27, 22, 2481]</Typography>
      </Box>
    );
};

export default InfoSection;