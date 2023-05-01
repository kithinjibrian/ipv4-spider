/*
 *initialize objection
 *Take knex
 **/
 
 // fetch modules
 const config=require("../knexfile"),
        knex=require("knex")(config["development"]),
        {Model}=require("objection");

//  objection model takes knex instance
Model.knex(knex);

//  Export objection model
module.exports = Model;