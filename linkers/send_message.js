let fs = require('fs')
let token = JSON.parse(fs.readFileSync('bin/_main.json')).token
let axios = require('axios')

let input = document.getElementById('message-box')
let button = document.getElementById('send-button')
input.addEventListener('keyup', function(event) {
    event.preventDefault()
    if(event.keyCode === 13) {
        button.click()
    }
})

send_message = function(chat_id) {
    let message = document.getElementById('message-box').value
    document.getElementById('message-box').value = ""
    console.log(chat_id)
    post_message(message, chat_id)
}

post_message = async function(message, chat_id) {
    source_guid = (new Date())*1
    console.log(source_guid)
    config = {
        headers: {
            "Content-Type":"application/json",
            "X-Access-Token":token
        }
    }
    data = {
        "message": {
            "text":message,
            "source_guid":source_guid
        }
    }
    let response = await axios.post('https://api.groupme.com/v3/groups/' + chat_id +'/messages', data, config)
    console.log(response)
}