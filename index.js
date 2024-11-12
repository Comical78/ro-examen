const express = require('express');
const mustache = require('mustache');
const fs = require('fs');
const path = require('path');
const app = express();
const PORT = process.env.PORT || 3000;
app.use('/assets/', express.static(path.join(__dirname, 'assets')));
app.get("/", (req, res) => {
    const index = path.join(__dirname, 'pages', 'evaloare.html');
    fs.readFile(index, 'utf8', (err, data) => {
        if (err) {
            console.error(err);
            res.status(500).send('A apărut o eroare la citirea fișierului HTML.');
        } else {
            res.status(200).send(data);
        }
    });
});
app.use((req, res) => {
    const index = path.join(__dirname, 'pages', '404.html');
    fs.readFile(index, 'utf8', (err, data) => {
        if (err) {
            console.error(err);
            res.status(404).send('404 Not Found');
        } else {
            const rendered = mustache.render(data, { location: req.originalUrl });
            res.status(404).send(rendered);
        }
    });
});
module.exports = app;
