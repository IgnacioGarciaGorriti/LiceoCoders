document.addEventListener('DOMContentLoaded', () => {
    const delBtn = [...document.getElementsByClassName('trash-icon')]
    const csrf_token = document.getElementById('csrf_token')

    console.log(csrf_token)
    delBtn.forEach((btn) => {
        btn.addEventListener('click', async () => {
            deleteBook(btn.dataset.id, csrf_token.value).then(res => location.reload())
        });
    });
});

const deleteBook = (id, csrf_token) => {
    return new Promise((resolve) => {
        const http = new XMLHttpRequest();
        http.open('DELETE', window.location.origin + '/books/delete/' + id)
        http.setRequestHeader("X-CSRFToken", csrf_token);
        http.onreadystatechange = () => {
            console.log('hola')
            console.log(http.status)
            console.log(http.readyState)
            if (http.status === 200 && http.readyState === 4) {
                resolve(http.responseText)
            }
        }
        http.send()
    });
}