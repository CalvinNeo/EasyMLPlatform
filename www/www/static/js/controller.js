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
function uploadDatasetController($scope, $http){

}