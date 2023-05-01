const { Model } = require("./init");


class IPs extends Model {
    static get tableName() {
        return "IPs"
    }
}

module.exports = IPs;