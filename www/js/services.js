angular.module('starter.services', [])


.factory('Camera', ['$q', function($q) {

  return {
    getPicture: function(options) {
      var q = $q.defer();

      navigator.camera.getPicture(function(result) {
        // Do any magic you need
        q.resolve(result);
          //console.log('jgnjfg');
          
      }, function(err) {
        q.reject(err);
      }, options);

      return q.promise;
    }
  }
}])

.factory('imageFactory', function ( $http, ApiEndpoint) {
    console.log('ApiEndpoint', ApiEndpoint)

    var factory = {};
    factory.imageArray = [];

    
    factory.getImageData = function(callbackFunc){
        
            //console.log('gg');
            
             //ON browser: 
            //$http.get('/images').then(function(data){
            $http.get('http://192.168.1.9:4000/images').then(function(data){
                console.log(JSON.stringify(data));
              factory.imageArray = data.data;
              callbackFunc(factory.imageArray);    
                
            },function(error){
                console.log(JSON.stringify(error));
                
                factory.imageArray = [];
                callbackFunc(factory.imageArray);
            });
    }
    
    factory.getSelectedImage = function(){

    for(var i = 0; i < factory.imageArray.length; i++){

        if(factory.imageArray[i]._id === factory.selected_id){

            return factory.imageArray[i];
        }
    }
        
    }
    
    return factory;

})