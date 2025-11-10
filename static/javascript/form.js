class FormValidation {
    constructor(form, loader) {
        this.form = form;
        this.loader = loader;
        this.inputs = {
            numberOfTravelers: form.querySelector('input[name="number_of_travelers"]'),
            budget: form.querySelector('input[name="budget"]'),
            arrival: form.querySelector('input[name="arrival_date"]'),
            departure: form.querySelector('input[name="departure_date"]'),
            destination: form.querySelector('input[name="destination"]'),
        };
        this.currentState = 'FORM';
    }

    setState(state) {
        this.currentState = state;

        switch (state) {
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
            errorElement.style.color = 'var(--accent-two)';
            inputElement.parentElement.appendChild(errorElement);
        }
        errorElement.textContent = message;
    }

    validateForm() {
        const { numberOfTravelers, budget, arrival, departure, destination } = this.inputs;
        let isValid = true;
        const errors = [];

        // number of travelers validation
        if (!numberOfTravelers.value) {
            errors.push({ element: numberOfTravelers, message: 'Number of travelers is required.' });
            isValid = false;
        }
        else if (numberOfTravelers.value && (parseInt(numberOfTravelers.value) <= 0 || !Number.isInteger(parseFloat(numberOfTravelers.value)))) {
            errors.push({ element: numberOfTravelers, message: 'Number of travelers must be positive.' });
            isValid = false;
        }
        else if (parseInt(numberOfTravelers.value) > 10) {
            errors.push({ element: numberOfTravelers, message: 'Number of travelers cannot exceed 10.' });
            isValid = false;
        }
        else {
            this.clearFieldError(numberOfTravelers);
        }

        // budget validation
        if (budget.value && parseFloat(budget.value) <= 0) {
            errors.push({ element: budget, message: 'Budget must be greater than zero. For best results, aim for a budget in the thousands.' });
            isValid = false;

            console.log(`${budget.value} is ${isValid}`);
        }
        else {
            this.clearFieldError(budget);
        }

        // date validation
        let currentDate = new Date();
        currentDate.setHours(0, 0, 0, 0);
        const arrivalDate = new Date(`${arrival.value}T00:00:00`);
        const departureDate = new Date(`${departure.value}T00:00:00`);
        const oneDay = 24 * 60 * 60 * 1000;


        if (arrivalDate.getTime() < currentDate.getTime()) {
            errors.push({ element: arrival, message: 'Arrival must be today onwards.' });
            isValid = false;
        }
        else {
            this.clearFieldError(arrival);
        }

        if (arrival.value && departure.value && arrivalDate >= departureDate) {
            errors.push({ element: departure, message: 'Departure must be after arrival.' });
            isValid = false;
        }
        else {
            this.clearFieldError(departure);
        }

        if (arrival.value && departure.value && (Math.round((departureDate - arrivalDate) / oneDay) > 7)) {
            console.log(Math.round((departureDate - arrivalDate) / oneDay));
            errors.push({
                element: departure,
                message: 'Trip duration cannot exceed 7 days.',
            });
            isValid = false;
        } else {
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
            input.addEventListener('change', () => {
                const valid = this.validateForm();
                if (valid) this.setState('FORM');
            });
        });
    }
}

// slider
class LinkedSliders {
    constructor(sliders, totalBudget) {
        this.sliders = sliders,
            this.slidersLength = sliders.length,
            this.totalBudgetInput = totalBudget,
            this.totalBudget = parseInt(totalBudget.value) || 1000,

            this.init();
    }

    init() {
        this.updateSliderLimits();
        this.listenForBudget();
        this.listenForSlider();
    }

    updateSliderLimits() {
        const min = Math.floor(this.totalBudget / 8);
        const max = Math.floor(this.slidersLength * Math.floor(this.totalBudget / 8));

        Object.values(this.sliders).forEach(slider => {
            slider.min = min;
            slider.max = max;
            slider.value = min;

            parent = slider.parentNode;

            parent.style.setProperty('--min', slider.min);
            parent.style.setProperty('--max', slider.max);
            parent.style.setProperty('--value', slider.value);
            parent.style.setProperty('--text-value', JSON.stringify((+slider.value).toLocaleString()));
        });

        this.updateTotal();
    }

    listenForBudget() {
        this.totalBudgetInput.addEventListener('change', () => {
            this.totalBudget = parseInt(this.totalBudgetInput.value);
            this.updateSliderLimits();
        });
    }

    listenForSlider() {
        Object.values(this.sliders).forEach(slider => {
            slider.addEventListener('input', () => this.handleSliderInput(slider));
        })
    }

