const Model = require("./init");

class ScanData extends Model {
    static get tableName() {
        return "ScanData"
    }
}

module.exports = ScanData;