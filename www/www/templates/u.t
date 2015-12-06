<form method='post' enctype="multipart/form-data" autocomplete=off action="{% url 'index' 'onlinedataset_upload' %}" style="width:100%;" id="onlineFrom" >
	{% csrf_token %}
	<div class="container-fluid npnm" >
		<div class="col-md-6 npnm" >
			<p><label for="name">Name Your Online Dataset</label>
				<input type="text" name="name" class="form-control" ng-model="onlineFrom.olname" ng-minlength=1 ng-maxlength=20 required id=" olname">
				<div class="error" ng-show="onlineFrom.olname.$dirty && onlineFrom.olname.$invalid">
					<small class="error text-danger" ng-show="onlineFrom.olname.$error.required"> Name Required </small>
				</div>
			</p>
		</div>
		<div class="col-md-6 npnm" >
			<p><label for="url">URL</label>
				<input name="url" type="text" class="form-control" ng-pattern="/^((http|https)://)?([\w-]+\.)+[\w-:]+(/[\w- ./?%&=_]*)?$/" required ng-model="onlineFrom.olurl" id=" olurl">
				<div class="error" ng-show="onlineFrom.olurl.$dirty && onlineFrom.olurl.$invalid">
					<small class="error text-danger" ng-show="onlineFrom.olurl.$error.required"> URL Required </small>
				</div>
			</p>
		</div>
	</div>
	<div class="container-fluid npnm" >
		<div class="col-md-6 npnm" >
			<label for="location">Table Location (CSS Selector)</label>
			<input name="location" type="text" class="form-control" ng-model="onlineFrom.ollocation" id="ollocation ">
		</div>
		<div class="col-md-6 npnm" >
			<label for="search">Read</label>
			<input name="search" type="text" class="form-control" ng-model="onlineFrom.olsearch" id="olsearch ">
		</div>
	</div>
	<div class="container-fluid npnm" >
		<div class="col-md-6 npnm" >
			<label for="renew">Renew Strategy</label>
			<input name="renew" type="text" class="form-control" ng-model="onlineFrom.olrenew" id=" olrenew">
		</div>
	</div>
	<div class="container-fluid npnm" >
		<div class="col-md-4 npnm" >
			<label for="hashead">Dataset Header</label>
			<p><input name="hashead" type="checkbox" ng-model="onlineFrom.olhashead" id=" olhashead">Has Head</input></p>
		</div>
		<div class="col-md-8 npnm" >
			<label for="head">Specified Types</label>
			<input name="head" type="text" class="form-control" ng-model="onlineFrom.olhead" id=" olhead"></input>
		</div>
	</div>
	<hr/>
	<div class="container-fluid npnm" >
		<div class="col-md-6 npnm" >
			<input type="submit" class="btn btn-success btn-block" value="{% templatetag openvariable %} {true:'Create Online Dataset', false:'Modify Online Dataset'}[onlineactiontype=='new'] {% templatetag closevariable %}">
		</div>
		<div class="col-md-6 npnm" >
			<input type="button" class="btn btn-info btn-block" value="Reset" ng-click="setonlineactiontype('new')">
		</div>
	</div>
</form>
<script>
$("#olrenew").typeahead({
    source: [{% for strategy in renewstrategies %}'{{strategy}}',{% endfor%}],//数据源
    items: 8,//最多显示个数
    updater: function (item) {
        return item;//这里一定要return，否则选中不显示，外加调用display的时候null reference错误。
    },
    displayText: function (item) {
        return item;//返回字符串
    },
    afterSelect: function (item) {
        //选择项之后的事件 ，item是当前选中的。
        return item;
    },
    delay: 500//延迟时间
});
</script>