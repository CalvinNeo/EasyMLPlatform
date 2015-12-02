var app = angular.module('mlApp',[],
	['$httpProvider', function ($httpProvider) {
		// Use x-www-form-urlencoded Content-Type
		$httpProvider.defaults.headers
			.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';

		// tell the server it is ajax, otherwise Codeignitor won't say it is ajax
		// common set for all angular ajax requests
		$httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';

		// Override $http service's default transformRequest
		$httpProvider.defaults.transformRequest = [function (data) {
			var param = function (obj) {
				var query = '';
				var name, value, fullSubName, subName, subValue, innerObj, i;

				for (name in obj) {
					value = obj[name];

					if (value instanceof Array) {
						for (i = 0; i < value.length; ++i) {
							subValue = value[i];
							fullSubName = name + '[' + i + ']';
							innerObj = {};
							innerObj[fullSubName] = subValue;
							query += param(innerObj) + '&';
						}
					}
					else if (value instanceof Object) {
						for (subName in value) {
							subValue = value[subName];
							fullSubName = name + '[' + subName + ']';
							innerObj = {};
							innerObj[fullSubName] = subValue;
							query += param(innerObj) + '&';
						}
					}
					else if (value !== undefined && value !== null) {
						query += encodeURIComponent(name) + '=' + encodeURIComponent(value) + '&';
					}
				}

				return query.length ? query.substr(0, query.length - 1) : query;
			};

			return angular.isObject(data) && String(data) !== '[object File]' ? param(data) : data;
		}];
	}]
);

function bodyController($scope, $http){
	$scope.bodystyle=navigator.platform.indexOf("Win32")!=-1?
		{'padding-top':'55px','overflow-x':'hidden','background':'#f4f4f4'}:
		{'padding-top':'0px','overflow-x':'hidden','background':'#f4f4f4'};
}
function switchDatasetController($scope, $http, $location){
	var cleanned_location = $location.path().replace('/','')
	$scope.datatype = cleanned_location ==''? 'file' : cleanned_location
	$scope.setdatatype = function(x){
		if (x == 'file'){
			$scope.datatype = 'file'
			$location.path('/file')
		}else{
			$scope.datatype = 'online'
			$location.path('/online')
		}
	}
	$scope.actiontype = 'new'
	$scope.setactiontype = function(x){
		if (x == 'new'){
			$scope.datatype = 'new'
		}else{
			$scope.datatype = 'change'
		}
	}
	$scope.uploadFormShow = function(){
		return $scope.datatype == "file"
	}
	$scope.onlineShow = function(){
		return !$scope.uploadFormShow()
	}
	$scope.onlineForm = {}
	$scope.uploadForm = {}
}
function newModelController($scope, $http){
	$scope.actiontype = 'new'
	$scope.submitbutton = 'Create New Model'
	$scope.modelForm = {}
	$scope.setactiontype = function(x){
		if (x == 'new'){
			$scope.actiontype = 'new'
			$scope.submitbutton = 'Create New Model'
		}else{
			$scope.actiontype = 'change'
			$scope.submitbutton = 'Modify This Model'
		}
	}
	$scope.updateModel = function(modelindex){
		$scope.setactiontype('change')
		$.ajax({
			url : '/api/model_view?modelindex='+ modelindex
			,async : true
			,success : function (data, textStatus) {
				$scope.modelForm['name'] = data['name']
			}
		})
	}
}