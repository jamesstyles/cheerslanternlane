  angular.module('subscriptionForm', [])
    .controller('subscriptionController', ['$scope', function($scope) {

      $scope.updateSubscription = function(user) {
		$scope.user.email = "";

		$scope.user.email = document.getElementById('email').value;		
		
		console.log(JSON.stringify(user));  
		messageToSQS(JSON.stringify(user));
		
		//disable the form button after click and re-initialise intent
		$scope.user.email = "";
		}; 
    }]);

	function getEmail(){
	var hashParams = window.location.hash.substr(1).split('&'); // substr(1) to remove the `#`
	for(var i = 0; i < hashParams.length; i++){
    var p = hashParams[i].split('=');
    document.getElementById(p[0]).value = decodeURIComponent(p[1]);;
    }}