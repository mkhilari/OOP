const net = require('net');
const PromiseReadline = require('promise-readline');
const PromiseSocket = require('promise-socket')

const SHIPS = {
    'aircraftcarrier': 5,
    'battleship': 4,
    'submarine': 3,
    'cruiser': 3,
    'destroyer': 2,
};
const COLS = 'abcdefghij'.split('');
const ROWS = '0123456789'.split('');

function sample(array) {
    return array[Math.floor(Math.random() * array.length)];
}

function getShipName(identifier) {
    for (let shipName of Object.keys(SHIPS)) {
        if (shipName.startsWith(identifier)) {
            return shipName;
        }
    }
    return 'unknown';
}

class Connection {
    constructor(host, port=50008) {
        console.log(`Connecting to ${host}:${port}.`)
        this.host = host;
        this.port = port;
        this.socket = new net.Socket();
        this.writer = new PromiseSocket(this.socket);
        this.reader = PromiseReadline(this.socket);
    }

    async connect() {
        await this.writer.connect(this.port, this.host);
    }

    async send(msg) {
        console.log(`> ${msg}`)
        await this.writer.write(msg + '\n');
    }

    async getLine() {
        let line;
        do {
            line = await this.reader.readLine();
            console.log(`< ${line}`);
            if (line == null) {
                return null;
            }
        } while (line == "" || line[0] == ' ');
        return line;
    }

    close() {
        this.socket.destroy();
    }
}

class BattleshipClient {
    constructor(conn, name) {
        this.conn = conn;
        this.name = name;
        this.gameOver = false;
    }

    async configure() {
        await this.conn.send(`id ${this.name}`);
        await this.conn.send(`autodump`);
    }

    async placeShips() {
        let col= 'a', row = 1;
        for (const ship of Object.keys(SHIPS)) {
            await this.conn.send(`place ${ship} ${col}${row} horizontal`);
            await this.conn.getLine();
            row++;
        }
    }

    async waitForGo() {
        while (true) {
            let line = await this.conn.getLine();
            if (line.startsWith('go')) {
                break;
            }
        }
    }

    async shoot() {
        const col = sample(COLS);
        const row = sample(ROWS);
        await this.conn.send(`shoot ${col}${row}`)
        const line = await this.conn.getLine();
        this.handlePlayerResult(line);
    }

    async awaitPartnerTurn() {
        const line = await this.conn.getLine();
        this.handlePartnerResult(line);
    }

    handlePlayerResult(result) {
        if (result.startsWith('hit')) {
            console.log('Yay!');
        } else if (result.startsWith('miss')) {
            console.log('Boo');
        } else if (result.startsWith('sunk')) {
            console.log(`HA! I sunk your ${getShipName(result[-2])}`);
        } else if (result.startsWith('won')) {
            console.log(`HA! I sunk your ${getShipName(result[-2])}`);
            console.log('HOORAY!!!');
            this.gameOver = true;
        } else {
            console.log(`Unknown result: ${result}`);
        }
    }

    handlePartnerResult(result) {
        if (result.startsWith('partner hit')) {
            console.log('Darn');
        } else if (result.startsWith('partner miss')) {
            console.log('Nah nah nay');
        } else if (result.startsWith('partner sunk')) {
            console.log(`AH! You sunk my ${getShipName(result[-2])}`);
        } else if (result.startsWith('partner won')) {
            console.log(`AH! You sunk my ${getShipName(result[-2])}`);
            console.log('drats');
            this.gameOver = true;
        } else {
            console.log(`Unknown partner result: ${result}`);
        }
    }
}

async function main() {
    if (process.argv.length !== 3) {
        console.log('Provide server host as the only argument');
        return;
    }

    const host = process.argv[2];
    const name = 'Goofy';  // set this to your name
    const conn = new Connection(host);
    try {
        await conn.connect();
        const client = new BattleshipClient(conn, name);
        await client.configure();
        await client.placeShips();
        await client.waitForGo();
        while (true) {
            await client.shoot();
            if (client.gameOver) {
                break;
            }
            await client.awaitPartnerTurn();
            if (client.gameOver) {
                break;
            }
        }
    } finally {
        conn.close();
    }
}

if (require.main === module) {
    main();
}
