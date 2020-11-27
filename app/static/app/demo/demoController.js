angular
  .module('demoApp')
  .controller("DemoCtrl", DemoCtrl);

function DemoCtrl($scope) {
    $scope.url = null;

    $scope.start = function() {
        $scope.url = null;
        $scope.cameraRequested = true;
    }

    $scope.processURLfromQR = function (url) {

        //$scope.url = url.replaceAll("'", '"');
        $scope.url = url;

        //$scope.document = JSON.parse($scope.url);
        console.log($scope.url);
        $('#id_code').val($scope.url);
        $scope.cameraRequested = false;
    }
}
