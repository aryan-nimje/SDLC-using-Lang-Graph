const cells = document.querySelectorAll('.cell');
const scoreDisplay = document.getElementById('scoreDisplay');
const message = document.getElementById('message');
const startGameBtn = document.getElementById('startGame');
const newSessionBtn = document.getElementById('newSession');
const player1Input = document.getElementById('player1');
const player2Input = document.getElementById('player2');

let board = ['', '', '', '', '', '', '', '', ''];
let currentPlayer = 'X';
let running = false;
let scores = { X: 0, O: 0 };
let playerNames = { X: 'Player1', O: 'Player2' };

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

function startGame() {
    const p1 = player1Input.value.trim();
    const p2 = player2Input.value.trim();
    if (!p1 || !p2) {
        alert('Please enter names for both players.');
        return;
    }
    playerNames.X = p1;
    playerNames.O = p2;
    scores = { X: 0, O: 0 };
    updateScoreboard();
    resetBoard();
    running = true;
    message.textContent = `${playerNames.X}'s turn (X)`;
    localStorage.setItem('ticTacToeScores', JSON.stringify(scores));
    localStorage.setItem('ticTacToePlayerNames', JSON.stringify(playerNames));
}

function updateScoreboard() {
    scoreDisplay.textContent = `${playerNames.X}: ${scores.X} - ${playerNames.O}: ${scores.O}`;
}

function resetBoard() {
    board = ['', '', '', '', '', '', '', '', ''];
    cells.forEach(cell => {
        cell.textContent = '';
        cell.classList.remove('win');
    });
    currentPlayer = 'X';
}

function checkWinner() {
    let roundWon = false;
    for (let condition of winningConditions) {
        const [a, b, c] = condition;
        if (board[a] && board[a] === board[b] && board[a] === board[c]) {
            roundWon = true;
            cells[a].classList.add('win');
            cells[b].classList.add('win');
            cells[c].classList.add('win');
            break;
        }
    }
    return roundWon;
}

function checkDraw() {
    return board.every(cell => cell !== '');
}

function cellClicked() {
    const index = this.getAttribute('data-index');
    if (board[index] !== '' || !running) return;
    board[index] = currentPlayer;
    this.textContent = currentPlayer;
    if (checkWinner()) {
        message.textContent = `${playerNames[currentPlayer]} (${currentPlayer}) wins!`;
        scores[currentPlayer]++;
        updateScoreboard();
        running = false;
        localStorage.setItem('ticTacToeScores', JSON.stringify(scores));
        return;
    }
    if (checkDraw()) {
        message.textContent = `It's a draw!`;
        running = false;
        return;
    }
    currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
    message.textContent = `${playerNames[currentPlayer]}'s turn (${currentPlayer})`;
}

function newSession() {
    scores = { X: 0, O: 0 };
    updateScoreboard();
    resetBoard();
    message.textContent = 'New session started. Enter player names and start the game.';
    running = false;
    player1Input.value = '';
    player2Input.value = '';
    localStorage.removeItem('ticTacToeScores');
    localStorage.removeItem('ticTacToePlayerNames');
}

function loadFromStorage() {
    const savedScores = localStorage.getItem('ticTacToeScores');
    const savedNames = localStorage.getItem('ticTacToePlayerNames');
    if (savedScores && savedNames) {
        scores = JSON.parse(savedScores);
        playerNames = JSON.parse(savedNames);
        updateScoreboard();
        message.textContent = `Welcome back! ${playerNames.X}'s turn (X)`;
        running = false;
        player1Input.value = playerNames.X;
        player2Input.value = playerNames.O;
    }
}

startGameBtn.addEventListener('click', startGame);
cells.forEach(cell => cell.addEventListener('click', cellClicked));
newSessionBtn.addEventListener('click', newSession);

loadFromStorage();
