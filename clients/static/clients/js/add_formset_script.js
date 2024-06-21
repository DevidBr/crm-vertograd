        document.getElementById('add-contact-person').addEventListener('click', function(e) {
        e.preventDefault();

        var contactPersonFormset = document.getElementById('contact-person-formset');
        var newForm = contactPersonFormset.getElementsByClassName('contact-person-form')[0].cloneNode(true);
        var formRegex = RegExp(/\{\{ formset\.(\d+)\.id }\}/, 'g')

        formRegex.lastIndex = 0;
        var newFormHTML = newForm.innerHTML.replace(formRegex, function() {
            return '{{ formset.' + (formRegex.lastIndex++) + '.id }}';
        });

        newForm.innerHTML = newFormHTML;
        contactPersonFormset.appendChild(newForm);
    });




        document.getElementById('remove-contact-person').addEventListener('click', function(e) {
        e.preventDefault();

        var contactPersonFormset = document.getElementById('contact-person-formset');
        var forms = contactPersonFormset.getElementsByClassName('contact-person-form');

        if (forms.length > 1) {
            forms[forms.length - 1].remove();
        }
    });