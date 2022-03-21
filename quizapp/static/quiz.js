const url = window.location.href
console.log(url)
const quizBox = document.getElementById('quiz-box')
const scoreBox = document.getElementById('score-box')
const resultBox = document.getElementById('result-box')
const nextButton = document.getElementById('next-btn')
const submitButton = document.getElementById('sbt-btn')

let currentQuestionIndex

currentQuestionIndex = 0
nextButton.addEventListener('click', () => {
    if (return_data.length > currentQuestionIndex + 1) {
        currentQuestionIndex++
        setNextQuestion()
    } else {
        nextButton.style.display = 'none'
        submitButton.style.visibility = "visible"
    }
})

var return_data = function () {
    var data = null;
    $.ajax({
        async: false,
        type : "GET",
        url: `${url}data/`,
        success: function(response) {
            data = response.data;
            const first_question = Object.keys(data[0])[0]
            quizBox.innerHTML = `
                <hr>
                <div class="mb-2">
                    <b>${first_question} Question ${1} from ${data.length}</b>
                </div>
            `
            submitButton.style.visibility = "hidden"
            const answers = Object.values(data[0])[0]
            console.log(answers)
            answers.forEach(answer => {
                quizBox.innerHTML += `
                    <div>
                       <input type="checkbox" class="ans" id="${first_question}-${answer}" name="${first_question}" value="${answer}">
                       <label for "${first_question}">${answer}</label>
                    </div>
                `
            })
            console.log('loading OK')
        }
    });
    return data;
}();

function setNextQuestion(){
    setQuestion(return_data[currentQuestionIndex])
    console.log('setNextQuestion OK')
}

function setQuestion(qstn) {
    const question = Object.keys(qstn)[0]
    quizBox.innerHTML = `
        <hr>
        <div class="mb-2">
            <b>${question} Question ${currentQuestionIndex + 1} from ${return_data.length}</b>
        </div>
    `
    const answers = Object.values(qstn)[0]
    answers.forEach(answer => {
        quizBox.innerHTML += `
            <div>
                <input type="checkbox" class="ans" id="${question}-${answer}" name="${question}" value="${answer}">
                <label for "${question}">${answer}</label>
            </div>
        `
    console.log('OK')
    })
}

//const var_ = Object.values(return_data[0])
//console.log(var_)

const quizControl = document.getElementById('control')
const quizForm = document.getElementById('quiz-form')
const csrf = document.getElementsByName('csrfmiddlewaretoken')
const questionBox = document.getElementById('question-box')

