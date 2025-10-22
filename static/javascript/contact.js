class GoogleForm {
    constructor(form, url, successmessage) {
        this.form = form,
        this.url = url,
        this.successmessage = successmessage,
        this.init()
    }
    init() {
        this.form.addEventListener('submit', (e)=>{
            this.handleSubmit(e);
        });
    }
    async handleSubmit(e) {
        e.preventDefault();

        const formData = new FormData();
        
        const selectedType = this.form.querySelector('input[name="feedback-type"]:checked');
        if (selectedType) {
            formData.append('entry.1591633300', selectedType.value);
        }

        formData.append('entry.326955045', this.form.querySelector('input[name="feedback"]').value);

        try {
            await fetch(this.url, {
                method: 'POST',
                mode: 'no-cors',
                body: formData,
            });

            this.form.reset();
            this.form.classList.add('hidden');
            if (this.successmessage) this.successmessage.classList.toggle('hidden');
        } catch (err) {
            console.log(err);
            alert('Something went wrong. Please try again.');
        }
    }
}

document.addEventListener('DOMContentLoaded', ()=> {
    const form = document.getElementById('goog-form');
    const success = document.getElementById('success');
    const googForm = new GoogleForm(form, "https://docs.google.com/forms/u/0/d/e/1FAIpQLSdQ6YZnmyyhUJdcbZrn4dwWA0oz9QVrqF0Us-pR7M58vpgNPQ/formResponse", success);
});