import {
    Avatar,
    Box,
    Card,
    CardContent,
    Grid,
    LinearProgress,
    Typography,
} from '@mui/material';
import ArrowUpwardIcon from '@mui/icons-material/ArrowUpward';
import GrassIcon from '@mui/icons-material/Grass';

const SoilHumidityCard = ({ humidity }) => (
    <Card sx={{ height: '100%' }}>
        <CardContent>
            <Grid
                container
                spacing={3}
                sx={{ justifyContent: 'space-between' }}
            >
                <Grid item>
                    <Typography
                        color="textSecondary"
                        gutterBottom
                        variant="overline"
                    >
                        Độ ẩm đất
                    </Typography>
                    <Typography color="textPrimary" variant="h4">
                        {(humidity ? humidity.value : 0).toString() +
                            ' g/m\u00B3'}
                    </Typography>
                </Grid>
                <Grid item>
                    <Avatar
                        sx={{
                            backgroundColor: 'warning.main',
                            height: 56,
                            width: 56,
                        }}
                    >
                        <GrassIcon />
                    </Avatar>
                </Grid>
            </Grid>
            {/* <Box
        sx={{
          alignItems: 'center',
          display: 'flex',
          pt: 2
        }}
      >
        <ArrowUpwardIcon color="success" />
        <Typography
          variant="body2"
          sx={{
            mr: 1
          }}
        >
          1 g/m&sup3;
        </Typography>
        <Typography
          color="textSecondary"
          variant="caption"
        >
          So với 1 giờ trước
        </Typography>
      </Box> */}
        </CardContent>
    </Card>
);


export default SoilHumidityCard;