/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
exports.up = function(knex) {
  return knex.schema.createTableIfNotExists("IPs",(table)=>{
    table.string('id').primary()
  })
  .createTableIfNotExists("ScanData",(table)=>{
    table.increments('id').primary();
    table.string('ip');
    table.string("port");
    table.string("state");
    table.string("reason");
    table.string("name");
    table.string("product");
    table.string("version");
    table.string("extrainfo");
    table.string("conf");
    table.string("cpe");
    table.string("script");
    table.foreign("ip").references("IPs.ip");
  })
};

/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
exports.down = function(knex) {
  return knex.schema.dropTable("IPs")
                    .dropTable("ScanData")
};
