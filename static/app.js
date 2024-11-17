(async () => {
            
    let game_id = null
    let playerInterval = null
    let gameInterval = null

    const $searchSection = document.querySelector('#search-game')
    const $gameSection = document.querySelector('#game')

    const searchGame = async () => {
        const r = await fetch(`/search/${user_id}`)
        const response = await r.json()

        console.log('search', response)


        playerInfoLoop()

    }

    const playerInfoLoop = async () => {

        clearInterval(playerInterval)
        playerInterval = setInterval( async() => {
            const r = await fetch(`/player/${user_id}`)
            const response = await r.json()

            console.log('player', response)

            game_id = response.game_id
            
            if (game_id) {
                enableGame()
                gameInfoLoop();
                clearInterval(playerInterval)
            }
        }, 1000)

    }


    const gameInfoLoop = async () => {


        clearInterval(gameInterval)
        gameInterval = setInterval( async () => {
            const r = await fetch(`/game/${game_id}/by/${user_id}`)
            const response = await r.json()

            drawGame(response)

            if (response.status == "finished") {
                game_id = null
                enableSearchGame()
                clearInterval(playerInterval)
                clearInterval(gameInterval)
            }

        }, 1000)

    }

    const buyCard = async () => {
        const r = await fetch(`/game/${game_id}/by/${user_id}/buy-card`)
        const response = await r.json()
    }

    const drawGame = (gameInfo) => {

        const $playerCards = document.querySelector('#player-cards')
        const $enemyCards = document.querySelector('#enemy-cards')
        const $turnCounter = document.querySelector('#turn-counter')
        const $scoreboard = document.querySelector('#scoreboard')

        let player_cards_html = ''
        for(let card of gameInfo.player.hand_cards) {
            player_cards_html += `
                <div class="card">${card}</div>
            `
        }  

        let enemy_cards_html = ''
        for(let card of gameInfo.enemy.hand_cards) {
            enemy_cards_html += `
                <div class="card">${card}</div>
            `
        }  



        $turnCounter.innerHTML = gameInfo.turn_counter
        $scoreboard.innerHTML = `${gameInfo.scoreboard[0]} / ${gameInfo.scoreboard[1]}`

        $playerCards.innerHTML = player_cards_html
        $enemyCards.innerHTML = enemy_cards_html

    }

    const enableSearchGame = () => {
        $gameSection.classList.remove('running')
        $searchSection.classList.remove('game_found')
    }

    const enableGame = () => {
        $gameSection.classList.add('running')
        $searchSection.classList.add('game_found')
    }

    document.querySelector('#searchGame').addEventListener('click', (ev) => {
        searchGame();
    })

    document.querySelector('#buyCard').addEventListener('click', (ev) => {
        buyCard();
    })

})()