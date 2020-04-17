$(function(){

	var error_name = false;
	var error_password = false;
	var error_check_password = false;
	var error_email = false;
	var error_check = false;






	$('#id_username').blur(function() {
		check_user_name();
	});

	$('#id_password').blur(function() {
		check_pwd();
	});

	$('#id_password1').blur(function() {
		check_cpwd();
	});

	$('#id_email').blur(function() {
		check_email();
	});

	$('#allow').click(function() {
		if($(this).is(':checked'))
		{
			error_check = false;
			$(this).siblings('span').hide();
		}
		else
		{
			error_check = true;
			$(this).siblings('span').html('请勾选同意');
			$(this).siblings('span').show();
		}
	});


	function check_user_name(){
		var len = $('#id_username').val().length;
		if(len<5||len>20)
		{
			$('#id_username').next().html('请输入5-20个字符的用户名')
			$('#id_username').next().show();
			error_name = true;
		}
		else
		{
			$.get('/user/register_exist/?username='+$('#id_username').val(),function (data) {
				if(data.count==1){
					$('#id_username').next().html('用户名已存在').show();
					error_name = true;
				}
				else{
					$('#id_username').next().hide();
					error_name = false;
				}
			});
		}
	}

	function check_pwd(){
		var len = $('#id_password').val().length;
		if(len<8||len>20)
		{
			$('#id_password').next().html('密码最少8位，最长20位')
			$('#id_password').next().show();
			error_password = true;
		}
		else
		{
			$('#id_password').next().hide();
			error_password = false;
		}
	}


	function check_cpwd(){
		var pass = $('#id_password').val();
		var cpass = $('#id_password1').val();

		if(pass!=cpass)
		{
			$('#id_password1').next().html('两次输入的密码不一致')
			$('#id_password1').next().show();
			error_check_password = true;
		}
		else
		{
			$('#id_password1').next().hide();
			error_check_password = false;
		}

	}

	function check_email(){
		var re = /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;

		if(re.test($('#id_email').val()))
		{
			$('#id_email').next().hide();
			error_email = false;
		}
		else
		{
			$('#id_email').next().html('你输入的邮箱格式不正确')
			$('#id_email').next().show();
			error_check_password = true;
		}

	}


	$('#reg_form').submit(function() {
		check_user_name();
		check_pwd();
		check_cpwd();
		check_email();

		if(error_name == false && error_password == false && error_check_password == false && error_email == false && error_check == false)
		{
			return true;
		}
		else
		{
			return false;
		}

	});








})
