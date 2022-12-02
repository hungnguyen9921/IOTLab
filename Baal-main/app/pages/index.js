import Head from 'next/head';
import { useState, useEffect, useRef, useContext } from 'react';
import { Box, Container, Grid } from '@mui/material';
import AirHumidity from '../components/dashboard/air-humidity';
import DashboardLayout from '../components/dashboard-layout';
import Temperature from '../components/dashboard/temperature';
import AirHumidityCard from '../components/dashboard/air-humidity-card';
import TemperatureCard from '../components/dashboard/temperature-card';
import AreaCard from '../components/dashboard/area-card';
import IotServer from '../controller/adafruit-io';
import TemperatureRecord from '../models/temperature-record';
import AppContext from '../context/app-context';
import LocationController from '../controller/location-controller';
import HumidityRecord from '../models/humidity-record';

const Dashboard = () => {
    const isUnmounted = useRef(false);
    const flag = useRef(false)
    const [temperature, setTemperature] = useState(null);
    const [humidity, setHumidity] = useState(null);
    const [tempRecs, setTempRecs] = useState(null);
    const [airHumRecs, setAirHumRecs] = useState(null);

    const { area, setArea, areas, setAreas } = useContext(AppContext);

    const tempUnsubcriber = useRef(() => {});
    const airUnsubcriber = useRef(() => {});
    const location = areas.length > 0 ? areas[area] : undefined;
    useEffect(() => {
        const timerId = setInterval(() => {
            IotServer.getInstance().getTemperatureRecord().then((res) =>{
                if(res.value >= 35 && flag.current === false){
                    // const messages = {
                    //     to: '',
                    //     body:''
                    // }
                    // fetch('/api/messages',{
                    //     method: 'POST',
                    //     headers:{
                    //         'Content-Type':'application-json'
                    //     },
                    //     body: JSON.stringify(messages)
                    // })
                    console.log("temperature was high");
                    flag.current = true;
                } else if(res.value < 35 && flag){
                    flag.current = false;
                }
            });
        },5000)
        return () => clearInterval(timerId);
    }, [])
    
    useEffect(() => {
        (async () => {
            IotServer.getInstance().subscribeTemperature((tempRecord) => {
                tempUnsubcriber.current();
                tempUnsubcriber.current = LocationController.getInstance().subscribeTemperature(
                                areas[area],
                                (tempRecordRec) => {
                                   if(tempRecordRec.id !== tempRecord.id){
                                        LocationController.getInstance().addTempRecord(
                                            location,
                                            new TemperatureRecord(
                                                tempRecord.id,
                                                tempRecord.deviceId,
                                                tempRecord.value,
                                                tempRecord.name,
                                                tempRecord.collectedTime
                                            ),
                                        );
                                   }
                                },
                            );
                if (!isUnmounted.current) setTemperature(tempRecord);
            })
            IotServer.getInstance().subscribeHumidity((humidRecord) => {
                airUnsubcriber.current();
                airUnsubcriber.current = LocationController.getInstance().subscribeHumidity(
                    areas[area],
                    (humiRecordRec) => {
                       if(humiRecordRec.id !== humidRecord.id){
                            LocationController.getInstance().addHumiRecord(
                                location,
                                new HumidityRecord(
                                    humidRecord.id,
                                    humidRecord.deviceId,
                                    humidRecord.value,
                                    humidRecord.name,
                                    humidRecord.collectedTime
                                ),
                            );
                       }
                    },
                );
                if (!isUnmounted.current) setHumidity(humidRecord);
            })
        }) ()
        
        return () => {
            isUnmounted.current = true;
        };
    }, []);

    useEffect(() => {
        (async () => {
            if (areas.length > 0) {
                var temperatureRecordsData =
                    await LocationController.getInstance().getTemperatureRecords(
                        areas[area],
                    );
                var airHumidityRecordsData =
                    await LocationController.getInstance().getHumidityRecords(
                        areas[area],
                    );

                if (isUnmounted.current) return;
                setTempRecs(temperatureRecordsData);
                setAirHumRecs(airHumidityRecordsData);
            }
        })();
    }, [area, areas]);

                
    return (
        <>
            <Head>
                <title>Dashboard | Greenhouse</title>
            </Head>
            <Box
                component="main"
                sx={{
                    flexGrow: 1,
                    py: 8,
                }}
            >
                <Container maxWidth={false}>
                    <Grid container spacing={3}>
                        <Grid item xl={3} lg={6} sm={6} xs={12}>
                            <TemperatureCard temperature={temperature} />
                        </Grid>
                        <Grid item xl={3} lg={6} sm={6} xs={12}>
                            <AirHumidityCard humidity={humidity} />
                        </Grid>
                        <Grid item xl={3} lg={6} sm={6} xs={12}>
                            <AreaCard sx={{ height: '100%' }} />
                        </Grid>
                        <Grid item lg={12} md={12} xl={12} xs={12}>
                            <AirHumidity
                                records={
                                    airHumRecs ? airHumRecs.getRecords() : []
                                }
                            />
                        </Grid>
                        <Grid item lg={12} md={12} xl={12} xs={12}>
                            <Temperature
                                records={tempRecs ? tempRecs.getRecords() : []}
                            />
                        </Grid>
                    </Grid>
                </Container>
            </Box>
        </>
    );
};

Dashboard.getLayout = (page) => <DashboardLayout>{page}</DashboardLayout>;

export default Dashboard;
