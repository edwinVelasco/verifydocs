angular
  .module('demoApp')
  .controller("DemoCtrl", DemoCtrl);

function DemoCtrl($scope) {
    $scope.start = function() {
        $scope.url = null;
        $scope.cameraRequested = true;
    }

    $scope.processURLfromQR = function (url) {
        $scope.url = url;
        $('#id_code').val(url);
        $scope.cameraRequested = false;
    }
}
