let {PythonShell} = require('python-shell');

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

async function get_messages(chat_id) {

    let options = {
        mode: 'text',
        scriptPath: 'app_engine/',
        args: ["fetch_chat", chat_id]
    }

    await PythonShell.run('main.py', options, function (err, results) {
        if (err) throw err;
        console.log('Fetched chat data!');
    });

    let button = document.getElementById('send-button')
    button.setAttribute('onclick', 'send_message(' + chat_id + ')')
    let list = document.getElementById('message-window')
    while(list.firstChild) {
        list.removeChild(list.firstChild)
    }

    let messages = JSON.parse(fs.readFileSync('bin/groups/' + chat_id + '/messages/batch.json'))
    for(let x = 0; x < arr_length(messages) && x < 50; x++) {
        var message = document.createElement("li")
        var message_content = document.createElement("div")
        try { 
            message.setAttribute('id', messages[x]['source_guid'])      
        }
        catch {
            console.log(messages[x])
        }
        message.setAttribute('class', 'list-group-item')
        message_content.setAttribute('class', 'message-content')
        
        
        var image = document.createElement("img")
        if(messages[x]['avatar_url'] == null) {
            image.setAttribute('src', 'https://img.adityadiwakar.me/u/7U36.jpg')
        }
        else {
            image.setAttribute('src', messages[x]['avatar_url'])
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