//shows input field for selected fields to search
function showMe(name, box, group) {
        var chboxs = document.getElementsByName(name);
        var vis = "none";
        var color = "#c7c0bc";
        for(var i=0;i<chboxs.length;i++) { 
            if(chboxs[i].checked){
             vis = "block";
             color = "#a6a09d";
                break;
            }
        }
        document.getElementById(box).style.display = vis;
        document.getElementById(box).style.background = color;
	var newBox = box + "Option";
	andOr(newBox, group);

        $('#users input[type=checkbox]').each(function () {
                if(this.checked) $(this).parent().addClass('active');
                else{            $(this).parent().removeClass('active'); }
        });
        $('#projects input[type=checkbox]').each(function () {
                if(this.checked) $(this).parent().addClass('active');
                else{            $(this).parent().removeClass('active'); }
        });

};

//adds and and/or to the bottom of each input field for the query results
function andOr(id, group) {
	var check = $('#'+group+' input[type=checkbox]:checked').size();
        if (check > 1) {
		var count = 0;
		$('#'+group+' input[type=checkbox]:checked').each(function() {
			count++;
			if (count == $('#'+group+' input[type=checkbox]:checked').size()){
                        	document.getElementById($(this).attr('name')+'Option').style.display = 'none';
			}
			else {
				document.getElementById($(this).attr('name')+'Option').style.display = 'block';
			}
                });
		$('#'+group+' input[type=checkbox]:not(:checked)').each(function() {
                        document.getElementById($(this).attr('name')+'Option').style.display = 'none';
                });

        }
        else {
                $('#'+group+' input[type=checkbox]').each(function() {
			document.getElementById($(this).attr('name')+'Option').style.display = 'none';
		});
        }

};

//gives the possibility of a date range
function showRange(to, bar, vis) {
        document.getElementById(to).style.display=vis
        document.getElementById(bar).style.display=vis
};

//displays users or project numbers tables
function openTab(evt, cityName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(cityName).style.display = "block";
    evt.currentTarget.className += " active";
};
//set users as default open
document.getElementById("defaultOpen").click();

//gets the input that the user entered to query the database with
function getParams(tableClass) {
	$('#mytable'+tableClass.substring(0,1).toUpperCase()+' tr').remove();
	var option = "";
	if (tableClass == 'users') {
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
	//checks if each input is valid 
        $('#'+tableClass+' input[type=checkbox]').each(function(){
                if(this.checked) {
                        var name = $(this).attr('name');
                        var text = "";
			option = ""
                        if ($('#'+name+'Option input[type=radio]:checked:visible').val() != null) {
                                option = " "+$('#'+name+'Option input[type=radio]:checked:visible').val();
                        }

                        if (name == 'status' || name == 'status1'){
                                //check for and or
                                if ($('#'+tableClass+' input[type=radio][value=ENABLE]').is(':checked')){
                                        text = 'ENABLED'+option;
                                } else {
                                        text = 'DISABLED'+option;
                                }
                        }
                        else if ($(this).val() != 'on') {
                                if ($('#'+tableClass+' input[type=radio][value=RANGE][name=group'+$(this).val()+']').is(':checked')){
                                        $('#'+tableClass+' input[type=text][name='+name+']').each(function(){
                                                text = text + $(this).val()+ " ";
                                        });
					text = text + option;
                                }
                                else {
                                        text = $('#'+tableClass+' input[type=text][name='+name+']').val()+option;
                                }
                        } 
                        else {
                                text = $('#'+tableClass+' input[type=text][name='+name+']').val() +option;
                        }
			if (name.indexOf("1") != -1) {
                                name = name.substring(0, name.indexOf("1"));
                        }
                        //param.push(name.toUpperCase()+"-"+text);
			param[name.toUpperCase()] = text;
                }
        });
	search(param); 
};

