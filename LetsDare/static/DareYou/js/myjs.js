function clearstorage(count)
{
    localStorage.clear()
    for (var i = 1; i <= count; i++)
    {
        document.getElementById("s" + i).value = "Select";
        document.getElementById("s" + i).style.backgroundColor="#e7e7e7";
        console.log(i+" N S")
    }
}
   


function selected(count, item)
{
    if (localStorage.getItem("first") == null)
    {
        localStorage.setItem("first", "No")
        for (var i = 1; i <= count; i++)
        {
            localStorage.setItem(i, "N")
            document.getElementById("s" + i).value = "Select";
            document.getElementById("s" + i).style.backgroundColor="#e7e7e7";
            //document.getElementById("s" + i).classList.remove("removal_btn");
            //document.getElementById("s" + i).classList.add("slection_btn");
            console.log(i+" N S");
        }
    }
    var va = localStorage.getItem(item);
    if (va == "N")
    {
        localStorage.setItem(item, "Y");
        document.getElementById("s" + item).value = "Remove";
        document.getElementById("s" + item).style.backgroundColor="red";
        //document.getElementById("s" + item).classList.remove("slection_btn");
        //document.getElementById("s" + item).classList.add("removal_btn");
        console.log(item+" Y R");
    } 
    else{
        localStorage.setItem(item, "N");
        document.getElementById("s" + item).value = "Select";
        document.getElementById("s" + item).style.backgroundColor="#e7e7e7";
        //document.getElementById("s" + item).classList.remove("removal_btn");
        //document.getElementById("s" + item).classList.add("selection_btn");
        console.log(item+" N S");
    }
}

function validation(count){
	if(localStorage.getItem("first")==null){
		document.getElementById("error_msg").innerHTML="no data";
		document.getElementById("error_msg").style.color="red";
		return false
	}
	var selected_q_str=""
	if(localStorage.getItem("first")!=null)
	{
		var q_count=0
		for (var i = 1; i <= count; i++)
        {
        	if(localStorage.getItem(i)=="Y"){
        		q_count+=1
        		selected_q_str+=i+","
        	}
        }
		if(q_count>0)
		{
			selected_q_str=selected_q_str.substring(0,selected_q_str.length-1)
			console.log(selected_q_str)
			var form=document.getElementById('selection_form');//retrieve the form as a DOM element
			var input = document.createElement('input');//prepare a new input DOM element
			input.setAttribute('name', 'selected_q_str');//set the param name
			input.setAttribute('value', selected_q_str);//set the value
			input.setAttribute('type', 'text')//set the type, like "hidden" or other
			form.appendChild(input);//append the input to the form
			clearstorage(count)
			form.submit()
			return true
		}else{
			document.getElementById("error_msg").innerHTML="please select question."
			document.getElementById("error_msg").style.color="red";
			return false
		}
	}
	return false
}

function validate(form,name) {
  var x = document.forms[form][name].value;
  if (x == "") {
    	document.getElementById("userNameMsg").innerHTML="User Name is required";
    	document.getElementById("userNameMsg").style.color="red"
    	document.getElementById("userName").style.background="#fdd0d0";
    	
    	setTimeout(function(){document.getElementById("userNameMsg").innerHTML=""},1000);
		setTimeout(function(){document.getElementById("userName").style.background="#fff";},1000);
    	return false;
  }else{
	  return true;
  }
}