// table
const container = document.querySelector('.container')

// buttons
const findBtn = document.querySelector('.form__button_type_find')
const resetBtn = document.querySelector('.form__button_type_reset')

// inputs chenges
const intervalToApog = document.querySelector('.input-request_name_apogey')
const intervalInputApog = document.querySelector('.interval_type_apogey')

const intervalToPerig =  document.querySelector('.input-request_name_perigey')
const intervalInputPerig = document.querySelector('.interval_type_perigey')

const intervalToInclin = document.querySelector('.input-request_name_inclin')
const intervalInputInclin = document.querySelector('.interval_type_inclin')

// open table with btn find
function openTable() {
    container.classList.add('container_opened');
    console.log(1);
}

findBtn.addEventListener('click', openTable);

// change inputs intervals
function intervalEqual(elem) {
    elem.classList.add("form__interval_type_equal")
}

function intervalBlur(interval, inpTo) {
    if (inpTo.value === "") {
        interval.classList.remove("form__interval_type_equal")
    }
}

intervalToApog.addEventListener('focus', () => intervalEqual(intervalInputApog))
intervalToApog.addEventListener('blur', () => intervalBlur(intervalInputApog, intervalToApog))

intervalToPerig.addEventListener('focus', () => intervalEqual(intervalInputPerig))
intervalToPerig.addEventListener('blur', () => intervalBlur(intervalInputPerig, intervalToPerig))

intervalToInclin.addEventListener('focus', () => intervalEqual(intervalInputInclin))
intervalToInclin.addEventListener('blur', () => intervalBlur(intervalInputInclin, intervalToInclin))


// click on reset
function deleteEqual() {
    intervalInputApog.classList.remove("form__interval_type_equal")
    intervalInputPerig.classList.remove("form__interval_type_equal")
    intervalInputInclin.classList.remove("form__interval_type_equal")
}

resetBtn.addEventListener('click', deleteEqual)