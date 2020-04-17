
	$(function(){
    $(".sort_bar a").click(function() {
        $(this).siblings().removeClass('active');  // 删除其他兄弟元素的样式
        $(this).addClass('active');                            // 添加当前元素的样式
       });
    });
    $(document).ready(function(){  
        $(".sort_bar a").each(function(){
            $this = $(this);  
            if($this[0].href==String(window.location)){ 
                $(".sort_bar a").addClass("active");
                $this.siblings().removeClass("active");  //active表示被选中效果的类名
            } 
        });  
    }); 

