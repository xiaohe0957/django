


     function add() {
            num = parseFloat($('.num_show').val());
            $('.num_show').val(num+1);
            $('.num_show').blur();
        }

        function minus() {
            num = parseFloat($('.num_show').val());
            if (num > 0) {
            $('.num_show').val(num-1);
            $('.num_show').blur();
            }

        }

        $(function () {
            $('.num_show').blur(function () {
                num = parseInt($('.num_show').val());
                if (num <= 1){
                    num =1;
                }
                price = parseFloat($('#gprice').text());
                total = num*price;
                $('#num_show').val(num);
                $('#gtotal').text(total.toFixed(2)+'元');

            });




		var $add_y = $('.add_cart').offset().left;
        var $add_x = $('.add_cart').offset().top;
		var $to_x = $('#show_count').offset().top;
		var $to_y = $('#show_count').offset().left;

		$(".add_jump").css({'left':$add_y+80,'top':$add_x+10,'display':'block'})
		$('.add_cart').click(function(){

		    if ($('.login_btn').text().indexOf('登录')>=0){
		        alert('请先登录后再购买');
		        location.href = '/user/login/';
		        return ;
            }
			$(".add_jump").stop().animate({
				'left': $to_y+7,
				'top': $to_x+7},
				"fast", function() {
					$(".add_jump").fadeOut('fast',function(){});
					num =parseInt($('.num_show').val());
					nice = $('#quzhi').text()
					$.get('/cart/add/'+nice+'/'+num+'/',function (data) {
                        $('#show_count').text(data.count);
                    })

			});
		});




           });
