Delete = function(row){
	var tableClass = row.parentElement.parentElement.id;
        if (tableClass == 'mytableU') {
                var param = ['USERS'];
                var editusr = ['USERS'];
        }
        else {
                var param = ['PROJECTS'];
                var editusr = ['PROJECTS'];
        }
        for (var i = 1; i < row.cells.length;i++){
                if (row.cells[i].innerHTML.toUpperCase() == 'ENABLED'){
			editusr.push('DISABLED');
                } else {
			editusr.push(row.cells[i].innerHTML);
		}
                param.push(row.cells[i].innerHTML);
        }
	var r = confirm('Are you sure you want to delete this User?');
	if (r == true){
		$.ajax({
        	        url: './assets/python/delete.py',
        	        data: {data: param},
        	        traditional: true,
        	        async: true,
        	        success: function(response){
				console.log(response);
        	        },
        	        error: function(response){
        	                console.log('Error');
        	                console.log(response);
        	        }
        	});
		$(".check-logs-spinner").show("fade");
		$.ajax({
                        url: './assets/python/editusr.py',
                        data: {data: editusr},
                        traditional: true,
                        async: true,
                        success: function(response){
				$(".check-logs-spinner").hide("fade");
                                console.log(response);
                        },
                        error: function(response){
                                console.log('Error');
                                console.log(response);
                        }
                });
		document.getElementById(tableClass).deleteRow(row.rowIndex);
	}
}

