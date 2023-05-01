const express = require('express'),
    router = express.Router(),
    fs = require("fs"),
    path = require("path"),
    scandata = require("../models/scandata")

/* GET home page. */
router.get('/', async (req, res) => {
  const a = await scandata.query()
  const b = a.map(i=>{
    if(i.script!=='') {
      let s = fs.readFileSync(path.join(__dirname,"../../../data/scripts/"+i.script),'utf-8');
      i.script = JSON.parse(s)
    }
    return i
  })

  const c = b.reduce((ac,ob)=>{
    const key = ob.ip;
    if(!ac[key]) {
      ac[key] = []
    }
    ac[key].push(ob);
    return ac;
  },{})
  res.json(c)
});

module.exports = router;
