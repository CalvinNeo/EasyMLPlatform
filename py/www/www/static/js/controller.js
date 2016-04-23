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

angular.module('mlApp').factory('hashimageService',['$http',function($http){
    var getimage = function(img_elem, imgname, action, args){
        $http({
            method:'POST',
            url:'/api/hash_image/',
            data:{
                imgname: imgname
                ,action: action
                ,args: args
            }
        }).success(function(data){
            img_elem.attr("src", imgname)
        });
    }
}])

angular.module('mlApp').controller('bodyController', function($scope, $http, hashimageService){
    $scope.bodystyle=navigator.platform.indexOf("Win32")!=-1?
        {'padding-top':'55px','overflow-x':'hidden','background':'#f4f4f4'}:
        {'padding-top':'0px','overflow-x':'hidden','background':'#f4f4f4'};
})

angular.module('mlApp').controller('switchDatasetController', function($scope, $http, $location, hashimageService){
    var cleanned_location = $location.path().replace('/','')
    $scope.datatype = cleanned_location ==''? 'file' : cleanned_location
    $scope.onlineForm = {}
    $scope.uploadForm = {}
    $scope.uploadactiontype = 'new'
    $scope.onlineactiontype = 'new'
    $scope.datasetviewtype = 'table' // or graphic
    // $scope.selecteddataset = -1
    // $scope.selectedoldataset = -1
    // $scope.selectedmodel = -1
    // $scope.selectwhichdatasettype = 'ds'
    $scope.dataindex = -1

    $scope.setdatatype = function(x){
        if (x == 'file'){
            $scope.datatype = 'file'
            $location.path('/file')
        }else{
            $scope.datatype = 'online'
            $location.path('/online')
        }
    }
    $scope.setdatasetviewtype = function(x){
        $scope.datasetviewtype = x;
        if(x == 'graphic'){
            if($scope.datatype=='file'){
                $.ajax({
                    url : '/api/dsimage'
                    ,data : {
                        datasetindex : $scope.dataindex 
                    }
                    ,async : true
                    ,success : function (data, textStatus) {
                        $("#datasetimage").attr("src", data)
                    }
                })
            }else{
                $.ajax({
                    url : '/api/oldsimage'
                    ,data : {
                        datasetindex : $scope.dataindex 
                    }
                    ,async : true
                    ,success : function (data, textStatus) {
                        $("#datasetimage").attr("src", data)
                    }
                })
            }
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
        $scope.dataindex = datasetindex
        // if($scope.datatype == 'file')
        //     reurl = '/api/dsimage'
        // else
        //     reurl = '/api/oldsimage'
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
    $scope.updateDataset = function(datasetindex){
        $scope.setuploadactiontype('change')
        $.ajax({
            url : '/api/dataset_view?datasetindex='+ datasetindex
            ,async : false
            ,success : function (data, textStatus) {
                data = data.replace(/True/g, "true")
                data = data.replace(/False/g, "false")
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
        $scope.dataindex = datasetindex
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
    $scope.updateOLDataset = function(datasetindex){
        $scope.setonlineactiontype('change')
        $.ajax({
            url : '/api/oldataset_view?datasetindex='+ datasetindex
            ,async : false
            ,success : function (data, textStatus) {
                // data = jQuery.parseJSON(data)
                data = data.replace(/True/g, "true")
                data = data.replace(/False/g, "false")
                // data = data.replace(/True/, "true").replace(/False/, "false")
                data = eval( "(" + data + ")" )
                $scope.onlineForm['olname'] = data.info.name
                $scope.onlineForm['olurl'] = data.info.url
                $scope.onlineForm['ollocation'] = data.info.location
                $scope.onlineForm['olsearch'] = data.info.search
                $scope.onlineForm['olrenew'] = data.info.renewstrategy
                $scope.onlineForm['olhashead'] = data.info.hashead
                $scope.onlineForm['olhead'] = data.info.head
            }
        })
    }
    $scope.ondatasetselected = function(datasetindex){

    }
    $scope.onoldatasetselected = function(datasetindex){
        
    }
})

angular.module('mlApp').controller('newModelController', function($scope, $http, $location, hashimageService){
    $scope.actiontype = 'new'
    $scope.modelForm = {}
    $scope.datatype = 'file'
    $scope.showwhich = 'list'
    $scope.selecteddataset = -1
    $scope.selectedoldataset = -1
    $scope.selectedmodel = -1
    $scope.selectwhichdatasettype = 'ds'
    $scope.currenthead = []

    $scope.setdatatype = function(x){
        if (x == 'file'){
            $scope.datatype = 'file'
            $scope.selectwhichdatasettype = 'ds'
        }else{
            $scope.datatype = 'online'
            $scope.selectwhichdatasettype = 'ol'
        }
    }
    $scope.uploadFormShow = function(){
        return $scope.datatype == "file"
    }
    $scope.onlineShow = function(){
        return !$scope.uploadFormShow()
    }
    $scope.setshowwhich = function(x){
        if (x == 'list'){
            $scope.showwhich = 'list'
        }else{
            $scope.showwhich = 'new'
        }
    }
    $scope.newModelShow = function(){
        return !$scope.listShow()
    }
    $scope.listShow = function(){
        return $scope.showwhich == 'list'
    }
    $scope.setactiontype = function(x){
        if (x == 'new'){
            $scope.modelForm = {}
            $scope.selecteddataset = -1
            $scope.selectedoldataset = -1
            $scope.selectedmodel = -1
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
        $.ajax({
            url : '/api/model_delete?modelindex='+modelindex
            ,async : false
            ,success : function (data, textStatus) {
                location.reload(true)
                }
            })
    }
    $scope.trainModel = function(modelindex){
        $.ajax({
            url : '/api/model_train?modelindex='+ modelindex
            ,async : true
            ,success : function (data, textStatus) {
                location.reload(true)
            }
        })
    }
    $scope.abortTrain = function(taskindex){
        $.ajax({
            url : '/api/task_delete?taskindex=' + taskindex
            ,async : true
            ,success : function(data, testStatus){
                location.reload(true)
            }
        })
    }
    $scope.ondatasetselected = function(datasetindex){
        $scope.gethead();
    }
    $scope.onoldatasetselected = function(datasetindex){
        $scope.gethead();
    }
    $scope.gethead = function(){
        if (($scope.selecteddataset==-1 && $scope.selectwhichdatasettype=='ds') || ($scope.selectedoldataset==-1 && $scope.selectwhichdatasettype!='ds')){
            return []
        }
        req_url = $scope.selectwhichdatasettype == 'ds'? '/api/dataset_view?datasetindex=' + $scope.selecteddataset : '/api/oldataset_view?datasetindex=' + $scope.selectedoldataset
        $.ajax({
            url : req_url
            ,async : false
            ,success : function (data, textStatus) {
                data = data.replace(/True/g, "true")
                data = data.replace(/False/g, "false")
                data = eval( "(" + data + ")" )
                $scope.currenthead = data.view.head
            }
        })
    }
})

angular.module('mlApp').controller('applyModelController', function($scope, $http, $location, hashimageService){
    $scope.actiontype = 'new'
    $scope.applyForm = {}
    $scope.datatype = 'file'
    $scope.showwhich = 'list'
    $scope.selecteddataset = -1
    $scope.selectedoldataset = -1
    $scope.selectedmodel = -1
    $scope.selectwhichdatasettype = 'ds'
    $scope.currentshow = 'ds'

    $scope.runapply = function(){
        $.ajax({
            url : '/api/model_apply'
            ,data : {
                modelindex : $scope.selectedmodel
                ,datasetindex : $scope.selecteddataset
                ,oldatasetindex : $scope.selectedoldataset
                ,selectwhichdatasettype : $scope.selectwhichdatasettype
                ,removeitem : $scope.applyForm.removeitem
            }
            ,async : true
            ,success : function (data, textStatus) {
                document.getElementById('datasetviewframe').contentWindow.document.body.innerHTML = data
                $("#modelimage").hide()
            }
        })
    }

    // below are copied from switchDatasetController
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
        $scope.currentshow = 'ds'
        $("#modelimage").hide()
        $("#datasetviewframe").show()
        $("#datasetviewframe").attr("src","/index/ds_view?datasetindex="+datasetindex)
    }

    $scope.showOLDataset = function(datasetindex){
        $scope.currentshow = 'ds'
        $("#modelimage").hide()
        $("#datasetviewframe").show()
        $("#datasetviewframe").attr("src","/index/olds_view?datasetindex="+datasetindex)
    }

    $scope.showModel = function(modelindex){
        $scope.currentshow = 'md'
        $("#datasetviewframe").hide()
        $("#modelimage").show()
        $.ajax({
            url : '/api/mdimage'
            ,data : {
                modelindex : modelindex
            }
            ,async : true
            ,success : function (data, textStatus) {
                $("#modelimage").attr("src", data)
            }
        })
    }

    $scope.ondatasetselected = function(datasetindex){

    }
    $scope.onoldatasetselected = function(datasetindex){
        
    }
})

angular.module('mlApp').controller('assessModelController', function($scope, $http, $location, hashimageService){
    $scope.actiontype = 'new'
    $scope.assessForm = {}
    $scope.datatype = 'file'
    $scope.showwhich = 'list'
    $scope.selecteddataset = -1
    $scope.selectedoldataset = -1
    $scope.selectedmodel = -1
    $scope.selectwhichdatasettype = 'ds'
    $scope.currentshow = 'ds'
    $scope.classfeatureindex = -1
    $scope.ans = [] //[{'name':xxx, 'value':yyy}, {...}]
    $scope.safeApply = function(fn) {
        var phase = this.$root.$$phase;
        if(phase == '$apply' || phase == '$digest') {
            if(fn && (typeof(fn) === 'function')) {
              fn();
            }
        } else {
           this.$apply(fn);
        }
    };
    // $scope.runassess = function(){
    //     $.ajax({
    //         url : '/api/model_assess'
    //         ,data : {
    //             modelindex : $scope.selectedmodel
    //             ,datasetindex : $scope.selecteddataset
    //             ,oldatasetindex : $scope.selectedoldataset
    //             ,selectwhichdatasettype : $scope.selectwhichdatasettype
    //             ,classfeatureindex : $scope.assessForm.classfeatureindex
    //             ,assessmethod : $scope.assessForm.assessmethod
    //         }
    //         ,async : true
    //         ,success : function (data, textStatus) {
    //             $scope.safeApply(function(){
    //                 $scope.ans = data
    //             })
    //         }
    //     })
    // }
    $scope.runassess = function(){
        $http({
            url: '/api/model_assess',
            params: {
                modelindex : $scope.selectedmodel
                ,datasetindex : $scope.selecteddataset
                ,oldatasetindex : $scope.selectedoldataset
                ,selectwhichdatasettype : $scope.selectwhichdatasettype
                ,classfeatureindex : $scope.assessForm.classfeatureindex
                ,assessmethod : $scope.assessForm.assessmethod
            }
        }).success(function(response, status, headers, config){
          $scope.ans = response
        });
    }

    // below are copied from switchDatasetController
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

})
