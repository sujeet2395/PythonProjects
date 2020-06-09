function val_cnfbx_playing(count)
{
	var is_answered=true;
	for(var i=1; i<=count; i++)
	{
		if(val_input("ans"+i, "ans_err_msg"+i)==false)
		{
			is_answered=false;
		}
	}
	
	if(is_answered==true)
	{
		return true;
	}
	return false;
}

function val_input(ans_id, ans_err_msg_id)
{
	var ans=document.getElementById(ans_id);
	var ans_err_msg=document.getElementById(ans_err_msg_id);
	var is_input=true;
	if(ans.value=="")
	{
		ans_err_msg.innerHTML="Please enter answer.";
		ans.style.background="#fdd0d0";
		is_input=false;
		setTimeout(function(){
			ans_err_msg.innerHTML="";
			ans.style.background="#fff";
		},1000);
	}else{
		ans_err_msg.innerHTML="";
	}
	return is_input;
}