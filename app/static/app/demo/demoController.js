angular
  .module('demoApp')
  .controller("DemoCtrl", DemoCtrl);

function DemoCtrl($scope) {
    $scope.start = function() {
        $scope.url = null;
        $scope.cameraRequested = true;
    }

    $scope.processURLfromQR = function (url) {

        $scope.url = url.replaceAll("'", '"');
        $scope.document = JSON.parse($scope.url);
        console.log($scope.document);
        $('#id_code').val($scope.document.token);
        console.log($scope.url);
        $scope.cameraRequested = false;
    }
}
