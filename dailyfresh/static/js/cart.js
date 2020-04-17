function total(){
    total1= 0;
    total_count = 0;
    $('.col07').each(function () {
        if(unit = $(this).prev().prev().prev().prev().prev().prev().find('input').prop('checked') == true){
        count = $(this).prev().find('input').val();
        price = $(this).prev().prev().text();
        total0 = parseFloat(count)*parseFloat(price);
        $(this).text(total0.toFixed(2));
        total1 +=total0;
        total_count++;
        }

    });
    $('#total').text(total1.toFixed(2));
    $('.total_count1').text(total_count);
}
 function go_order() {
 s = '';
 $(':checked:not(#check_all)').each(function () {
 id = $(this).parents('.cart_list_td').attr('id');

 s = s +'cart_id='+id + '&'

 });

 //删掉最后一个&

 s=s.substring(0,s.length-1);

 location.href = '/order?'+s ;

 }


function cart_del(cart_id){
    del = confirm('确定要删除吗?');
    if(del){
        $.get('/cart/delete/'+cart_id+'/',function (data) {
            if (data.ok == 1){
                $('ul').remove('#'+cart_id);
                total();
            }
        });
    }
}


$(function () {
    total();

    $('#check_all').click(function () {
        state =$(this).prop('checked');
        $(':checkbox:not(#check_all)').prop('checked',state);
                $.get('/cart/check/',function (data) {
            if (data.ok == 1){
                total();
            }
        })
    });
    $(':checkbox:not(#check_all)').click(function () {
        if ($(this).prop('checked')){
            if ($(':checked').length+1 == $(':checkbox').length){
                $('#check_all').prop('checked',true);
            }
        }
        else {
            $('#check_all').prop('checked',false);
        }
        $.get('/cart/check/',function (data) {
            if (data.ok == 1){
                total();
            }
        })
    });
    $('.add').click(function () {
        txt = $(this).prev();
        txt.val(parseFloat(txt.val())+1).blur();
    });
    $('.minus').click(function () {
        txt = $(this).next();
        txt.val(parseFloat(txt.val())-1).blur();
    });

    $('.num_show').blur(function () {
        count = $(this).val();
        if (count<=0){
            alert('请输入正确的数量');
            $(this).focus();
            return;
        }
        else if (count>=100){
            alert('数量不能超过100');
            $(this).focus();
            return;
        }
        cart_id = $(this).parents('.cart_list_td').attr('id');
        $.get('/cart/edit/'+cart_id+'/'+count+'/',function (data) {
            if(data.ok ==0){
                total();
            }else {
                $(this).val(data.ok);
            }
        })
    })
    

});
