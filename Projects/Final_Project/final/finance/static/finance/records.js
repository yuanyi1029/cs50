document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#record_form').style.display = 'none';
    
    const new_record_button = document.querySelector('#new_record_button');

    new_record_button.addEventListener('click', () => show_record_form())
});

function show_record_form(){
    document.querySelector('#record_form').style.display = 'block';
    document.querySelector('#new_record_button').style.display = 'none';
};

