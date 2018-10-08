'use strict';
const express = require('express');
const path = require('path');
const fs = require('fs');
const app = express();
const api = require('./api/index.js');
const cors = require('cors');
app.get("/crab", (req, res) => {
    res.send("fdasfdsa dsa ");
});
app.use("/api", cors(), (req, res) => {
    api.projectsGET().then((x) => {
        res.json(x);
    });
});
// Use the built-in express middleware for serving static files from './www'
app.use("/", (req, res) => {
    const p = path.join(__dirname, path.join("/www", req.path));
    console.log(p);
    fs.lstat(p, (err, stats) => {
        if (err !== null) {
            res.status(404);
            res.send();
        }
        else {
            if (stats.isDirectory()) {
                res.sendFile(path.join(p, 'index.html'));
            }
            else if (stats.isFile()) {
                res.sendFile(p);
            }
        }
    });
});
// Start the server
const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
    console.log(`App listening on port ${PORT}`);
    console.log('Press Ctrl+C to quit.');
});
//# sourceMappingURL=app.js.map