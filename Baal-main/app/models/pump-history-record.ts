import firebase from 'firebase/compat';

class PumpHistoryRecord {
    public id: string;
    public auto: boolean;
    public startTime: Date;
    public endTime: Date;
    public user: string;

    static factory(
        data: firebase.firestore.QueryDocumentSnapshot<firebase.firestore.DocumentData>,
    ): PumpHistoryRecord {
        return new PumpHistoryRecord(
            data.id,
            data.get('auto'),
            data.get('startTime').toDate(),
            data.get('endTime').toDate(),
            data.get('user'),
        );
    }

    constructor(
        id: string,
        auto: boolean,
        startTime: Date,
        endTime: Date,
        user: string,
    ) {
        this.id = id;
        this.auto = auto;
        this.startTime = startTime;
        this.endTime = endTime;
        this.user = user;
    }
}

export default PumpHistoryRecord;
