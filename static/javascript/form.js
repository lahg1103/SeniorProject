class FormValidation {
    constructor(form, loader) {
        this.form = form;
        this.loader = loader;
        this.inputs = {
            budget: form.querySelector('input[name="budget"]'),
            arrival: form.querySelector('input[name="arrival_date"]'),
            departure: form.querySelector('input[name="departure_date"]'),
            destination: form.querySelector('input[name="destination"]'),
        };
        this.currentState = 'FORM';
    }

    setState(state) {
        this.currentState = state;
        
        switch(state) {
            case 'FORM':
                this.loader.classList.add('hidden');
                break;

            case 'LOADING':
                this.loader.classList.remove('hidden');
                const loaderLogo = this.loader.querySelector('#loaderlogo');
                if (loaderLogo) loaderLogo.classList.add('spin-logo');
                break;

            case 'ERROR':
                this.loader.classList.add('hidden');
                break;
        }
    }

    clearFieldError(inputElement) {
        const errorElement = inputElement.parentElement.querySelector('.field-error');
        if (errorElement) errorElement.remove();
    }

    showFieldError(inputElement, message) {
        let errorElement = inputElement.parentElement.querySelector('.field-error');
        if (!errorElement) {
            errorElement = document.createElement('div');
            errorElement.className = 'field-error';
            errorElement.style.color = 'var(--accentTwo)';
            inputElement.parentElement.appendChild(errorElement);
        }
        errorElement.textContent = message;
    }

    validateForm() {
        // Object.values(this.inputs).forEach(input => this.clearFieldError(input));
        const { budget, arrival, departure, destination } = this.inputs;
        let isValid = true;
        const errors = [];

        // budget validation
        if ( budget.value && parseFloat(budget.value) <= 0) {
            errors.push({ element: budget, message: 'Budget must be greater than zero. For best results, aim for a budget in the thousands.'});
            isValid = false;

            console.log(`${budget.value} is ${isValid}`);
        }
        else {
            this.clearFieldError(budget);
        }

        // date validation
        let currentDate = new Date();
        currentDate.setHours(0,0,0,0);
        const arrivalDate = new Date(`${arrival.value}T00:00:00`);
        const departureDate = new Date(`${departure.value}T00:00:00`);

        
        if (arrivalDate.getTime() < currentDate.getTime()) {
            errors.push({ element: arrival, message: 'Arrival must be today onwards.'});
            isValid = false;
        }
        else{
            this.clearFieldError(arrival);
        }

        if(arrival.value && departure.value && arrivalDate >= departureDate) {
            errors.push({ element: departure, message: 'Departure must be after arrival.'});
            isValid = false;
        }
        else {
            this.clearFieldError(departure);
        }
        

        // update state.
        if (!isValid) {
            this.setState('ERROR');
            errors.forEach(({ element, message }) => this.showFieldError(element, message));

            console.log(`error found`);
        }

        return isValid;
    }

    listenForChanges() {
        console.log(`listening for changes in form`);
        Object.values(this.inputs).forEach(input => {
            input.addEventListener('change', ()=> {
                const valid = this.validateForm();
                if (valid) this.setState('FORM');
            });
        });
    }
}

// loader
    let textType = function(e, toRotate, period) {
        this.toRotate = toRotate;
        this.e = e;
        this.loop = 0;
        this.period = parseInt(period, 10) || 2000;
        this.text = '';
        this.tick();
        this.isDeleting = false;
    };
    textType.prototype.tick = function(){
        var i = this.loop % this.toRotate.length;
        var fullText = this.toRotate[i];

        if (this.isDeleting) {
            this.text = fullText.substring(0, this.text.length - 1);
        }
        else {
            this.text = fullText.substring(0, this.text.length + 1);
        }

        this.e.textContent = this.text;
        
        let delta = 200 - Math.random() * 100;

        if(this.isDeleting) {
            delta /= 2;
        }
        
        if(!this.isDeleting && this.text === fullText) {
            delta = this.period;
            this.isDeleting = true;
        } else if (this.isDeleting && this.text === '') {
            this.isDeleting = false;
            this.loop++;
            delta = 500;
        }

        setTimeout(()=>{
            this.tick();
        }, delta);
    }

    const optionalFieldVisibility = function(fields, show) {
        for (let f of fields) {
            f.classList.toggle('hidden', !show);
        }
    }


document.addEventListener('DOMContentLoaded', ()=> {
    const form = document.getElementById('itinerary-form');
    const loader = document.getElementById('loader');
    const FormValidator = new FormValidation(form, loader);

    const globalError = document.querySelector('.global-error');

    FormValidator.listenForChanges();
    

    const sliders = document.querySelectorAll('input[type="range"]');
    const totalBudget = document.getElementById('');

    const typewritten = document.getElementsByClassName('typewrite');
    for (let t of typewritten) {
        let toRotate = t.getAttribute('data-type');
        let period = t.getAttribute('data-period');
        if(toRotate) {
            new textType(t, JSON.parse(toRotate), period);
        }
    }
    
    // send stuff to Flask to add to Database
    form.addEventListener('submit', async(e) => {


        e.preventDefault();

        const isValid = FormValidator.validateForm();
        

        if (isValid) {
            FormValidator.setState('LOADING');

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
                FormValidator.setState('FORM');
                globalError.textContent = "There was an error submitting your form.";
                window.scroll({
                top: 0,
                left: 0,
                behavior: "smooth",
            });
            }
        }
        else if (!isValid) {
            globalError.textContent = "There was an error submitting your form. Please revise the highlighted fields, and try again.";
        }
    }); 
});