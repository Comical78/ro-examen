const express = require('express');
require('dotenv').config();
const fs = require('fs');
const path = require('path');
const app = express();
const PORT = process.env.PORT || 3000;
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'pages'));
app.use('/assets/', express.static(path.join(__dirname, 'assets')));
app.use("/evalori/en-2025-01/", (req, res) => {
    res.render('evaloare-en-2025-01');
});
app.use("/", (req, res) => {
    res.render('index');
});
app.use((req, res) => {
    res.render('404', { location: req.originalUrl });
});
module.exports = app;