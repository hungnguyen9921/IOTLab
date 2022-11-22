import HumidityRecord from './humidity-record';
import SoilHumidityRecord from './soil-humidity-record';
import TemperatureRecord from './temperature-record';
import firebase from 'firebase/compat';

class History {
    private records:
        | HumidityRecord[]
        | TemperatureRecord[];

    public static factory(
        data: firebase.firestore.QuerySnapshot<firebase.firestore.DocumentData>,
        type: 'AIR_HUMIDITY' | 'TEMPERATURE',
    ) {
        if (type === 'AIR_HUMIDITY') {
            return new History(
                data.docs.map((e) => HumidityRecord.databaseFactory(e)),
            );
        } 
        else {
            return new History(
                data.docs.map((e) => TemperatureRecord.databaseFactory(e)),
            );
        }
    }

    private constructor(
        records: HumidityRecord[] | TemperatureRecord[],
    ) {
        this.records = records;
    }

    public filter(start?: number, end?: number): History {
        return new History(
            this.records.filter((e) => {
                if (start) {
                    if (end) {
                        return (
                            Date.parse(e.collectedTime) >= start && Date.parse(e.collectedTime) <= end
                        );
                    } else {
                        return Date.parse(e.collectedTime) >= start;
                    }
                } else {
                    return true;
                }
            }),
        );
    }

    public getRecords():
        | HumidityRecord[]
        | TemperatureRecord[] {
        return this.records;
    }
}

export default History;