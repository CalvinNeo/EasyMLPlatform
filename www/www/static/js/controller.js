function bodyController($scope, $http){
	$scope.bodystyle=navigator.platform.indexOf("Win32")!=-1?
		{'padding-top':'55px','overflow-x':'hidden','background':'#f4f4f4'}:
		{'padding-top':'0px','overflow-x':'hidden','background':'#f4f4f4'};
}