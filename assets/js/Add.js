draw_add = function(){
	$("body").html(
		//'<div id="dropdown" onclick="$(\'#dropdown\').hide(\'fade\');updateCell()""><div class="content" onclick="event.stopPropagation();"></div></div>'+
		'<div><h3>Add Users/Project#s</h3>'+
                '<button class="add" onclick="draw()">Search</button></div>'+
		'<div class="title"><h1>ADD</h1></div>'+
		'<div class="loglink"><i class="fa fa-spinner fa-spin check-logs-spinner"></i><a href="./assets/admin/log/">Check Logs</a></div>'+
                '<div class="tab">'+
                        '<button class="tablinks" onclick="openTab(event, \'users\')" id="defaultOpen">Users</button>'+
                        '<button class="tablinks" onclick="openTab(event, \'projects\')">Projects</button>'+
                '</div>'+
                '<div id="users" class="tabcontent">'+
                        '<h3>Users</h3>'+
                        '<p>Add values into fields</p>'+
		'<table>'+
			'<tr>'+
			'<th>'+
                                '<label class="button" name="usrID">User ID</label>'+
                        '</th>'+
                        '<th>'+
                                '<label class="button" name="date_Added">Date Added</label>'+
                        '</th>'+
                        '<th>'+
                                '<label class="button" name="status">Status</label>'+
                        '</th>'+
                        '<th>'+
                                '<label class="button" name="expiration">Expiration</label>'+
                        '</th>'+
                        '<th>'+
                                '<label class="button" name="name">Users\' Name</label>'+
                        '</th>'+
                        '<th>'+
                                '<label class="button" name="organization">Organization</label>'+
                        '</th>'+
                        '<th>'+
                                '<label class="button" name="email">Email</label>'+
                        '</th>'+
                        '<th>'+
                                '<label class="button" name="phone">Phone#</label>'+
                        '</th>'+
                        '<th>'+
                                '<label class="button" name="datasets">Valid Datasets</label>'+
                        '</th>'+
			'</tr>'+
			'<tr>'+
			'<td>'+
                                '<div class="search-container" id="usrID">'+
                                        '<input id="search_bar_Add" type="text" class="form-control" placeholder="User ID" name="usrID">'+
                                '</div>'+
                        '</td>'+
                        '<td>'+
                                '<div class="search-container" id="date_Added">'+
                                        '<label id="format">Format: YYYY-MM-DD</label>'+
                                        '<label id="exact"><input type="radio" name="group" onclick="showRange(\'to\',\'search_bar25\',\'none\')" checked value="EXACT">Exact</label>'+
                                        '<label id="range"><input type="radio" name="group" onclick="showRange(\'to\',\'search_bar25\',\'block\')" value="RANGE">Range</label>'+
                                        '<input id="search_bar2" type="text" class="form-control" placeholder="Date Added" name="date_Added">'+
                                        '<label id="to" style="display:none"> To</label>'+
                                        '<input id="search_bar25" type="text" class="form-control" placeholder="Date Added" style="display:none" name="date_Added">'+
                                '</div>'+
                        '</td>'+
                        '<td>'+
                                '<div class="search-container" id="status">'+
                                        '<label id="checkbox_enable">'+
                                        '<input type="radio" name="stat" value="ENABLE" checked>Enabled</label>'+
                                        '<label id="checkbox_disable">'+
                                        '<input type="radio" name="stat" value="DISABLE">Disabled</label>'+
                                '</div>'+
                        '</td>'+
                        '<td>'+
                                '<div class="search-container" id="expiration">'+
                                        '<label id="format2">Format: YYYY-MM-DD</label>'+
                                        '<label id="exact2"><input type="radio" name="group2" onclick="showRange(\'to2\',\'search_bar45\',\'none\')" checked value="EXACT">Exact</label>'+
                                        '<label id="range2"><input type="radio" name="group2" onclick="showRange(\'to2\',\'search_bar45\',\'block\')" value="RANGE">Range</label>'+
                                        '<input id="search_bar4" type="text" class="form-control" placeholder="Expiration" name="expiration">'+
                                        '<label id="to2" style="display:none"> To</label>'+
                                        '<input id="search_bar45" type="text" class="form-control" placeholder="Expiration" style="display:none" name="expiration">'+
                                '</div>'+
                        '</td>'+
                        '<td>'+
                                '<div class="search-container" id="name">'+
                                        '<input id="search_bar_Add" type="text" class="form-control" placeholder="Users\' Name" name="name">'+
                                '</div>'+
                        '</td>'+
                        '<td>'+
                                '<div class="search-container" id="organization">'+
                                        '<input id="search_bar_Add" type="text" class="form-control" placeholder="Oragnization" name="organization">'+
                                '</div>'+
                        '</td>'+
                        '<td>'+
                                '<div class="search-container" id="email">'+
                                        '<input id="search_bar_Add" type="text" class="form-control" placeholder="Email" name="email">'+
                                '</div>'+
                        '</td>'+
                        '<td>'+
                                '<div class="search-container" id="phone">'+
                                        '<input id="search_bar_Add" type="text" class="form-control" placeholder="Phone" name="phone">'+
                                '</div>'+
                        '</td>'+
                        '<td>'+
                                '<div class="search-container" id="datasets">'+
					'<label id="default">*Default Dataset is ALL</label>'+
					//'<button onclick="$(\'#dropdown\').show(\'fade\');setContent(this.parentElement)">Edit</button> ALL'+
                                        '<input id="search_bar_Add" type="text" class="form-control" placeholder="Datasets" name="datasets">'+
                                '</div>'+
                        '</td>'+
			'</tr>'+
		'</table>'+
		'<div id="enter0">'+
                        '<button class="enter_Add" onclick="addParams(\'users\')">Go</button>'+
                '</div>'+
		'<table id="mytableAddU">'+
                '</table>'+	
		'</div>'+
		'<div id="projects" class="tabcontent">'+
                        '<h3>Projects</h3>'+
                        '<p>Add values into fields</p>'+
		'<table>'+
			'<tr>'+
			'<th>'+
                                '<label class="button" name="projID">Project Number</label>'+
                        '</th>'+
                        '<th>'+
                                '<label class="button" name="date_Added1">Date Added</label>'+
                        '</th>'+
                        '<th>'+
                                '<label class="button" name="status1">Status</label>'+
                        '</th>'+
                        '<th>'+
                                '<label class="button" name="expiration1">Expiration</label>'+
                        '</th>'+
                        '<th>'+
                                '<label class="button" name="name1">Project Name</label>'+
                        '</th>'+
                        '<th>'+
                                '<label class="button" name="contact">Users\' Contact</label>'+
                        '</th>'+
                        '<th>'+
                                '<label class="button" name="datasets1">Valid Datasets</label>'+
                        '</th>'+
			'</tr>'+
			'<tr>'+
			'<td>'+
                                '<div class="col-xs-12 search-bar-container" id="projID">'+
                                        '<input id="search_bar_Add" type="text" class="form-control" placeholder="Project ID" name="projID">'+
                                '</div>'+
                        '</td>'+
                        '<td>'+
                                '<div class="col-xs-12 search-bar-container" id="date_Added1">'+
                                        '<label id="format">Format: YYYY-MM-DD</label>'+
                                        '<label id="exact"><input type="radio" name="groupP" onclick="showRange(\'toP\',\'search_bar25P\',\'none\')" checked >Exact</label>'+
                                        '<label id="range"><input type="radio" name="groupP" onclick="showRange(\'toP\',\'search_bar25P\',\'block\')">Range</label>'+
                                        '<input id="search_bar2" type="text" class="form-control" placeholder="Date Added" name="date_Added1">'+
                                        '<label id="toP" style="display:none"> To</label>'+
                                        '<input id="search_bar25P" type="text" class="form-control" placeholder="Date Added" style="display:none" name="date_Added1">'+
                                '</div>'+
                        '</td>'+
                        '<td>'+
                                '<div class="col-xs-12 search-bar-container" id="status1">'+
                                        '<label id="checkbox_enable">'+
                                        '<input type="radio" name="statP" value="ENABLE" checked>Enabled</label>'+
                                        '<label id="checkbox_disable">'+
                                        '<input type="radio" name="statP" value="DISABLE">Disabled</label>'+
                                '</div>'+
                        '</td>'+
                        '<td>'+
                                '<div class="col-xs-12 search-bar-container" id="expiration1">'+
                                        '<label id="format2">Format: YYYY-MM-DD</label>'+
                                        '<label id="exact2"><input type="radio" name="group2P" onclick="showRange(\'to2P\',\'search_bar45P\',\'none\')" checked>Exact</label>'+
                                        '<label id="range2"><input type="radio" name="group2P" onclick="showRange(\'to2P\',\'search_bar45P\',\'block\')">Range</label>'+
                                        '<input id="search_bar4P" type="text" class="form-control" placeholder="Expiration" name="expiration1">'+
                                        '<label id="to2P" style="display:none"> To</label>'+
                                        '<input id="search_bar45P" type="text" class="form-control" placeholder="Expiration" style="display:none" name="expiration1">'+
                                '</div>'+
                        '</td>'+
                        '<td>'+
                                '<div class="col-xs-12 search-bar-container" id="name1">'+
                                        '<input id="search_bar_Add" type="text" class="form-control" placeholder="Project Name" name="name1">'+
                                '</div>'+
                        '</td>'+
                        '<td>'+
                                '<div class="col-xs-12 search-bar-container" id="contact1">'+
                                        '<input id="search_bar_Add" type="text" class="form-control" placeholder="Users\' Contact" name="contact">'+
                                '</div>'+
                        '</td>'+
                        '<td>'+
                                '<div class="col-xs-12 search-bar-container" id="datasets1">'+
					'<label id="default">*Default Dataset is ALL</label>'+
                                        '<input id="search_bar_Add" type="text" class="form-control" placeholder="Datasets" name="datasets1">'+
                                '</div>'+
                        '</td>'+
			'</tr>'+
		'</table>'+
		'<div id="enter1">'+
                        '<button class="enter_Add" onclick="addParams(\'projects\')">Go</button>'+
                '</div>'+
		'<table id="mytableAddP">'+
                '</table>'+
		'</div>'
)
document.getElementById("defaultOpen").click();
};
