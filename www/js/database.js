
var mongoose = require("mongoose");

mongoose.connect('mongodb://localhost:27017/melanoma', connectionStatus);

/**
  *Connection callback for fail and ok cases
  */
function connectionStatus(err, ok) {

    if (err) {

        console.log(err.message);
    } else {

        console.log("Melanoma database connected");
    }
}
var Schema = mongoose.Schema;

var imageSchema = new Schema({
    picture: { type:Object },
    date: Date,
    condition: Number,
    symmetry_primary: Number,
    symmetry_secondary: Number,
    color_primary: Number,
    color_secondary: Number,
    borders: Number
});
var images = mongoose.model('images', imageSchema);

//exports to expose the data to other modules
exports.images = images;