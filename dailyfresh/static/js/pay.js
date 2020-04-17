function pay(){
    $('body').on('click','#pay',function() {
        // 获取status
        status = $(this).attr('status');
        if (status == "False") {
            // 进行支付
            // 获取订单id
            order_id = $(this).attr('order_id');
            csrf = $('input[name="csrfmiddlewaretoken"]').val();
            // 组织参数
            params = {'order_id': order_id, 'csrfmiddlewaretoken': csrf};
            // 发起ajax post请求，访问/order/pay, 传递参数:order_id
            $.post('/order/alipay', params, function (data) {
                if (data.res == 3) {
                    // 引导用户到支付页面
                    window.open(data.pay_url)
                    $.post('/order/check',params,function (data) {
                        if (data.res == 3){
                            alert('支付成功');
                            // 刷新页面
                            location.reload()
                        }
                        else{
                            alert(data.errmsg)
                        }
                    })
                } else {
                    alert(data.errmsg)
                }
            })
        } else {
            // 其他情况
            alert("异常")
        }
    })
}









// function pay() {
//         // 获取status
//         status = $("#pay").attr('status');
//         if (status == "False") {
//             // 进行支付
//             // 获取订单id
//             order_id = $("#pay").attr('order_id');
//             alert(order_id)
//             csrf = $('input[name="csrfmiddlewaretoken"]').val();
//             // 组织参数
//             params = {'order_id': order_id, 'csrfmiddlewaretoken': csrf};
//             // 发起ajax post请求，访问/order/pay, 传递参数:order_id
//             $.post('/order/alipay', params, function (data) {
//                 if (data.res == 3) {
//                     // 引导用户到支付页面
//                     window.open(data.pay_url)
//                     $.post('/order/check',params,function (data) {
//                         if (data.res == 3){
//                             alert('支付成功')
//                             // 刷新页面
//                             location.reload()
//                         }
//                         else{
//                             alert(data.errmsg)
//                         }
//                     })
//                 } else {
//                     alert(data.errmsg)
//                 }
//             })
//         } else {
//             // 其他情况
//             alert("222222222222222")
//         }
//     }



 // $('#oper_btn').click(function () {
 //        // 获取status
 //        status = $(this).attr('status')
 //        // 获取订单id
 //        order_id = $(this).attr('order_id')
 //        if (status == 1){
 //            // 进行支付
 //            csrf = $('input[name="csrfmiddlewaretoken"]').val()
 //            // 组织参数
 //            params = {'order_id':order_id, 'csrfmiddlewaretoken':csrf}
 //            // 发起ajax post请求，访问/order/pay, 传递参数:order_id
 //            $.post('/order/pay', params, function (data) {
 //                if (data.res == 3){
 //                    // 引导用户到支付页面
 //                    window.open(data.pay_url)
 //                    // 浏览器访问/order/check, 获取支付交易的结果
 //                    // ajax post 传递参数:order_id
 //                    $.post('/order/check', params, function (data){
 //                        if (data.res == 3){
 //                            alert('支付成功')
 //                            // 刷新页面
 //                            location.reload()
 //                        }
 //                        else{
 //                            alert(data.errmsg)
 //                        }
 //                    })
 //                }
 //                else{
 //                    alert(data.errmsg)
 //                }
 //            })
 //        }
 //        else if (status == 4){
 //            // 其他情况
 //            // 跳转到评价页面
 //            location.href = '/order/comment/'+order_id
 //        }
 //    })

