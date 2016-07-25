var express = require("express");
var multer = require('multer');
var upload = multer({ dest: './uploads/' });
var path = require("path");
var database = require('./js/database');
var query = require('./js/queries');
var PythonShell = require('python-shell');

var app = express();

var storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, './uploads/')
  },
  filename: function (req, file, cb) {
    cb(null, Date.now()+'.jpg')
  }
})
 
var upload = multer({ storage: storage })
app.set('port', 4000)
//=====================Middlewares========================


app.use('/', express.static(path.join(__dirname, '../templates')));

app.use('/js', express.static(path.join(__dirname, '../js')));
app.use('/css', express.static(path.join(__dirname, '../css')));
app.use('/img', express.static(path.join(__dirname, '../img')));


//=====================ROUTERS============================
app.post('/images', upload.single('file'), function (req, res) {
    //console.log("files " + req.files);
    console.log("file " + req.file.filename);
    //var image = req.files;

    var options = {
    mode: 'text',
    scriptPath: 'python',  
    args: ['--image', 'uploads/' + req.file.filename]
    };

    PythonShell.run('analyze.py', options, function (err, results) {
        if (err) {
            res.status(500);
            console.log('error')
        } 
        else {
            if (results == null){
                res.status(422);
                console.log('null results')
                }
            else {
        // results is an array consisting of messages collected during execution
        console.log('results:', results);
            query.saveNewImage(req, res, results);
            res.status(200);
            console.log('sent')
                }
        }
    });
    

    });

app.get('/images', function (req, res){
    
   query.loadAllImages(req, res);
    //console.log(req.body);
    //res.status(200);
    
});
app.listen(4000);