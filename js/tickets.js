  angular.module('ticketsForm', [])
    .controller('ticketsController', ['$scope', function($scope) {

      $scope.update = function(user) {
		
		//initialise auto-filled variables
		$scope.user.address = "";
		$scope.user.postcode = "";

		//set autofilled variables from form
		$scope.user.address = document.getElementById('autocomplete').value;
		$scope.user.postcode = document.getElementById('postal_code').value;

		//log output and call SQS
		console.log(JSON.stringify(user));  
		messageToSQS(JSON.stringify(user));

		//disable the form button after click and re-initialise intent
		$scope.user.email = "";
		$scope.user.name = "";
		$scope.user.phone = "";
		$scope.user.tickets = "";
		$scope.user.address = "";
		document.getElementById('autocomplete').value = null;
		document.getElementById('postal_code').value = null;
		}; 
    }]);

