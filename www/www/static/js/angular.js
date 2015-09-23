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
// angular.module('mlApp').factory('sessionService',['$http',function($http){
// 	return{
// 		getuser : function(isjson){
// 			if(window.localStorage.getItem("user")){
// 				if(isjson){
// 					return angular.fromJson(window.localStorage.getItem("user"));
// 				}else{
// 					return window.localStorage.getItem("user");
// 				}
// 			}else{
// 				return undefined;
// 			}
// 		}
// 		,setuser : function(data){
// 			window.localStorage.setItem("user",(typeof data === 'string') ? data : angular.toJson(data));
// 		}
// 		,removeuser : function(){
// 			window.localStorage.removeItem("user");
// 		}
// 		,logout : function(){
// 			var self = this;
// 			$http({
// 				method:'POST',
// 				url:'aspreader.asp?action=logout',
// 			}).success(function(data){
// 				self.removeuser();
// 				location.href = "aspreader.asp";
// 			});
// 		}
// 		,login : function(a,p){
// 			var self = this;
// 			$http({
// 				method:'POST',
// 				url:'aspreader.asp?action=checklogin',
// 				data:{
// 					'account':a,
// 					'password':p,
// 				},
				
// 			}).success(function(data){
// 				if(parseInt(data)==0){
// 					self.setuser(a);
// 					location.href = "aspreader.asp?action=opentable&name=geo_teacher";
// 					// location.reload(true);
// 				}else{
// 					alert("密码错误")
// 				}
// 			});
// 		}
// 		,islogged : function(){
// 			!(this.getuser() == undefined)
// 		}
// 	}
// }]);
// angular.module('appreader').directive('ngEnter', function () {
//     return function (scope, element, attrs) {
//         element.bind("keydown keypress", function (event) {
//             if(event.which === 13) {
//                 scope.$apply(function (){
//                     scope.$eval(attrs.ngEnter);
//                 });

//                 event.preventDefault();
//             }
//         });
//     };
// });