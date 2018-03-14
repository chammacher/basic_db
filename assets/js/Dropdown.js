var curr_cell = null;
var curr_selection = [];
var og = null;

//set the attribute for the edit button
setDropdown = function(cell){
	var temp = cell.innerHTML;
	$(cell).html('<button onclick="$(\'#dropdown\').show(\'fade\');setContent(this.parentElement)">Edit</button> '+temp);
}

//select all the checkboxs that should be when opening popup windwo
setContent = function(cell) {
	value = cell.innerHTML.split('</button>')[1];
	og = value;
	var t = value.split(" - ");
	curr_cell = cell;
	//check for servers and groups
	if (t.length == 1){
		//check if its all or just a server
		if (t == ' ALL'){
			//set content to select ALL
			$('#ALL').prop('checked',true);
			if(!curr_selection.includes('ALL')){
				curr_selection.push('ALL');
			}
			//set all other checkboxs to be greyed out
			grayOut(true);
		}
		else{
			//set content to select certain servers
			server = t[0].split(":");
			servers = server[1].split(",").forEach(function(s){
				$('#'+s).prop('checked',true);
				if(!curr_selection.includes(s)){
					curr_selection.push(s);
				}
			});
		}
	}
	else{
		//set content to select servers and groups
		$('#ALL').prop('checked',false);
		grayOut(false);
		server = t[0].split(":");
		group = t[1].split(":");
		servers = server[1].split(",").forEach(function(s){
			$('#'+s).prop('checked',true);
			if(!curr_selection.includes(s)){
				curr_selection.push(s);
			}
			groups = group[1].split(",").forEach(function(g){
                	        $('#'+s+'-'+g).prop('checked',true);
				if(!curr_selection.includes(g)){
					curr_selection.push(g);
				}
        	        });	
		});
	}
	drawDropdown();
}

reset = function() {
        value = og;
        var t = value.split(" - ");
        //check for servers and groups
        if (t.length == 1){
                //check if its all or just a server
                if (t == ' ALL'){
                        //set content to select ALL
                        $('#ALL').prop('checked',true);
                        if(!curr_selection.includes('ALL')){
                                curr_selection.push('ALL');
                        }
                        //set all other checkboxs to be greyed out
                        grayOut(true);
                }
                else{
                        //set content to select certain servers
                        server = t[0].split(":");
                        servers = server[1].split(",").forEach(function(s){
                                $('#'+s).prop('checked',true);
                                if(!curr_selection.includes(s)){
                                        curr_selection.push(s);
                                }
                        });
                }
        }
        else{
                //set content to select servers and groups
		var idx = curr_selection.indexOf('ALL');
		if (idx > -1) {
			console.log('here')
			curr_selection.splice(idx, 1);
		}
                server = t[0].split(":");
                group = t[1].split(":");
                servers = server[1].split(",").forEach(function(s){
                        $('#'+s).prop('checked',true);
                        if(!curr_selection.includes(s)){
                                curr_selection.push(s);
                        }
                        groups = group[1].split(",").forEach(function(g){
                                $('#'+s+'-'+g).prop('checked',true);
                                if(!curr_selection.includes(g)){
                                        curr_selection.push(g);
                                }
                        });
                });
        }
}

checkALL = function(id){
	var sats = id.split('-');
	if(document.getElementById('ALL').checked){
		grayOut(true);
		//curr_selection = [];
		if(!curr_selection.includes('ALL')){
                        curr_selection.push('ALL');
                }
	}else{
		grayOut(false);
		if(document.getElementById(id).checked){
			if(sats.length > 1){
		                if(!curr_selection.includes(sats[1])){
       		 	                curr_selection.push(sats[1]);
                		}
				$('#'+sats[0]).prop('checked',true);
				if(!curr_selection.includes(sats[0])){
                                        curr_selection.push(sats[0]);
                                }
			}else{
				if(!curr_selection.includes(sats[0])){
                                        curr_selection.push(sats[0]);
                                }
			}
        	}
		else{
			if(sats.length > 1){
                                var index = curr_selection.indexOf(sats[1]);
				curr_selection.splice(index, 1);
                        }else{
                                var index = curr_selection.indexOf(sats[0]);
				curr_selection.splice(index, 1);
                        }
		}
	}
}

grayOut = function(gray){
	if (gray){
		$('#dropdown .content .dataset-checkbox').css('opacity',0.5);
		$('#dropdown .content .header').css('opacity',0.5);
		$('#dropdown .content #div-ALL').css('opacity',1.0);
	}
	else{
		$('#dropdown .content .dataset-checkbox').css('opacity',1.0);
                $('#dropdown .content .header').css('opacity',1.0);
	}
}

updateCell = function(){
	//loop through each check box to see if its checked or not
	//start with ALL checkbox
	if(document.getElementById('ALL').checked){
		//update cell text to say ALL
		var temp = 'ALL';
	}
	else{
		var server_string = 'SERVER:';
		var s_array = [];
		var server_check = false;
		var group_string = 'GROUP:';
		var g_array = [];
		var group_check = false;
		curr_selection.forEach(function(key){
			if(key === key.toUpperCase()){
				g_array.push(key);
				group_check = true;
			}else if(key === key.toLowerCase()){
				s_array.push(key);
				server_check = true;
			}
		});
		//set temp to new data added
		if(server_check && group_check){
			var temp = server_string + s_array.join(',') + ' - ' + group_string+g_array.join(',');
		}else if(server_check){
			var temp = server_string+s_array.join(',');
		}else{
			var temp = 'ALL'
		}
	}
	//end by clearing all the checkboxes
	$('#dropdown .content :input').prop('checked',false);
	grayOut(false);
	curr_selection = [];
	if(og == ' '+temp){
		//do nothing
	}else{
		curr_cell.innerHTML = curr_cell.innerHTML.split('</button>')[0]+ '</button> ' + temp;
		document.getElementById("sync").style.display = 'block';
		list.push([curr_cell, temp, og]);	
	}
}

drawDropdown = function(){
	$("#dropdown .content").html('<label id="content-header">Edit info for User: </label>');

	//set up basic layout of this screen
	$("#dropdown .content").append('<div class="tests-box" id="div0"></div><div class="tests-box" id="div1"></div><div class="tests-box" id="div2"></div><div class="tests-box" id="div3"></div>'+
		'<div id="button-div"><button class="util-button" onclick="$(\'#dropdown\').hide(\'fade\');updateCell()"> Save Changes</button>'+
		'<button class="util-button" onclick="$(\'#dropdown\').hide(\'fade\');reset()"> Discard Changes</button></div>');


	$.ajax({
       	 url: './assets/python/get_host.py',
        	data: false, 
       	 traditional: true,
        	async: true,
        	success: function(response){
        	        var tests = JSON.parse(response);
			Object.keys(tests).forEach(function(key, idx){
				var test = tests[key];
				$("#dropdown .content #div"+idx%4).append(
					'<div class="tests-box-padding">'+
						'<div class="header" id="div-'+key+'"><input type="checkbox" onclick="checkALL(id)" id="'+key+'"></input> '+key+'</div>'+
						'<div class="dataset-checkbox">'+
						test.map(function(a){
							if(test != ""){
								return '<label class="test"><input type="checkbox" onclick="checkALL(id)" id="'+key+'-'+a+'"></input> '+a+'</label>';
							}else{return '';}
						}).join('')+
						'</div>'+
					'</div>'
				);		
			});
		},
        	error: function(xhr, status){
        	        console.log('error');
        	        console.log(status);
        	}
	});
}
