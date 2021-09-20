$(document).ready(function() {
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    console.log("hello")
    $(".add, .subtract, .closebtn").on('click',function(e){
        e.preventDefault()
        console.log("close")
       var element = this
       var product_id =  $(this).parent().data("product-id")
       var action = $(this).data('action')
       if(action == "remove"){
           product_id =  $(this).data("product-id")
       }
       URL  = $(this).data('url')
       
       $.ajax({
           url: URL,
           type : 'GET',
           data: {  
              'csrfmiddlewaretoken' : csrftoken,
              'action':action,
              'product_id': product_id 
           },
           success: function(response){
               $(element).parent().find('.quantity').text(response.quantity)
               
               $(element).parent().parent().find('.quantity_price').text(response.price)
               $('#total_items_price').text(response.totalprice)
               
               if(response.quantity <= 0){
                   
                   $('#'+product_id).remove()
               }
           }

       })
    })

 });













// $(document).ready(function(){
    
//     $('a.add_to_cart').click(function(e){
//         console.log('hello')
//         e.preventDefault()
//         id = $(this).data("id")
//         $.ajax({
//             url: "{% url 'store:addtocart'  %}",
//             type: "GET",
//             data: {"product_id":id},
//             success: function(response){
//                 console.log("succeccfully added")
//             }
//          }
//         )
//     })
  
//  });
