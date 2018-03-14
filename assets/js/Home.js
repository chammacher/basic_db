draw = function(){
	$("body").html(
		'<div id="dropdown" onclick="$(\'#dropdown\').hide(\'fade\');updateCell()""><div class="content" onclick="event.stopPropagation();"></div></div>'+
		'<div><h3>Query Users/Project#s</h3>'+
        	'<button class="add" onclick="draw_add()">Add</button></div>'+
		'<div class="title"><h1>SEARCH</h1></div>'+
		'<div class="loglink"><i class="fa fa-spinner fa-spin check-logs-spinner"></i><a href="./assets/admin/log/">Check Logs</a></div>'+
		'<div id="notification" style="display: none">'+
			'<span class="dismiss"><a title="dismiss this notification"></a></span></div>'+
		'<div id="sync" style="display: none">'+
			'<button class="submit" onclick="pushChange()">Submit</button></div>'+
		'<div class="tab">'+
			'<button class="tablinks" onclick="openTab(event, \'users\')" id="defaultOpen">Users</button>'+
			'<button class="tablinks" onclick="openTab(event, \'projects\')">Projects</button>'+
		'</div>'+
		'<div id="users" class="tabcontent">'+
			'<h3>Users</h3>'+
			'<p>Select fields to search</p>'+
		'<table>'+
		'<tr class="btn-group" data-toggle="buttons">'+
			'<th>'+
				'<label class="button">'+
				'<input type="checkbox" name="usrID" onclick="showMe(name, \'usrID\', \'users\')" autocomplete="off">User ID</label>'+
			'</th>'+
			'<th>'+
				'<label class="button">'+
				'<input type="checkbox" value="" name="date_Added" onclick="showMe(name, \'date_Added\', \'users\')" autocomplete="off"> Date Added</label>'+
			'</th>'+
			'<th>'+
				'<label class="button">'+
				'<input type="checkbox" name="status" onclick="showMe(name, \'status\', \'users\')" autocomplete="off"> Status</label>'+
			'</th>'+
			'<th>'+
				'<label class="button">'+
				'<input type="checkbox" value="2" name="expiration" onclick="showMe(name, \'expiration\', \'users\')" autocomplete="off"> Expiration</label>'+
			'</th>'+
			'<th>'+
				'<label class="button">'+
				'<input type="checkbox" name="name" onclick="showMe(name, \'name\', \'users\')" autocomplete="off">Users\' Name</label>'+
			'</th>'+
			'<th>'+
				'<label class="button">'+
				'<input type="checkbox" name="organization" onclick="showMe(name, \'organization\', \'users\')" autocomplete="off">Organization</label>'+
			'</th>'+
			'<th>'+
				'<label class="button">'+
				'<input type="checkbox" name="email" onclick="showMe(name, \'email\', \'users\')" autocomplete="off">Email</label>'+
			'</th>'+
			'<th>'+
				'<label class="button">'+
				'<input type="checkbox" name="phone" onclick="showMe(name, \'phone\', \'users\')" autocomplete="off">Phone#</label>'+
			'</th>'+
			'<th>'+
				'<label class="button">'+
				'<input type="checkbox" name="datasets" onclick="showMe(name, \'datasets\', \'users\')" autocomplete="off">Valid Datasets</label>'+
			'</th>'+
		'</tr>'+
		'<tr>'+
			'<td>'+
				'<div class="search-container" style="display:none" id="usrID">'+
                               		'<input id="search_bar" type="text" class="form-control" placeholder="User ID" name="usrID">'+
				'</div>'+
                        '</td>'+
			'<td>'+
				'<div class="search-container" style="display:none" id="date_Added">'+
                                	'<label id="format">Format: YYYY-MM-DD</label>'+
                                	'<label id="exact"><input type="radio" name="group" onclick="showRange(\'to\',\'search_bar25\',\'none\')" checked value="EXACT">Exact</label>'+
                                	'<label id="range"><input type="radio" name="group" onclick="showRange(\'to\',\'search_bar25\',\'block\')" value="RANGE">Range</label>'+
                                	'<input id="search_bar2" type="text" class="form-control" placeholder="Date Added" name="date_Added">'+
                                	'<label id="to" style="display:none"> To</label>'+
                                	'<input id="search_bar25" type="text" class="form-control" placeholder="Date Added" style="display:none" name="date_Added">'+
				'</div>'+
                        '</td>'+
			'<td>'+
				'<div class="search-container" style="display:none" id="status">'+
       	                        	'<label id="checkbox_enable">'+
                                	'<input type="radio" name="stat" value="ENABLE" checked>Enabled</label>'+
                                	'<label id="checkbox_disable">'+
                                	'<input type="radio" name="stat" value="DISABLE">Disabled</label>'+
				'</div>'+
                        '</td>'+
			'<td>'+
				'<div class="search-container" style="display:none" id="expiration">'+
                                	'<label id="format2">Format: YYYY-MM-DD</label>'+
                                	'<label id="exact2"><input type="radio" name="group2" onclick="showRange(\'to2\',\'search_bar45\',\'none\')" checked value="EXACT">Exact</label>'+
                                	'<label id="range2"><input type="radio" name="group2" onclick="showRange(\'to2\',\'search_bar45\',\'block\')" value="RANGE">Range</label>'+
                                	'<input id="search_bar4" type="text" class="form-control" placeholder="Expiration" name="expiration">'+
                                	'<label id="to2" style="display:none"> To</label>'+
                                	'<input id="search_bar45" type="text" class="form-control" placeholder="Expiration" style="display:none" name="expiration">'+
				'</div>'+
                        '</td>'+
			'<td>'+
				'<div class="search-container" style="display:none" id="name">'+
                                	'<input id="search_bar" type="text" class="form-control" placeholder="Users\' Name" name="name">'+
				'</div>'+
                        '</td>'+
			'<td>'+
				'<div class="search-container" style="display:none" id="organization">'+
                                	'<input id="search_bar" type="text" class="form-control" placeholder="Oragnization" name="organization">'+
				'</div>'+
                        '</td>'+
			'<td>'+
				'<div class="search-container" style="display:none" id="email">'+
                                	'<input id="search_bar" type="text" class="form-control" placeholder="Email" name="email">'+
				'</div>'+
                        '</td>'+
			'<td>'+
				'<div class="search-container" style="display:none" id="phone">'+
                                	'<input id="search_bar" type="text" class="form-control" placeholder="Phone" name="phone">'+
				'</div>'+
                        '</td>'+
			'<td>'+
				'<div class="search-container" style="display:none" id="datasets">'+
					'<label id="format2">Format: SERVER: - GROUP:</label>'+
                                	'<input id="search_bar" type="text" class="form-control" placeholder="Datasets" name="datasets">'+
				'</div>'+
                        '</td>'+
		'</tr>'+
		'<tr>'+
			'<td>'+
				'<div class="andOr" style="display:none" id="usrIDOption">'+
                                        '<label>'+
                                        '<input type="radio" name="UID" value="OR" checked>OR</label>'+
                                        '<label>'+
                                        '<input type="radio" name="UID" value="AND">AND</label>'+
                                '</div>'+
                        '</td>'+
                        '<td>'+
				'<div class="andOr" style="display:none" id="date_AddedOption">'+
                                        '<label>'+
                                        '<input type="radio" name="DA" value="OR" checked>OR</label>'+
                                        '<label>'+
                                        '<input type="radio" name="DA" value="AND">AND</label>'+
                                '</div>'+
                        '</td>'+
                        '<td>'+
				'<div class="andOr" style="display:none" id="statusOption">'+
                                        '<label>'+
                                        '<input type="radio" name="S" value="OR" checked>OR</label>'+
                                        '<label>'+
                                        '<input type="radio" name="S" value="AND">AND</label>'+
                                '</div>'+
                        '</td>'+
                        '<td>'+
				'<div class="andOr" style="display:none" id="expirationOption">'+
                                        '<label>'+
                                        '<input type="radio" name="EX" value="OR" checked>OR</label>'+
                                        '<label>'+
                                        '<input type="radio" name="EX" value="AND">AND</label>'+
                                '</div>'+
                        '</td>'+
                        '<td>'+
				'<div class="andOr" style="display:none" id="nameOption">'+
                                        '<label>'+
                                        '<input type="radio" name="UN" value="OR" checked>OR</label>'+
                                        '<label>'+
                                        '<input type="radio" name="UN" value="AND">AND</label>'+
                                '</div>'+
                        '</td>'+
                        '<td>'+
				'<div class="andOr" style="display:none" id="organizationOption">'+
                                        '<label>'+
                                        '<input type="radio" name="O" value="OR" checked>OR</label>'+
                                        '<label>'+
                                        '<input type="radio" name="O" value="AND">AND</label>'+
                                '</div>'+
                        '</td>'+
                        '<td>'+
				'<div class="andOr" style="display:none" id="emailOption">'+
                                        '<label>'+
                                        '<input type="radio" name="E" value="OR" checked>OR</label>'+
                                        '<label>'+
                                        '<input type="radio" name="E" value="AND">AND</label>'+
                                '</div>'+
                        '</td>'+
			'<td>'+
				'<div class="andOr" style="display:none" id="phoneOption">'+
                                        '<label>'+
                                        '<input type="radio" name="P#" value="OR" checked>OR</label>'+
                                        '<label>'+
                                        '<input type="radio" name="P#" value="AND">AND</label>'+
                                '</div>'+
			'</td>'+
			'<td>'+
				'<div class="andOr" style="display:none" id="datasetsOption">'+
                                        '<label>'+
                                        '<input type="radio" name="D" value="OR" checked>OR</label>'+
                                        '<label>'+
                                        '<input type="radio" name="D" value="AND">AND</label>'+
                                '</div>'+
			'</td>'+
		'</tr>'+
		'</table>'+
		'<div id="enter0">'+
			'<button class="enter" onclick="getParams(\'users\')">Go</button>'+
		'</div>'+
		'<table id="mytableU">'+
			'<col width="60">'+
                '</table>'+
		'</div>'+
	'<div id="projects" class="tabcontent">'+
		'<div>'+
			'<h3>Projects</h3>'+
			'<p>Select fields to search</p>'+
		'</div>'+
		'<table>'+
		'<tr class="btn-group" data-toggle="buttons">'+
			'<th>'+
				'<label class="button">'+
				'<input type="checkbox" name="projID" onclick="showMe(name, \'projID\', \'projects\')" autocomplete="off">Project Number</label>'+
			'</th>'+
			'<th>'+
				'<label class="button">'+
				'<input type="checkbox" value="P" name="date_Added1" onclick="showMe(name, \'date_Added1\', \'projects\')" autocomplete="off">Date Added</label>'+
			'</th>'+
			'<th>'+
				'<label class="button">'+
				'<input type="checkbox" name="status1" onclick="showMe(name, \'status1\', \'projects\')" autocomplete="off">Status</label>'+
			'</th>'+
			'<th>'+
				'<label class="button">'+
				'<input type="checkbox" value="2P" name="expiration1" onclick="showMe(name, \'expiration1\', \'projects\')" autocomplete="off"> Expiration</label>'+
			'</th>'+
			'<th>'+
				'<label class="button">'+
				'<input type="checkbox" name="name1" onclick="showMe(name, \'name1\', \'projects\')" autocomplete="off">Project Name</label>'+
			'</th>'+
			'<th>'+
				'<label class="button">'+
				'<input type="checkbox" name="contact" onclick="showMe(name, \'contact1\', \'projects\')" autocomplete="off">Users\' Contact</label>'+
			'</th>'+
			'<th>'+
				'<label class="button">'+
				'<input type="checkbox" name="datasets1" onclick="showMe(name, \'datasets1\', \'projects\')" autocomplete="off">Valid Datasets</label>'+
			'</th>'+
		'</tr>'+
		'<tr>'+
			'<td>'+
                        	'<div class="col-xs-12 search-bar-container" style="display:none" id="projID">'+
                	        	'<input id="search_bar" type="text" class="form-control" placeholder="Project ID" name="projID">'+
				'</div>'+
                        '</td>'+
			'<td>'+
                        	'<div class="col-xs-12 search-bar-container" style="display:none" id="date_Added1">'+
                                	'<label id="format">Format: YYYY-MM-DD</label>'+
                                	'<label id="exact"><input type="radio" name="groupP" onclick="showRange(\'toP\',\'search_bar25P\',\'none\')" checked >Exact</label>'+
                                	'<label id="range"><input type="radio" name="groupP" onclick="showRange(\'toP\',\'search_bar25P\',\'block\')">Range</label>'+
                                	'<input id="search_bar2" type="text" class="form-control" placeholder="Date Added" name="date_Added1">'+
                                	'<label id="toP" style="display:none"> To</label>'+
                                	'<input id="search_bar25P" type="text" class="form-control" placeholder="Date Added" style="display:none" name="date_Added1">'+
				'</div>'+
                        '</td>'+
			'<td>'+
                        	'<div class="col-xs-12 search-bar-container" style="display:none" id="status1">'+
                                	'<label id="checkbox_enable">'+
                                	'<input type="radio" name="statP" value="ENABLE" checked>Enabled</label>'+
                                	'<label id="checkbox_disable">'+
                                	'<input type="radio" name="statP" value="DISABLE">Disabled</label>'+
				'</div>'+
                        '</td>'+
			'<td>'+
                        	'<div class="col-xs-12 search-bar-container" style="display:none" id="expiration1">'+
                                	'<label id="format2">Format: YYYY-MM-DD</label>'+
                                	'<label id="exact2"><input type="radio" name="group2P" onclick="showRange(\'to2P\',\'search_bar45P\',\'none\')" checked>Exact</label>'+
                                	'<label id="range2"><input type="radio" name="group2P" onclick="showRange(\'to2P\',\'search_bar45P\',\'block\')">Range</label>'+
                                	'<input id="search_bar4P" type="text" class="form-control" placeholder="Expiration" name="expiration1">'+
                                	'<label id="to2P" style="display:none"> To</label>'+
                                	'<input id="search_bar45P" type="text" class="form-control" placeholder="Expiration" style="display:none" name="expiration1">'+
				'</div>'+
                        '</td>'+
			'<td>'+
                        	'<div class="col-xs-12 search-bar-container" style="display:none" id="name1">'+
                                	'<input id="search_bar" type="text" class="form-control" placeholder="Project Name" name="name1">'+
				'</div>'+
                        '</td>'+
			'<td>'+
                        	'<div class="col-xs-12 search-bar-container" style="display:none" id="contact1">'+
                                	'<input id="search_bar" type="text" class="form-control" placeholder="Users\' Contact" name="contact">'+
				'</div>'+
                        '</td>'+
			'<td>'+
                        	'<div class="col-xs-12 search-bar-container" style="display:none" id="datasets1">'+
					'<label id="format2">Format: SERVER: - GROUP:</label>'+
                                	'<input id="search_bar" type="text" class="form-control" placeholder="Datasets" name="datasets1">'+
				'</div>'+
                        '</td>'+
		'</tr>'+
		'<tr>'+
			'<td>'+
                                '<div class="andOr" style="display:none" id="projIDOption">'+
                                        '<label>'+
                                        '<input type="radio" name="PID" value="OR" checked>OR</label>'+
                                        '<label>'+
                                        '<input type="radio" name="PID" value="AND">AND</label>'+
                                '</div>'+
                        '</td>'+
                        '<td>'+
                                '<div class="andOr" style="display:none" id="date_Added1Option">'+
                                        '<label>'+
                                        '<input type="radio" name="PDA" value="OR" checked>OR</label>'+
                                        '<label>'+
                                        '<input type="radio" name="PDA" value="AND">AND</label>'+
                                '</div>'+
                        '</td>'+
                        '<td>'+
                                '<div class="andOr" style="display:none" id="status1Option">'+
                                        '<label>'+
                                        '<input type="radio" name="SP" value="OR" checked>OR</label>'+
                                        '<label>'+
                                        '<input type="radio" name="SP" value="AND">AND</label>'+
                                '</div>'+
                        '</td>'+
                        '<td>'+
                                '<div class="andOr" style="display:none" id="expiration1Option">'+
                                        '<label>'+
                                        '<input type="radio" name="PE" value="OR" checked>OR</label>'+
                                        '<label>'+
                                        '<input type="radio" name="PE" value="AND">AND</label>'+
                                '</div>'+
                        '</td>'+
                        '<td>'+
                                '<div class="andOr" style="display:none" id="name1Option">'+
                                        '<label>'+
                                        '<input type="radio" name="PN" value="OR" checked>OR</label>'+
                                        '<label>'+
                                        '<input type="radio" name="PN" value="AND">AND</label>'+
                                '</div>'+
                        '</td>'+
                        '<td>'+
                                '<div class="andOr" style="display:none" id="contactOption">'+
                                        '<label>'+
                                        '<input type="radio" name="UC" value="OR" checked>OR</label>'+
                                        '<label>'+
                                        '<input type="radio" name="UC" value="AND">AND</label>'+
                                '</div>'+
                        '</td>'+
                        '<td>'+
                                '<div class="andOr" style="display:none" id="datasets1Option">'+
                                        '<label>'+
                                        '<input type="radio" name="DP" value="OR" checked>OR</label>'+
                                        '<label>'+
                                        '<input type="radio" name="DP" value="AND">AND</label>'+
                                '</div>'+
                        '</td>'+
		'</tr>'+
		'</table>'+
		'<div id="enter1">'+
			'<button class="enter" onclick="getParams(\'projects\')">Go</button>'+
		'</div>'+
		'<table id="mytableP">'+
			'<col width="60">'+
        	'</table>'+
	'</div>'
)
document.getElementById("defaultOpen").click();
};    	
	
draw();

