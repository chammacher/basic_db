//gets the entered information from the user to add a new user to the database
addParams = function(table){
        if (table == 'users') {
		var editusr = ['USERS'];
                var param = {
                        TABLE: 'USERS',
                        USRID: 'NULL',
                        DATE_ADDED: 'NULL',
                        STATUS: 'NULL',
                        EXPIRATION: 'NULL',
                        NAME: 'NULL',
                        ORGANIZATION: 'NULL',
                        EMAIL: 'NULL',
                        PHONE: 'NULL',
                        DATASETS: 'NULL'
                };
        }
        else {
		var editusr = ['PROJECTS']
                var param = {
                        TABLE: 'PROJECTS',
                        PROJID: 'NULL',
                        DATE_ADDED: 'NULL',
                        STATUS: 'NULL',
                        EXPIRATION: 'NULL',
                        NAME: 'NULL',
                        CONTACT: 'NULL',
                        DATASETS: 'NULL'
                };
        }
	//for each button check if the input was valid
        $('#'+table+' label[class=button]').each(function(){
                var name = $(this).attr('name');
                var text = "";

                if (name == 'status' || name == 'status1'){
                        //check for and or
                        if ($('#'+table+' input[type=radio][value=ENABLE]').is(':checked')){
                                text = 'ENABLED';
                        } else {
                                text = 'DISABLED';
                        }
                }
                else if ($(this).val() != 'on') {
                        if ($('#'+table+' input[type=radio][value=RANGE][name=group'+$(this).val()+']').is(':checked')){
                                $('#'+table+' input[type=text][name='+name+']').each(function(){
                                        text = text + $(this).val()+ " ";
                                });
                                text = text;
                        }
                        else {
                                text = $('#'+table+' input[type=text][name='+name+']').val();
                        }
                }
                else {
                        text = $('#'+table+' input[type=text][name='+name+']').val();
                }
                if (name.indexOf("1") != -1) {
                        name = name.substring(0, name.indexOf("1"));
                }
                //param.push(name.toUpperCase()+"-"+text);
                param[name.toUpperCase()] = text;
                if(text == ""){
			text = "empty";
		}
		editusr.push(text)
        });
	console.log(param)
	addCommit(param, table, editusr);
}

//adds a user to the database and creates permission files
addCommit = function(param, table, editusr){
	$.ajax({
                url: './assets/python/add.py',
                data: param,
                traditional: true,
                async: true,
                success: function(response){
			if (response != ''){
				printErr(response, table);
			}
			else{
				var t = 'P';
			        if (table == 'users'){
			                t = 'U';
			        }
				$('#mytableAdd'+t+' tr').remove();
				var tab = document.getElementById("mytableAdd"+t);
			        var err_row = tab.insertRow(0);
				var t = err_row.insertCell(0);
				t.style.color = "green";
				t.innerHTML = "Success";
				$(".check-logs-spinner").show("fade");
				$.ajax({
			                url:'./assets/python/editusr.py',
					data: {data: editusr},
			                traditional: true,
			                async: true,
			                success: function(response){
						$(".check-logs-spinner").hide("fade");
						alert(response);
                			},
			                error: function(reponse){
			                        console.log('Error');
                        			console.log(response);
			                }
        			});	 
			}
                },
                error: function(response){
                        console.log('Error');
                        console.log(response);
                }
        });
}

printErr = function(message, table){
	var t = 'P';
	if (table == 'users'){
		t = 'U';
	}
	$('#mytableAdd'+t+' tr').remove();
	var tab = document.getElementById("mytableAdd"+t);
        var err_row = tab.insertRow(0);
	var lines = message.split('\n');
        for(var i = 0;i < lines.length;i++) {
                var t  = err_row.insertCell(err_row.cells.length);
                t.style.color = "red";
                t.innerHTML = lines[i];
        }
}
