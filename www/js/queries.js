var db = require('./database');

//Query to save a new image to database
exports.saveNewImage = function (req, res,results) {
    //console.log(req.body);
    var imageTemp = new db.images();
    
    imageTemp.picture = req.file;
    imageTemp.date = new Date ();
    imageTemp.condition = 0;
    
    imageTemp.symmetry_primary = parseInt(results[0]);
    imageTemp.symmetry_secondary = parseInt(results[1]);
    imageTemp.color_primary= parseInt(results[2]);
    imageTemp.color_secondary= parseInt(results[3]);
    imageTemp.borders = parseInt(results[4]);
    
    console.log (imageTemp);

    imageTemp.save(function (err) {

                          if (err) {
                              res.status(500);
                          } else {
                              res.status(200);
                          }
                      });

};

//Query to get all images from database
exports.loadAllImages = function(req,res){
     
    db.images.find(function(err,data){
         
        if(err){
            console.log(err.message);
            res.send("Error");
        }
        else{
             console.log(data)
            res.send(data);
            
        }
    });
};