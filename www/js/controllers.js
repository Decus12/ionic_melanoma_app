angular.module('starter.controllers', [])

.controller('DashCtrl', function ($scope) {
})

.controller('CameraCtrl', function($scope, Camera, $rootScope, $cordovaFileTransfer) {

  $scope.getPhoto = function() {
      var imgoptions={
          quality : 100,
          saveToPhotoAlbum: false
      };
    Camera.getPicture(imgoptions).then(function(imageURI) {
      //alert(imageURI.substr(7));
        $rootScope.haa=imageURI.substr(7);

        var url = "http://192.168.1.9:4000/images";
        
        //File for Upload
        var targetPath = imageURI.substr(7);
        //alert(targetPath);
        // File name only
        var filename = targetPath.split("/").pop();
        //alert(filename);
        var options = {
             fileKey: "file",
             fileName: filename,
             chunkedMode: false,
             mimeType: "image/jpg",
         params : {'directory':'uploads', 'fileName':filename} // directory represents remote directory,  fileName represents final remote file name
         };

         $cordovaFileTransfer.upload(url, targetPath, options).then(function (result) {
             console.log("SUCCESS: " + JSON.stringify(result.response));
             //alert("Successfully Sent");
         }, function (err) {
             console.log("ERROR: " + JSON.stringify(err));
             //alert("Error while sending");
         }, function (progress) {
             // PROGRESS HANDLING GOES HERE
         });
    }, function(err) {
      console.err(err);
    });
  }
})

.controller('StatusCtrl', function($scope, imageFactory) {
    $scope.dataShown = true;
    $scope.detailsShown = false;
    $scope.$on('$ionicView.enter', function() {
    imageFactory.getImageData(dataCallback);
    function dataCallback(imageArray){
        console.log(imageArray);
    $scope.imageData = imageArray; 
        
    }
   
  });
    
    $scope.getID = function(index){
        console.log("clicked index: " + index)
        imageFactory.selected_id = $scope.imageData[index]._id; 
        
                  
  var selectedImage = imageFactory.getSelectedImage();
    
    
    $scope.id = selectedImage._id;
    $scope.picture = selectedImage.picture.path;
    console.log($scope.picture);    
    //$scope.diameter = selectedImage.diameter;
    $scope.symmetry = selectedImage.symmetry_primary;
    $scope.color = selectedImage.color_primary;
    $scope.borders = selectedImage.borders;  
    $scope.condition = selectedImage.condition;  
    
            $scope.temp = {
            
            id:$scope.id,
            picture:$scope.picture, 
            diameter:$scope.diameter,
            symmetry:$scope.symmetry,
            color:$scope.color,
            borders:$scope.borders,
            condition:$scope.condition
        }
            $scope.dataShown = false;
            $scope.detailsShown = true;

            };
    $scope.back = function(){
            $scope.dataShown = true;
            $scope.detailsShown = false;
    };
        $scope.onSwipeRight = function(){
            $scope.dataShown = true;
            $scope.detailsShown = false;
    };


})

