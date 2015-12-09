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
	$scope.uploadFormShow = function(){
		return $scope.datatype == "file"
	}
	$scope.onlineShow = function(){
		return !$scope.uploadFormShow()
	}
	$scope.setactiontype = function(x){
		if (x == 'new'){
			$scope.datatype = 'new'
		}else{
			$scope.datatype = 'change'
		}
	}
	$scope.onlineForm = {}//{'olname':'', 'olhashead': false, 'olurl': '', 'ollocation':'', 'olsearch':'', 'olrenew':'', 'olhead':''}
	$scope.uploadForm = {}//{'dsname':'', 'dshashead': false, 'dsattr_delim': '', 'dsrecord_delim':'', 'dshead':''}
	$scope.uploadactiontype = 'new'
	$scope.onlineactiontype = 'new'
	$scope.setuploadactiontype = function(x){
		if (x == 'new'){
			$scope.uploadactiontype = 'new'
		}else{
			$scope.uploadactiontype = 'change'
		}
	}
	$scope.setonlineactiontype = function(x){
		if (x == 'new'){
			$scope.onlineactiontype = 'new'
		}else{
			$scope.onlineactiontype = 'change'
		}
	}

	$scope.showDataset = function(datasetindex){
		$scope.updateDataset(datasetindex)
		$("#datasetviewframe").attr("src","/index/ds_view?datasetindex="+datasetindex)
	}
	$scope.downloadDataset = function(datasetindex){

	}
	$scope.deleteDataset = function(datasetindex){
		$.ajax({
			url : '/api/dataset_delete?datasetindex='+datasetindex
			,async : false
			,success : function (data, textStatus) {
				location.reload(true)
				}
			})
	}
	$scope.trainDataset = function(datasetindex){
		
	}
	$scope.updateDataset = function(datasetindex){
		$scope.setuploadactiontype('change')
		$.ajax({
			url : '/api/dataset_view?datasetindex='+ datasetindex
			,async : false
			,success : function (data, textStatus) {
				ndata = eval( "(" + data + ")" )
				$scope.uploadForm['dsname'] = ndata.info.name
				$scope.uploadForm['dshashead'] = ndata.info.hashead
				$scope.uploadForm['dsattr_delim'] = ndata.info.attr_delim
				$scope.uploadForm['dsrecord_delim'] = ndata.info.record_delim
				$scope.uploadForm['dshead'] = ndata.info.head
			}
		})
	}

	$scope.showOLDataset = function(datasetindex){
		$scope.updateOLDataset(datasetindex)
		$("#datasetviewframe").attr("src","/index/olds_view?datasetindex="+datasetindex)
	}
	$scope.deleteOLDataset = function(datasetindex){
		$.ajax({
			url : '/api/oldataset_delete?datasetindex='+datasetindex
			,async : false
			,success : function (data, textStatus) {
				location.reload(true)
				}
			})
	}
	$scope.dumpOLDataset = function(datasetindex){
		$.ajax({
			url : '/api/onlinedataset_dump?datasetindex='+datasetindex
			,async : false
			,success : function (data, textStatus) {
				location.reload(true)
				}
			})
	}
	$scope.trainOLDataset = function(datasetindex){
		
	}
	$scope.updateOLDataset = function(datasetindex){
		$scope.setonlineactiontype('change')
		$.ajax({
			url : '/api/oldataset_view?datasetindex='+ datasetindex
			,async : false
			,success : function (data, textStatus) {
				// data = jQuery.parseJSON(data)
				data = eval( "(" + data + ")" )
				$scope.onlineForm['olname'] = data.info.name
				$scope.onlineForm['olurl'] = data.info.url
				$scope.onlineForm['ollocation'] = data.info.location
				$scope.onlineForm['olsearch'] = data.info.search
				$scope.onlineForm['olrenew'] = data.info.renewstrategy
				$scope.onlineForm['olhashead'] = data.info.hashead
				$scope.onlineForm['olhead'] = data.info.head

				// $("#olname").val(data.info.name)
				// $("#olurl").val(data.info.url)
				// $("#ollocation").val(data.info.location)
				// $("#olsearch").val(data.info.search)
				// $("#olrenew").val(data.info.renewstrategy)
				// $("#olhashead").val(data.info.hashead)
				// $("#olnolheadame").val(data.info.head)

			}
		})
	}
}

function newModelController($scope, $http){
	$scope.actiontype = 'new'
	$scope.modelForm = {}
	$scope.datatype = 'file'
	$scope.setdatatype = function(x){
		if (x == 'file'){
			$scope.datatype = 'file'
		}else{
			$scope.datatype = 'online'
		}
	}
	$scope.uploadFormShow = function(){
		return $scope.datatype == "file"
	}
	$scope.onlineShow = function(){
		return !$scope.uploadFormShow()
	}
	$scope.setactiontype = function(x){
		if (x == 'new'){
			$scope.modelForm = {}
			$scope.actiontype = 'new'
		}else{
			$scope.actiontype = 'change'
		}
	}
	$scope.updateModel = function(modelindex){
		$scope.setactiontype('change')
		$.ajax({
			url : '/api/model_view?modelindex='+ modelindex
			,async : false
			,success : function (data, textStatus) {
				// data = jQuery.parseJSON(data)
				data = eval( "(" + data + ")" )
				$scope.modelForm['name'] = data.name
				$scope.modelForm['modeltype'] = data.modeltype
			}
		})
	}
	$scope.showModel = function(modelindex){
		$scope.updateModel(modelindex)
		$("#modelviewframe").attr("src","/index/md_view?modelindex="+modelindex)
	}
	$scope.downloadModel = function(modelindex){
		
	}
	$scope.deleteModel = function(modelindex){

	}

}