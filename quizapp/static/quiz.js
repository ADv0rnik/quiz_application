const url = window.location.href
console.log(url)
const quizBox = document.getElementById('quiz-box')
const quizForm = document.getElementById('quiz-form')
const scoreBox = document.getElementById('score-box')
const resultBox = document.getElementById('result-box')
const nextButton = document.getElementById('next-btn')
const submitButton = document.getElementById('sbt-btn')
const startButton = document.getElementById('start-btn')
const csrf = document.getElementsByName('csrfmiddlewaretoken')
const timerBox = document.getElementById('timer-box')

let currentQuestionIndex, resp_data

startButton.addEventListener('click', startQuiz)
nextButton.addEventListener('click', () => {
    if (return_data[0].length > currentQuestionIndex + 1) {
        currentQuestionIndex++
        setNextQuestion()
    } else {
        checkAnswers()
        nextButton.style.display = 'none'
        submitButton.style.visibility = "visible"
    }
})

function startQuiz(){
    var timer = null
    startButton.style.display = 'none'
    nextButton.style.visibility  = 'visible'
    currentQuestionIndex = 0
    resp_data = {}
    resp_data['csrfmiddlewaretoken'] = csrf[0].value
    setNextQuestion()
    activateTimer(return_data[2])
}

function activateTimer(time) {
    if (time.toString().length < 2) {
        timerBox.innerHTML = `<b>0${time}:00</b>`
    } else {
        timerBox.innerHTML = `<b>${time}:00</b>`
    }
    let minutes = time - 1
    let seconds = 60
    let displaySeconds
    let displayMinutes

    timer = setInterval(()=>{
        seconds --
        if (seconds < 0) {
            seconds = 59
            minutes --
        }
        if (minutes.toString().length < 2) {
            displayMinutes = '0'+minutes
        } else {
            displayMinutes = minutes
        }
        if(seconds.toString().length < 2) {
            displaySeconds = '0' + seconds
        } else {
            displaySeconds = seconds
        }
        if (minutes === 0 && seconds === 0) {
            timerBox.innerHTML = "<b>00:00</b>"
            setTimeout(()=>{
                clearInterval(timer)
                alert('Time is up')
                sendData()
            }, 500)
        }
        timerBox.innerHTML = `<b>${displayMinutes}:${displaySeconds}</b>`
    }, 1000)
}

function stopTimer(){
    clearInterval(timer)
    timerBox.innerHTML = `<b>${return_data[2]}:00</b>`
}

var return_data = function () {
    var data = [];
    $.ajax({
        async: false,
        type : "GET",
        url: `${url}data/`,
        success: function(response) {
            const data_ = response.data;
            const answ_type = response.type;
            const time = response.time;
            data.push(data_, answ_type, time)
            submitButton.style.visibility = "hidden"
            nextButton.style.visibility = "hidden"
        }
    })
    return data;
};

function setNextQuestion(){
    checkAnswers()
    setQuestion(return_data[0][currentQuestionIndex], return_data[1][currentQuestionIndex])
    console.log('setNextQuestion OK')
}

function setQuestion(qstn, type_of_answer) {
    const question = Object.keys(qstn)
    const answ = type_of_answer
    const answers = Object.values(qstn)[0]
    if(answ == 'input'){
    quizBox.innerHTML = `
        <hr>
        <div class="mb-2">
            <b>${question} Question ${currentQuestionIndex + 1} from ${return_data[0].length}</b><br>
            <input type="text" class="ans" placeholder='Type your answer here' id="${question}" name="${question}">
        </div>
    `
    console.log('OK')
    } else {
    quizBox.innerHTML = `
        <hr>
        <div class="mb-2">
            <b>${question} Question ${currentQuestionIndex + 1} from ${return_data[0].length}</b>
        </div>
    `
    answers.forEach(answer => {
        quizBox.innerHTML += `
            <div>
                <input type="checkbox" class="ans" id="${question}-${answer}" name="${question}" value="${answer}">
                <label for="${question}">${answer}</label>
            </div>
        `
    console.log('OK')
    })
    }
}

function checkAnswers(){
    const elem = [...document.getElementsByClassName('ans')]
    const value_list = [""] // empty storage for multiple answers
    console.log('class fetched')
    console.log(elem)
    console.log(elem.length)
    if (elem.length > 1){
        elem.forEach(el=>{
            if (el.checked) {
                value_list.push(el.value)
            } else {
                if (!resp_data[el.name]) {
                    resp_data[el.name] = null
            }
        }
        resp_data[el.name] = value_list
    })
    } else if (elem.length == 1) {
        resp_data[elem[0].name] = elem[0].value
    }
    console.log(resp_data)
}

const sendData = () => {
    $.ajax({
        type: 'POST',
        url: `${url}save/`,
        data: resp_data,
        success: function(response){
            console.log(response)
            const results = response.results
            quizForm.style.display = 'none'
            submitButton.style.display = 'none'
            nextButton.style.display = "none"

            scoreBox.innerHTML = `
            <hr>
            <div class="container">
                ${response.passed ? 'Congratulations! ' : 'Please, try again '}Your result is ${response.score.toFixed(2)}%
            </div>
            <hr>
            `
            results.forEach(res=>{
                const resDiv = document.createElement("div")
                for (const [question, resp] of Object.entries(res)){
                    resDiv.innerHTML += question
                    const cls = ['container', 'p-3', 'bg-opacity-75', 'text-dark', 'h6']
                    resDiv.classList.add(...cls)
                    if (resp=='missed') {
                        resDiv.innerHTML += '- missed'
                        resDiv.classList.add('bg-danger')
                    }
                    else {
                        const answer = resp['your answer']
                        const correct = resp['correct answer']
                            if (!(answer > correct) && !(answer < correct)){
                                resDiv.classList.add('bg-success')
                                resDiv.innerHTML += ` your answer: ${answer}`
                            } else {
                                resDiv.classList.add('bg-danger')
                                resDiv.innerHTML += ` | correct answer: ${correct}`
                                resDiv.innerHTML += ` | your answer: ${answer}`
                            }
                    }
                }
                resultBox.append(resDiv)
                stopTimer()
            })
        },
        error: function(error){
            console.log(error)
        }
    })
}

submitButton.addEventListener('click', sendData)
