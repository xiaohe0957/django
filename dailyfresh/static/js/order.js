$(function () {

    total1= 0;
    total_count = 0;
    $('.col07').each(function () {

        count=$(this).prev().text();
        price = $(this).prev().prev().text();
        total0 = parseFloat(count)*parseFloat(price);
        $(this).text(total0.toFixed(2));



    });

});

function go() {


		$('#order_btn').click(function() {
            // 获取用户选择的地址id, 支付方式, 要购买的商品id字符串

            sku_ids = $(this).attr('cart_id')
            csrf = $('input[name="csrfmiddlewaretoken"]').val()
            // alert(addr_id+":"+pay_method+':'+sku_ids)
            // 组织参数
            params = {  'sku_ids':sku_ids,
                        'csrfmiddlewaretoken':csrf}
            // 发起ajax post请求，访问/order/commit, 传递的参数: addr_id pay_method, sku_ids
            $.post('/order/handle/', params, function (data) {
                if (data.res == 5){
                    // 创建成功
                    localStorage.setItem('order_finish',2);
                    $('.popup_con').fadeIn('fast', function() {

                        setTimeout(function(){
                            $('.popup_con').fadeOut('fast',function(){
                                 window.location.href = '/order/pay/1';
                            });
                        },3000)
                    });
                }
                else{
                    alert(data.errmsg)
                }
            })



		}
		);
}