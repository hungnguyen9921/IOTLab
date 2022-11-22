class PumpRecord {
    public id: number;
    public status: boolean;
    public name: string;

    constructor(data: {
        id: string;
        name: string;
        data: string;
        unit: string;
    }) {
        this.id = +data.id;
        this.status = data.data === '1';
        this.name = data.name;
    }
}

export default PumpRecord;