    handleSliderInput(changedSlider) {
        const sliders = Object.values(this.sliders);
        let runningTotal = sliders.reduce((sum, s) => sum + parseInt(s.value), 0);

        changedSlider.parentNode.style.setProperty('--value', changedSlider.value);
        changedSlider.parentNode.style.setProperty('--text-value', JSON.stringify((+changedSlider.value).toLocaleString()));

        if (runningTotal > this.totalBudget) {
            const overflow = runningTotal - this.totalBudget;
            const otherSliders = sliders.filter(s => s !== changedSlider);
            let remaining = overflow;

            for (let slider of otherSliders) {
                if (remaining <= 0) break;

                const available = parseInt(slider.value) - parseInt(slider.min);
                const reduceBy = Math.min(available, Math.ceil(remaining / otherSliders.length));
                slider.value = parseInt(slider.value) - reduceBy;

                slider.parentNode.style.setProperty('--value', slider.value);
                slider.parentNode.style.setProperty('--text-value', JSON.stringify((+slider.value).toLocaleString()));

                remaining -= reduceBy;
            }

            let totalPostReduction = sliders.reduce((sum, s) => sum + parseInt(s.value), 0);
            while (totalPostReduction > this.totalBudget) {
                const target = otherSliders.find(s => parseInt(s.value) > parseInt(s.min));
                if (!target) break;
                target.value = parseInt(target.value) - 1;
                target.parentNode.style.setProperty('--value', target.value);
                target.parentNode.style.setProperty('--text-value', JSON.stringify((+target.value).toLocaleString()));
                totalPostReduction--;
            }
        }

        this.updateTotal();
    }

    updateTotal() {
        const sum = Object.values(this.sliders).reduce((acc, s) => acc + parseInt(s.value), 0);
        const totalElement = document.getElementById('totalAllocated');
        if (totalElement) totalElement.textContent = sum + ' / ' + this.totalBudget;
    }
}

// loader
let textType = function (e, toRotate, period) {
    this.toRotate = toRotate;
    this.e = e;
    this.loop = 0;
    this.period = parseInt(period, 10) || 2000;
    this.text = '';
    this.tick();
    this.isDeleting = false;
};
textType.prototype.tick = function () {
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

    if (this.isDeleting) {
        delta /= 2;
    }

    if (!this.isDeleting && this.text === fullText) {
        delta = this.period;
        this.isDeleting = true;
    } else if (this.isDeleting && this.text === '') {
        this.isDeleting = false;
        this.loop++;
        delta = 500;
    }

    setTimeout(() => {
        this.tick();
    }, delta);
}

const optionalFieldVisibility = function (fields, show) {
    for (let f of fields) {
        f.classList.toggle('hidden', !show);
    }
}

// loader
let pollItineraryStatus = function(itineraryId) {
    fetch(`/itinerary-status/${itineraryId}`).then(r => r.json()).then(data => {
        if ( data.status === "ready" ) {
            window.location.href = `/itinerary/${data.itinerary_id}`;
        } else {
            setTimeout(()=> pollItineraryStatus(itineraryId), 2500);
        }
    })
    .catch(() => setTimeout(() => pollItineraryStatus(itineraryId), 2500));
}


document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('itinerary-form');
    const loader = document.getElementById('loader');
    const FormValidator = new FormValidation(form, loader);

    const globalError = document.querySelector('.global-error');

    FormValidator.listenForChanges();


    const sliders = document.querySelectorAll('input[type="range"]');
    const totalBudget = document.getElementById('budget');

    const LinkSliders = new LinkedSliders(sliders, totalBudget);

    const typewritten = document.getElementsByClassName('typewrite');
    for (let t of typewritten) {
        let toRotate = t.getAttribute('data-type');
        let period = t.getAttribute('data-period');
        if (toRotate) {
            new textType(t, JSON.parse(toRotate), period);
        }
    }

    // send stuff to Flask to add to Database
    form.addEventListener('submit', async (e) => {


        e.preventDefault();

        const isValid = FormValidator.validateForm();


        if (isValid) {
            FormValidator.setState('LOADING');

            const formData = new FormData(form);
            const jsonData = Object.fromEntries(formData.entries());

            try {
                const preferencesResponse = await fetch('/process-itinerary', {
                    method: 'POST',
                    headers: { 'Content-type': 'application/json' },
                    body: JSON.stringify(jsonData)
                });
                if (!preferencesResponse.ok) throw new Error("Failed to save preferences");
                const { itinerary_id } = await preferencesResponse.json();

                const buildResponse = await fetch(`/build-itinerary/${itinerary_id}`);
                if (!buildResponse.ok) throw new Error("Failed to build itinerary");
                
                pollItineraryStatus(itinerary_id);
            }
            catch (err) {
                console.error(err);
                FormValidator.setState('FORM');
                globalError.textContent = "Something went wrong while building your itinerary. Please try again.";
                window.scroll({
                    top: 0,
                    left: 0,
                    behavior: "smooth",
                });
            }
        }
        else if (!isValid) {
            globalError.textContent = "There was an error submitting your form. Please revise the highlighted fields, and try again.";
            return;
        }
    });
});