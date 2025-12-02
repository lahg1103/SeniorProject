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
let pollItineraryStatus = function (itineraryId) {
    fetch(`/itinerary-status/${itineraryId}`).then(r => r.json()).then(data => {
        if (data.status === "ready") {
            window.location.href = `/itinerary/${data.itinerary_id}`;
        } else {
            setTimeout(() => pollItineraryStatus(itineraryId), 2500);
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

    // creating the multi-step form functionality
    const steps = Array.from(document.querySelectorAll('.form-step'));
    const wizardSteps = Array.from(document.querySelectorAll('.wizard-step'));
    let currentStep = 0;

    // function to move between steps, show a specific step, and hide others to reduce cluttering
    function showStep(index) {
        if (!steps.length)
            return;

        steps.forEach((step, i) => {
            step.hidden = i !== index;
        });

        wizardSteps.forEach((wizardStep, i) => {
            wizardStep.classList.toggle('active', i === index);
            wizardStep.classList.toggle('completed', i < index);
        });
        currentStep = index;

        const lastStepIndex = steps.length - 1;
        if (index === lastStepIndex) {
            updateReviewSection();
        }
    }

    function nextStep() {
        if (currentStep < steps.length - 1) {
            showStep(currentStep + 1);
        }
    }
    function previousStep() {
        if (currentStep > 0) {
            showStep(currentStep - 1);
        }
    }
    // function to update the review section with user inputs
    function updateReviewSection() {
        const reviewContainer = document.querySelector('.review-info');
        if (!reviewContainer || !form) {
            return;
        }
        const getVal = (selector) => {
            const el = form.querySelector(selector);
            return el && el.value ? el.value.trim() : '';
        };
        const getRadioVal = (name) => {
            const checked = form.querySelector(`input[name="${name}"]:checked`);
            return checked ? checked.value : '';
        };

        // first step
        const travelers = getVal('input[name="number_of_travelers"]');
        const budget = getVal('input[name="budget"]');
        // second step
        const destination = getVal('input[name="destination"]');
        const arrival = getVal('input[name="arrival_date"]');
        const departure = getVal('input[name="departure_date"]');
        // third step
        const foodBudget = getVal('input[name="foodBudget"]');
        const lodgingBudget = getVal('input[name="lodgingBudget"]');
        const activitiesBudget = getVal('input[name="activityBudget"]');
        const transportationBudget = getVal('input[name="transportationBudget"]');
        const foodRestriction = getRadioVal('food_restriction');
        const foodRestrictionType = getRadioVal('food_restriction_type');
        const otherFood = getVal('input[name="other_food_restriction"]');

        const formatCurrency = (value) => {
            const num = Number(value);
            if (!num) return '-';
            return num.toLocaleString('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 });
        };

        let foodSummary = 'None';
        // food restrictions summary
        if (foodRestriction === 'yes') {
            if (foodRestrictionType === 'other' && otherFood) {
                foodSummary = `Other - ${otherFood}`;
            }
            else if (foodRestrictionType) {
                let labelText = foodRestrictionType;
                const typeRadioEl = form.querySelector(`input[name="food_restriction_type"][value="${foodRestrictionType}"]`);
                if (typeRadioEl) {
                    const labelEl = typeRadioEl.closest('label');
                    if (labelEl) {
                        labelText = labelEl.textContent.trim();
                    }
                }
                foodSummary = labelText;
            }
            else {
                foodSummary = 'Yes (not specified)';
            }
        }
        // populate review section
        reviewContainer.innerHTML = `
        <p><strong>Number of Travelers:</strong> ${travelers || '-'}</p>
        <p><strong>Budget:</strong> ${formatCurrency(budget)}</p>
        <p><strong>Destination:</strong> ${destination || '-'}</p>
        <p><strong>Dates:</strong> ${arrival || '-'} to ${departure || '-'}</p>

        <p><strong>Budget Allocation:</strong></p>
        <ul class= "review-list">
            <li>Food: ${formatCurrency(foodBudget)}</li>
            <li>Lodging: ${formatCurrency(lodgingBudget)}</li>
            <li>Activities: ${formatCurrency(activitiesBudget)}</li>
            <li>Transportation: ${formatCurrency(transportationBudget)}</li>
        </ul>

        <p><strong>Food Restrictions:</strong> ${foodSummary}</p>
    `;
    }

    // next button, event listeners to guarantee user has filled required fields
    document.querySelectorAll('.wizard-next').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();

            const allFields = steps[currentStep].querySelectorAll("input, textarea, select");

            const fields = [...allFields].filter(input => {
                if (input.hidden) return false;

                const parentHidden = input.closest('[hidden]');
                if (parentHidden) return false;

                return true;
            });

            let filled = [...fields].every(input => {
                if (input.type === 'radio') {
                    const group = form.querySelectorAll(`input[name="${input.name}"]`);
                    return [...group].some(radio => radio.checked);
                }
                return input.value.trim() !== '';
            });
            if (!filled) {
                globalError.textContent = "Please fill in all required fields before proceeding.";
                return;
            }
            nextStep();
        });
    });
    // back buttons
    document.querySelectorAll('.wizard-back').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            previousStep();
        });
    });

    showStep(0);

    // food restriction logic
    const foodRestrictionRadios = document.querySelectorAll('input[name="food_restriction"]');
    const foodDetailsWrapper = document.getElementById('food_restriction_details');
    const foodTypeRadios = document.querySelectorAll('input[name="food_restriction_type"]');
    const otherFoodWrapper = document.getElementById('other_food_restriction_wrapper');
    const otherFoodInput = document.getElementById('other_food_restriction');
    // function to sync food restriction details visibility
    function syncFoodRestrictionDetails() {
        if (!foodDetailsWrapper || !foodRestrictionRadios.length || !foodTypeRadios.length || !otherFoodWrapper) {
            return;
        }
        const checkedRestriction = document.querySelector('input[name="food_restriction"]:checked');
        const hasRestriction = checkedRestriction && checkedRestriction.value === 'yes';

        foodDetailsWrapper.hidden = !hasRestriction;

        if (!hasRestriction) {
            foodTypeRadios.forEach(radio => radio.checked = false);
            otherFoodWrapper.hidden = true;
            if (otherFoodInput) otherFoodInput.value = '';
            return;
        }

        const checkedType = document.querySelector('input[name="food_restriction_type"]:checked');
        const isOther = checkedType && checkedType.value === 'other';

        otherFoodWrapper.hidden = !isOther;
        if (!isOther && otherFoodInput) {
            otherFoodInput.value = '';
        }
    }
    foodRestrictionRadios.forEach(radio => {
        radio.addEventListener('change', syncFoodRestrictionDetails);
    });
    foodTypeRadios.forEach(radio => {
        radio.addEventListener('change', syncFoodRestrictionDetails);
    });
    syncFoodRestrictionDetails();

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