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
            check_win(data.core.points)
            if (data.is_level_up) {
                get_boosts()
            }
        }).catch(error => console.log(error))
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
    }).catch(error => console.log(error))
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
        const panel = document.getElementById('boosts-holder')
        panel.innerHTML = ''
        boosts.forEach(boost => {
            add_boost(panel, boost)
        })
    }).catch(error => console.log(error))
}

function add_boost(parent, boost) {
    const button = document.createElement('button')
    button.setAttribute('class', 'boost')
    button.setAttribute('id', `boost_${boost.id}`)
    button.setAttribute('onclick', `buy_boost(${boost.id})`)
    button.innerHTML = `
        <p>Уровень: <span id="boost_level">${boost.level}</span></p>
        <p>+<span id="boost_power">${boost.power}</span></p>
        <p>Цена: <span id="boost_price">${boost.price}</span></p>
    `
    parent.appendChild(button)
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
            alert("Недостаточно денег")
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
    if (points >= 1000000000) {
        /**
        window.location.replace("http://stackoverflow.com");
         **/
        console.log("winner")
    }
}

game_status()
get_boosts()