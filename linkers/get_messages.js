function get_messages(chat_id) {
    let button = document.getElementById('send-button')
    button.setAttribute('onclick', 'send_message(' + chat_id + ')')
    let list = document.getElementById('message-window')
    while(list.firstChild) {
        list.removeChild(list.firstChild)
    }

    let messages = JSON.parse(fs.readFileSync('bin/groups/' + chat_id + '/messages/batch.json'))
    for(let x = 0; x < 50; x++) {
        var message = document.createElement("li")
        var message_content = document.createElement("div")
        message.setAttribute('id', messages[x]['source_guid'])
        message.setAttribute('class', 'list-group-item')
        message_content.setAttribute('class', 'message-content')
        
        
        var image = document.createElement("img")
        if(fs.existsSync('bin/users/' + messages[x]['sender_id'] + '/avatar.jpeg')) {
            image.setAttribute('src', 'bin/users/' + messages[x]['sender_id'] + '/avatar.jpeg')
        }
        else if(fs.existsSync('bin/users/' + messages[x]['sender_id'] + '/avatar.gif')) {
            image.setAttribute('src', 'bin/users/' + messages[x]['sender_id'] + '/avatar.gif')
        }
        else {
            image.setAttribute('src', 'bin/groups/null/avatar.jpeg')
        }
        image.setAttribute('class', 'avatar')


        var text = document.createElement("div")
        text.innerHTML = messages[x]['name'] + " - " + messages[x]['text']
        text.setAttribute('class', 'message-text')

        message_content.appendChild(image)
        message_content.appendChild(text)

        message.appendChild(message_content)

        document.getElementById("message-window").appendChild(message)
    }
}