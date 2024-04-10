function call_click() {
    fetch('api/click', {
        method: 'GET'
    }).then(response => {
        if (response.ok) {
            return response.json()
        }

        return Promise.reject(response)
        }).then(data => {
            document.getElementById('points').innerText = data.core.points
            document.getElementById('click-power').innerText = data.core.click_power
            let img = document.getElementById('hardbass-img')
            img.setAttribute('src', data.core.frame_url)
            check_win(data.core.points)
            if (data.is_level_up) {
                get_boosts()
            }
        }).catch(error => console.log(error))
    update_boosts_status()
    rewindGif()
}

function rewindGif() {
}

function game_status() {
    fetch('api/get_core', {
        method: 'GET'
    }).then(response => {
        if (response.ok) {
            return response.json()
        }
        return Promise.reject(response)
    }).then(data => {
        document.getElementById('points').innerText = data.core.points
        document.getElementById('click-power').innerText = data.core.click_power
        check_win(data.core.points)
        update_boosts_status()
    }).catch(error => console.log(error))
}

function update_boosts_status() {
    const money = Number(document.getElementById('points').innerText)
    const boosts = document.getElementsByClassName('boost-container');
    for (var i = 0; i < boosts.length; i++) {
        let boost = boosts[i]
        let price = Number(boost.querySelector('#boost_price').innerText)
        if (price <= money) {
            boost.classList.remove('inactive')
        } else {
            boost.classList.add('inactive')
        }
    }
}

function get_boosts() {
    fetch('api/boosts/list/', {
        method: 'GET'
    }).then(response => {
        if (response.ok) {
            return response.json()
        }
        return Promise.reject(response)
    }).then(boosts => {
        const panel = document.getElementById('boost-holder')
        panel.innerHTML = ''
        boosts.forEach(boost => {
            add_boost(panel, boost)
        })
        update_boosts_status()
    }).catch(error => console.log(error))
}

function add_boost(parent, boost) {
    const container = document.createElement('div')
    container.setAttribute('class', 'boost-container')
    container.setAttribute('id', `boost_${boost.id}`)
    container.innerHTML = `
        <img src="${boost.img_rel_url}" class="boost-image">
        <span class="boost-name" id="boost_name">${boost.name}</span>
        <p class="boost-level">Уровень: <span id="boost_level">${boost.level}</span></p>
        <p class="boost-power">+<span id="boost_power">${boost.power}</span></p>
        <p class="boost-price">Цена: <span id="boost_price">${boost.price}</span></p>
        <button class="boost-buy-button" onclick="buy_boost(${boost.id})"><p>Купить</p></button>
    `
    parent.appendChild(container)
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/** Функция покупки буста */
function buy_boost(boost_id) {
    const csrftoken = getCookie('csrftoken') // Забираем токен из кукесов

    fetch(`api/boosts/buy/${boost_id}/`, {
        method: 'PUT', // Теперь метод POST, потому что мы изменяем данные в базе
        headers: { // Headers - мета-данные запроса
            "X-CSRFToken": csrftoken, // Токен для защиты от CSRF-атак, без него не будет работать
            'Content-Type': 'application/json'
        }
    }).then(response => {
        if (response.ok) return response.json()
        else return Promise.reject(response)
    }).then(response => {
        if (response.error) return
        if (!response.is_bought) {
            return
        }
        const old_boost_stats = response.old_stats
        const new_boost_stats = response.new_stats
        console.log(old_boost_stats.price)

        const coinsElement = document.getElementById('points')
        coinsElement.innerText = Number(coinsElement.innerText) - old_boost_stats.price
        const powerElement = document.getElementById('click-power')
        powerElement.innerText = Number(powerElement.innerText) + old_boost_stats.power

        update_boost(new_boost_stats) // Обновляем буст на фронтике
        update_boosts_status()
    }).catch(err => console.log(err))
}

/** Функция для обновления буста на фронтике */
function update_boost(boost) {
    const boost_node = document.getElementById(`boost_${boost.id}`)
    boost_node.querySelector('#boost_level').innerText = boost.level
    boost_node.querySelector('#boost_power').innerText = boost.power
    boost_node.querySelector('#boost_price').innerText = boost.price
}

function check_win(points){
    if (points >= 1000000) {
        window.location.replace("https://www.youtube.com/watch?v=SD7TJF452zs");
        console.log("winner")
    }
}

game_status()
get_boosts()