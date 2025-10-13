const State = {
    FORM: "form",
    LOADING: "loading",
    ERROR: "error"
};

let currentState = State.FORM;


function showFieldError(inputElement, message) {
    let errorElement = inputElement.parentElement.querySelector('.field-error');
    if (!errorElement) {
        errorElement = document.createElement('div');
        errorElement.className = 'field-error';
        errorElement.style.color = 'var(--accent-two)';
        inputElement.parentElement.appendChild(errorElement);
    }
    errorElement.textContent = message;

    console.log(`Adding error at: ${errorElement} with message: ${message}`);
}

function clearFieldError(inputElement) {
    const errorElement = inputElement.parentElement.querySelector('.field-error');
    if (errorElement) errorElement.remove();

    console.log(`clearing field error at: ${errorElement}`);
}


function validateForm(form) {
    const budget = form.querySelector('input[name="budget"]');
    const arrival = form.querySelector('input[name="arrival_date"]');
    const departure = form.querySelector('input[name="departure_date"]');
    const destination = form.querySelector('input[name="destination"]');
    const inputFields = [budget, arrival, departure, destination];
    let errors = [];

    inputFields.forEach(clearFieldError);

    let isValid = true;

    // budget validation
    if (!budget.value || parseFloat(budget.value) <= 0) {
        errors.push({ element: budget, message: "Budget must be greater than zero."});
        isValid = false;

        console.log(`raising field error at budget form validation status: ${isValid}`);
    }

    // date validation
    const arrivalDate = new Date(arrival.value);
    const departureDate = new Date(departure.value);
    if (arrival.value && departure.value && arrivalDate >= departureDate) {
        errors.push({ element: departure, message: "Departure must be after arrival."});
        isValid = false;
        console.log(`raising field error at date form validation status: ${isValid}`);
    
    }

    // add city validation HERE!!!

    return { isValid, errors };
}


function setState(state, form, loader) {
    currentState = state;

    switch (state) {
        case State.FORM:
            loader.classList.add('hidden');
            break;
        case State.LOADING:
            loader.classList.remove('hidden');
            let loaderLogo = loader.querySelector('#loader-logo');
            if (loaderLogo) loaderLogo.classList.add('spin-logo');
            break;
        case State.ERROR:
            loader.classList.remove('hidden');
            elements.forEach(showFieldError(errorMessages));
    }

    if (state === State.ERROR && inputElement) {
        showFieldError;
        loader.classList.add('hidden');
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
    const loadingpage = document.getElementById('loader');
    

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
        
        ['stagger-fade-in', 'hidden'].forEach(c => loadingpage.classList.toggle(c));
        loaderlogo.classList.toggle('spin-logo');

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