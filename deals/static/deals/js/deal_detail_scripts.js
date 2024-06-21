$(function($){
    //Скрипт для изменения статуса сделки. 

    //Выбираем селектор формы по id changeServiceInDeal
    var changeServiceForm = $("#changeServiceInDeal")
    //Тут же есть окно с Alertom
    var alertForDeal = $("#alertForDeal")
    //Отслеживаем нажатие кнопки submit в форме выбора услуги.
    changeServiceForm.submit(function (e) {
        //Останавливаем поведение по-умолчанию 
        e.preventDefault();
        //Через ajax сериализуем данные в форме и отправляем ожидающей вьюхе
        $.ajax({
            type: this.method,
            url: this.action,
            data: $(this).serialize(),
            dataType: "json",
            success: function (response) {
                //На стороне вьюхи проверяем, все ли ок и отвечаем. Если ответ 200, то
                if(response.status === 200) {
                    //Выбираем селектор области полосы загрузки по id loadChangeServiceBar
                    var loadChangeServiceBarArea = $("#loadChangeServiceBar")
                    //Выбираем саму полосу загрузки
                    var loadChangeServiceBar = $("#loadChangeServiceBar > .progress-bar")
                    //Определяем переменную, содержащую ширину полосы загрузки
                    var loadChangeServiceBar_value = 0
                    //Делаем видимым окно с alert'ом и лобавляем в него текст из ответа от вьюхи
                    alertForDeal.removeClass("d-none").removeClass("alert-danger").addClass("alert-success").text(response.success)
                    //Делаем видимым область с полосой загрузки
                    loadChangeServiceBarArea.removeClass("d-none");
                    //Описываем функцию с увеличением ширины полосы загрузки и добавлением в css width элемента этого значения
                    function loadChangeServiceBar_value_up() {
                        loadChangeServiceBar_value += 40;
                        loadChangeServiceBar.css("width", loadChangeServiceBar_value + "%")
                    }
                    //Вызываем функцию loadChangeServiceBar_value_up первый раз
                    loadChangeServiceBar_value_up()
                    //Устанавливаем интервал вызова этой функции в 300мс, чтобы создать анимацию загрузки.
                    setInterval(loadChangeServiceBar_value_up, 300)
                    //Перезагружаем страницу
                    setTimeout(window.location.reload.bind(window.location), 900)
                //Если получили статус 400, то рендерим окно с alert'ом и текстом ошибки, полученным от вьюхи    
                } else if(response.status === 400) {
                    alertForDeal.removeClass("d-none").addClass("alert-danger").text(response.success)
                }
                
            }
        });
        
    });


    //Отслеживание формы с добавлением растений в запрос стоимости!

    //В модальном окне находится общая форма с формой создания объекта PriceRequest и формсетом PlantForPriceRequestFormset, в этом формсете
    //получаем данные для создания объектов PlantForPriceRequest (растения, входящие в состав заявки).
    //Отслеживаем нажатие кнопки добавления формы в формсет с растениями.
    $("#addPlantFormButton").click(function() {
        //Из формсета имеем на странице скрытые input'ы от management_form, а именно id_form-TOTAL_FORMS, определяем его значение (value) в переменную
        // form_idx, его значение изначально определено в extra в параметрах formset_factory. В данном случа - это 1
        var form_idx = $("#id_form-TOTAL_FORMS").val();
        //Выбираем селектор #plantFormSet - это div, в котором рендерится формсет с растениями. Так же выбираем селектор 
        // выбираем селектор #empty-form (это пустой формсет с __prefix__, вместо counter в input'ах), получаем html всех input'ов из emty-form и 
        // меняем __prefix__ на form_idx
        $("#plantFormSet").append("<tr>" + ($("#empty-form").html().replace(/__prefix__/g, form_idx)) + "</tr>");
        //$("#plantFormSet").append($("#empty-form").html().replace(/__prefix__/g, form_idx));
        // Присваеваем новое value для id_form-TOTAL_FORMS, инкрементируя его на 1
        $("#id_form-TOTAL_FORMS").val(parseInt(form_idx) + 1);
    });

    //Выбираем селектор с формой requestPriceFormFromModal, это form, включающий в себя форму создания объекта RequestPrice и формсет с данными для
    //создания объектов растений.
    var requestPriceFormFromModal = $("#requestPriceFormFromModal")
    //В этой общей form отслеживаем submit
    requestPriceFormFromModal.submit(function (e) { 
        //Прерываем событие по-умолчанию
        e.preventDefault();
        //Через ajax, полученные данные из формы отправляем во вьюху
        $.ajax({
            type: this.method,
            url: this.action,
            data: new FormData(this),
            processData: false,
            contentType: false,
            dataType: "json",
            success: function (response) {
                console.log(response.success);
                console.log(response.redirect_url)
                window.location.href = response.redirect_url
            }
        });
    });




})