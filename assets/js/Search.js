var list = [];
var success = false;


//searches the database and returns rows that fit the search description
search = function(param) {
	$.ajax({
                url: './assets/python/search.py',
                data: param,
                traditional: true,
                async: true,
		success: function(response){
			try{
				var json_parse = JSON.parse(response);
				draw_table(json_parse);
			}catch(err) {print_err(response);}
        	},
		error: function(response){
			console.log('Error');
			console.log(response);
		}	
	});
}

//if an invalid argument is given when trying to create new user print an error
print_err = function(message) {
	var json = JSON.parse(message);
	var tab = 'P';
        if (Object.keys(json).length == 9){
                var tab = 'U';
        }
	var table = document.getElementById("mytable"+tab);
        var err_row = table.insertRow(0);
	for(var key in json) {
		if (json[key] != '') {
			var t  = err_row.insertCell(err_row.cells.length);
			t.style.color = "red";
			t.innerHTML = key +' '+json[key];
		}
	}
}

//sets up the table for the requested rows
draw_table = function(message) {
	var tab = 'P';
	if (message[0].length == 9){
		var tab = 'U';
	}
	var table = document.getElementById("mytable"+tab);
	//for each element place it in a cell with attributes that fit it
	for (var arr in message) {
		row = table.insertRow(table.rows.length);
		for (var i = 0; i <= message[arr].length;i++) {
			cell = row.insertCell(row.cells.length);
			if(i == 0){
				//update this to be close button
				cell.innerHTML = '<i class="fa fa-times delete-button" onclick="Delete(this.parentElement.parentElement)"></i>';
			}
			else{
				if (message[arr][i-1] == null) {
					cell.innerHTML = 'empty';
				}else{
					cell.innerHTML = message[arr][i-1];
				}
				if (tab == 'U' && i == 9){
					setDropdown(cell);
				}
				else if (tab == 'P' && i == 7){
					setDropdown(cell);
				}
				else{
					cell.setAttribute("ondblclick","setSearch(this)");
				}
			}
		}
	}
}

//when you click off of an text box used to edit, update the old text box with your new input
clickOff = function(cell, temp, og) {
	cell.innerHTML = temp;
	if (temp != og){
		var obj = [cell, temp, og];
		list.push(obj);
		//prompt the user to confirm their changes when ready
		document.getElementById("sync").style.display = 'block';
		//getRow(cell, temp, og);
	}
}

//when user confirms changes update the database and create files needed
pushChange = function(){
	for(var i = 0; i < list.length;i++){
		getRow(list[i][0],list[i][1],list[i][2]);
	}
        showPopup(success);
	//reset list to be empty and hide submit button
	document.getElementById("sync").style.display = "none";
	list = [];
        success = false;
}

//gives attributes to each cell to be able to edit the values
setSearch = function(cell) {
	if (cell.innerHTML.length > 4){
		if (cell.innerHTML.substring(0,4) == '<inp'){
			$(document).click(function(event) {
                		if(!$(event.target).closest(cell).length) {
                        		cell.innerHTML = cell.innerHTML.split(/"/);
					return;
                		}
        		});
		}else {
                	var temp = cell.innerHTML;
                	cell.innerHTML = '';
                	var feld = document.createElement("textarea");
        	        //feld.setAttribute("type", "text");
       		        //feld.setAttribute("value",temp);
			feld.value = temp;
			feld.setAttribute("onblur", "clickOff(this.parentElement, value, '"+temp+"')");
        	        cell.appendChild(feld);

        	}
	}else {
                var temp = cell.innerHTML;
                cell.innerHTML = '';
                var feld = document.createElement("input");
                feld.setAttribute("type", "text");
                feld.setAttribute("value",temp);
		feld.setAttribute("onblur", "clickOff(this.parentElement, value, '"+temp+"')");
                cell.appendChild(feld);
        }
	feld.focus();		
}

//when a value is edited return that row and its content to be entered into the database
getRow = function(cell, newVal, oldVal) {
	var tableClass = cell.parentElement.parentElement.parentElement.id;
	if (tableClass == 'mytableU') {
		//param used to update database
                var param = ['USERS'];
		//editusr to create files needed to update users permissions
		var editusr = ['USERS'];
		//editusr_old used to remove previous permissions
		var editusr_old = ['USERS'];
        }
        else {
                var param = ['PROJECTS'];
		var editusr = ['PROJECTS'];
		var editusr_old = ['PROJECTS'];
        }
	for (var i = 1; i < cell.parentElement.cells.length;i++){
		if (i == cell.parentElement.cells.length-1){
			console.log(cell.parentElement.cells[i].innerHTML.split('</button> ')[1]);
			console.log(newVal);
			if(cell.parentElement.cells[i].innerHTML.split('</button> ')[1] == newVal){
				var val = '+new+'+cell.parentElement.cells[i].innerHTML.split('</button> ')[1]
				var val2 = oldVal
			}else{
				var val = cell.parentElement.cells[i].innerHTML.split('</button> ')[1]	
				var val2 = val;
			}
			var val3 = cell.parentElement.cells[i].innerHTML.split('</button> ')[1];
		}
		else if (cell.parentElement.cells[i].innerHTML != newVal){
			var val = cell.parentElement.cells[i].innerHTML;
			var val2 = cell.parentElement.cells[i].innerHTML;
			var val3 = val;
		}
		//else if(cell.parentElement.cells[i].innerHTML == 'ENABLED'){
		//	var val2 = 'DISABLED';
		//	var val = cell.parentElement.cells[i].innerHTML;
		//	var val3 = val;
		//}
		else {
			var val = "+new+"+newVal;
                        var val2 = cell.parentElement.cells[i].innerHTML;
			var val3 = cell.parentElement.cells[i].innerHTML;
		}
		param.push(val);
		editusr_old.push(val2);
		editusr.push(val3);
	}
	param.push(oldVal);
	//edit the users info in the database
	$.ajax({
                url: './assets/python/edit.py',
                data: {data: param},
                traditional: true,
                async: true,
                success: function(response){
			console.log(response);
                        if (response != ''){
                                cell.innerHTML = oldVal;
                                success = true;
                        }
                        else {
                                success = false;
                        }
                },
                error: function(xhr, status){
                        console.log('error');
                        console.log(status);
                }
        });
	//remove the previous permisions for usr to update to the new permisions
        $.ajax({
                url: './assets/python/editusr.py',
                data: {data: editusr_old},
                traditional: true,
                async: true,
                success: function(response){console.log(response);},
                error: function(xhr, status){
                        console.log('error');
                        console.log(status);
                }
        });
	$(".check-logs-spinner").show('fade');
	// edit the users new permision across all needed machines
	$.ajax({
                url: './assets/python/editusr.py',
                data: {data: editusr},
                traditional: true,
                async: true,
                success: function(response){
			$(".check-logs-spinner").hide('fade');
			//when finished alert user with a log of what happened
			console.log(response);
                },
                error: function(xhr, status){
                        console.log('error');
                        console.log(status);
                }
        });	
}

//show a green or red symbol if the database entry was successfull or not
showPopup = function(color) {
	if(color){
		var back_color = 'red';
		var message = 'INVALID';
	}
	else {
		var back_color = '#70d627';
		var message = 'SUCCESS';
	}
	$("#notification").css("background-color",back_color);
	$("#notification").fadeIn("slow").html(message);
	
	$("#notification").delay(800).fadeOut("slow");
}

