document.addEventListener('DOMContentLoaded', ()=> {
    const form = document.getElementById('itinerary-form');

    form.addEventListener('submit', async(e) => {
        e.preventDefault();

        const formData = new FormData(form);
        const jsonData = Object.fromEntries(formData.entries());

        const response = await fetch('/process-itinerary', {
            method: 'POST',
            headers: {'Content-type': 'application/json'},
            body: JSON.stringify(jsonData)
        });

        if (response.ok) {
            window.location.href = '/success';
        } else {
            alert('Submission failed.');
        }
    });
});