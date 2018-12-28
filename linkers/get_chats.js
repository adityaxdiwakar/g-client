var path = require('path')
let chats = JSON.parse(fs.readFileSync('bin/groups/_group_list.json'))

arr_length = function(array) {
    length = 0
    t_value = 0
    while(true) {
        if(array[t_value] != undefined) {
            length++;
        }
        else {
            break;
        }
        t_value++;
    }
    return length
}

for(let x = 0; x < arr_length(chats); x++) {
    var message = document.createElement("li")
    var message_content = document.createElement("button")
    message.setAttribute('id',chats[x]['id'])
    message.setAttribute('class', 'list-group-item')
    message_content.setAttribute('class', 'message-content btn btn-primary')
    message_content.setAttribute('onclick', 'get_messages(' + chats[x]['id'] + ')')
    
    
    var image = document.createElement("img")
    if(chats[x]['img_url'] == null) {
        image.setAttribute('src', 'https://img.adityadiwakar.me/u/7U36.jpg')
    }
    else {
        image.setAttribute('src', chats[x]['img_url'])
    }
    image.setAttribute('class', 'chat-avatar')


    var text = document.createElement("div")
    text.innerHTML = chats[x]['title']
    text.setAttribute('class', 'chat-text')

    message_content.appendChild(image)
    message_content.appendChild(text)

    message.appendChild(message_content)

    document.getElementById("chat-window").appendChild(message)
}