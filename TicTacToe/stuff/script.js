document.addEventListener('DOMContentLoaded', () => {
    const setupDiv = document.getElementById('setup');
    const board = document.getElementById('board');
    const message = document.getElementById('message');
    const startButton = document.getElementById('startGame');
    const playerNameInput = document.getElementById('playerName');
    const cells = Array(9).fill(null);
    let currentPlayer = 'X';
    let playerSymbol = 'X';
    let gameActive = true;
    let playerName = '';

    const winningConditions = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6]
    ];

    const createBoard = () => {
        board.innerHTML = '';
        cells.forEach((_, index) => {
            const cell = document.createElement('div');
            cell.classList.add('cell');
            cell.dataset.index = index;
            cell.addEventListener('click', handleCellClick);
            board.appendChild(cell);
        });
    };

    const handleCellClick = (e) => {
        const index = e.target.dataset.index;
        if (cells[index] || !gameActive) return;
        cells[index] = currentPlayer;
        e.target.textContent = currentPlayer;
        checkWinner();
        currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
        if (gameActive && currentPlayer !== playerSymbol) aiMove();
    };

    const checkWinner = () => {
        let roundWon = false;
        for (let i = 0; i < winningConditions.length; i++) {
            const [a, b, c] = winningConditions[i];
            if (cells[a] && cells[a] === cells[b] && cells[a] === cells[c]) {
                roundWon = true;
                break;
            }
        }

        if (roundWon) {
            gameActive = false;
            message.textContent = `${currentPlayer === playerSymbol ? playerName : 'AI'} hat gewonnen!`;
            highlightWinningCells();
            reloadPage();
            return;
        }

        if (!cells.includes(null)) {
            gameActive = false;
            message.textContent = 'Unentschieden!';
            reloadPage();
            return;
        }
    };

    const highlightWinningCells = () => {
        winningConditions.forEach(condition => {
            const [a, b, c] = condition;
            if (cells[a] && cells[a] === cells[b] && cells[a] === cells[c]) {
                document.querySelector(`.cell[data-index='${a}']`).classList.add('win');
                document.querySelector(`.cell[data-index='${b}']`).classList.add('win');
                document.querySelector(`.cell[data-index='${c}']`).classList.add('win');
            }
        });
    };

    const aiMove = () => {
        let availableCells = cells.map((cell, index) => cell === null ? index : null).filter(val => val !== null);
        let randomIndex = availableCells[Math.floor(Math.random() * availableCells.length)];
        cells[randomIndex] = currentPlayer;
        document.querySelector(`.cell[data-index='${randomIndex}']`).textContent = currentPlayer;
        checkWinner();
        currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
    };

    const reloadPage = () => {
        setTimeout(() => {
            location.reload();
        }, 5000);
    };

    startButton.addEventListener('click', () => {
        playerName = playerNameInput.value.trim();
        playerSymbol = document.querySelector('input[name="playerSymbol"]:checked').value;
        if (playerName === '') {
            alert('Bitte geben Sie einen Spielernamen ein.');
            return;
        }
        currentPlayer = playerSymbol;
        setupDiv.classList.add('hidden');
        board.classList.remove('hidden');
        message.classList.remove('hidden');
        createBoard();
    });
});
