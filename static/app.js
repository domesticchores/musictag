let namebox = document.getElementById("namebox")
let artistbox = document.getElementById("artistbox")
let langbox = document.getElementById("langbox")

let localsongselect = document.getElementById('local-song-select')

let song_template = document.getElementById("template").cloneNode(true)
document.getElementById("template").remove()

function loadContent() {
    document.getElementById("dynamic-area").innerHTML='Loading Results';
    $.ajax({
        url: '/get_songs_list',
        type: 'GET',
        data: { id: namebox.value },
        success: function(response) {
            console.log(response.content)
            if (!response.content) {
                document.getElementById("dynamic-area").innerHTML='No results found :(';
                return 
            } 
            else {
                document.getElementById("dynamic-area").innerHTML='';
            }
            
            for (obj in response.content) {
                console.log(response.content[obj]);
                let temp = song_template.cloneNode(true)
                temp.childNodes[3].innerHTML = response.content[obj]['name']
                temp.childNodes[5].innerHTML = response.content[obj]['artist']
                temp.setAttribute('mbid',response.content[obj]['id'])
                loadCover(temp, response.content[obj]['id'])
                document.getElementById("dynamic-area").appendChild(temp);
            }
            document.getElementById("namebox").value = ''
            document.getElementById("artistbox").value = ''
            document.getElementById("langbox").value = ''
        },
        error: function(error) {
            document.getElementById("dynamic-area").innerHTML='Error fetching dynamic content:', error;
            console.error('Error fetching dynamic content:', error);
        },
        complete: function() {
            // some stuff
        }
    });
}

function loadCover(obj, mbid) {
    $.ajax({
        url: '/get_cover',
        type: 'GET',
        data: { id: mbid },
        success: function(response) {
            console.log(response.content)
            let cover_url = response.content
            obj.childNodes[1].src = cover_url
        },
        error: function(error) {
            console.error('Error fetching dynamic content:', error);
        },
        complete: function() {
            // some stuff
        }
    });
}

function refreshLocalSongs() {
    $.ajax({
        url: '/get_local_songs',
        type: 'GET',
        success: function(response) {
            localsongselect.innerHTML = ''
            console.log(response.content)
            for (obj in response.content) {
                let option = document.createElement('option')
                option.value = response.content[obj]
                option.text = response.content[obj]
                localsongselect.appendChild(option)
            }
        },
        error: function(error) {
            console.error('Error fetching dynamic content:', error);
        },
        complete: function() {
            // some stuff
        }
    });
}