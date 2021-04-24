from django.apps import AppConfig


class OrderConfig(AppConfig):
    name = 'orders'
    verbose_name = 'Заказы'

'''

                            let container = document.querySelector("#ajax-service-list")
                            let elem_input = document.querySelector("#ajax-service")
                            for (let k = 0; k<=i; k++) {
                                console.log("let k "+k)
                                let elem = document.querySelector("#service"+k);
                                elem.addEventListener("click", function(e){
                                console.log("elem: "+ e.target.getAttribute("name"));
                                elem_input.value = e.target.getAttribute("name");
                                });
                                }

                            //container.addEventListener('click', ({ target }) => {
                            //    console.log("click: ");
                            //    if (target.nodeName === 'SPAN') {
                            //        console.log("click: ");
                            //        elem_input.value = target.textContent
                            //        }
                            //    })

                            //console.log("response: "+response.is_taken[i]);
                            //console.log("elem: "+elem);


    container.addEventListener('click', ({ target }) => {
                                console.log("click: ");
                                if (target.nodeName === 'SPAN') {
                                    console.log("click: ");
                                    elem_input.value = target.textContent
                                    }
                                })


    <script>
        $(document).ready(function () {
            // catch the form's submit event
            $('#ajax-service').keyup(function () {
                // create an AJAX call
                $.ajax({
                    data: $(this).serialize(), // get the form data
                    url: "{% url 'ajax_request' %}",
                    // on success
                    success: function (response) {
                        console.log(response);
                        if (response.is_exist) {
                            console.log("TYT");
                            let list = ''
                            for (var i in response.is_taken) {
                                list = list + '<span class="badge bg-secondary" name="'+(response.is_taken[i])+'" id="#service'+(i)+'">'+(response.is_taken[i])+'</span> '
                                }
                            //console.log("i: "+i);
                            //let elem_input = document.querySelector("ajax-service")
                            //let elem = document.querySelector("#service"+i);
                            //console.log("response: "+response.is_taken[i]);
                            //console.log("elem: "+elem);
                            $('#ajax-service-list').remove();
                            $('#ajax-service').after('<div id="ajax-service-list" name="ajax-service-list">'+(list)+'</div>')
                        }
                        else {
                            $('#ajax-service-list').remove();
                            $('#ajax-service').after('<div id="ajax-service-list" name="ajax-service-list"><span class="badge rounded-pill bg-warning text-dark" id="ajax-service-list">Нет совпадений</span></div>')

                        }
                    },
                    // on error
                    error: function (response) {
                        // alert the error if any error occured
                        console.log(response.responseJSON.errors)
                    }
                });
                return false;
            });
        })
    </script>
    
    
    <script>
        $(document).ready(function () {
            // catch the form's submit event
            $('#ajax-service').keyup(function () {
                // create an AJAX call
                $.ajax({
                    data: $(this).serialize(), // get the form data
                    url: "{% url 'ajax_request' %}",
                    // on success
                    success: function (response) {
                        if (response.is_exist == true) {
                            let list = ''
                            for (var i in response.is_taken) {
                                list = list + '<span class="badge bg-secondary" name="'+(response.is_taken[i])+'" id="#service'+(i)+'">'+(response.is_taken[i])+'</span> '
                                }
                            //console.log("i: "+i);
                            let elem_input = document.querySelector("ajax-service")
                            let elem = document.querySelector("service"+i);
                            //console.log("response: "+response.is_taken[i]);
                            //console.log("elem: "+elem);
                            $('#ajax-service-list').remove();
                            $('#ajax-service').after('<div id="ajax-service-list" name="ajax-service-list">'+(list)+'</div>')
                        }
                        else {
                             $('#ajax-service-list').remove();
                            $('#ajax-service').after('<div id="ajax-service-list" name="ajax-service-list"><span class="badge rounded-pill bg-warning text-dark" id="ajax-service-list">Нет совпадений</span></div>')
                        }

                    },
                    // on error
                    error: function (response) {
                        // alert the error if any error occured
                        console.log(response.responseJSON.errors)
                    }
                });

                return false;
            });
        })
    </script>
'''