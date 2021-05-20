class BoggleGame {

    constructor(boardId, secs = 60) {
        // define game length, display timer, reset score, make set for storing words, mark game board, 'tick' timer, check word is on board.
        this.secs = secs;
        this.displayTimer();
        this.score = 0;
        this.words = new Set();
        this.board = $('#' + boardId)
        this.timer = setInterval(this.tick.bind(this), 1000); // sets tick to one second intervals
        $('.submit-word', this.board).on('submit', this.handleSubmit.bind(this));
    }

    // display words as li in word ul
    displayWord(word) {
        $('.words', this.board).append($('<li>', { text: word }));
    }

    // display current score
    displayScore() {
        $('.score', this.board).text(this.score);
    }

    // display message (word added, word already in list, invalid word, word not on board)
    displayMessage(msg, cls) {
        $(".msg", this.board)
            .text(msg)
            .removeClass()
            .addClass(`msg ${cls}`);
    }

    // prevent reload on new word submission, if not in list and valid word on board will add to score and display word
    async handleSubmit(e) {
        e.preventDefault();
        const $word = $('.word', this.board);
        let word = $word.val();

        if (!word) return; // not a word
        if (this.words.had(word)) { // word already in list
            this.displayMessage(`${word} has already been found.`, 'err');
            return;
        }

        const res = await axios.get('/check-word', { params: { word: word } });
        if (res.data.result === 'not-word') {
            this.displayMessage(`${word} is not a valid word.`, 'err');
        }
        else if (res.data.result === 'not-on-board') {
            this.displayMessage(`${word} is not on the board.`, 'err');
        }
        else {
            this.displayWord(word);
            this.score += word.length;
            this.displayScore();
            this.words.add(word); // was trying to append, but realized this was a set
            this.displayMessage('${word} had been added to list.', 'ok')
        }
        $word.val('').focus(); // makes sure user is in input again after word is submitted
    }

    displayTimer() { // update timer
        $('.timer', this.board).text(this.secs);
    }
    async tick() { // every second that passes (interval 1000 ms)
        this.secs -= 1;
        this.displayTimer();

        if (this.secs === 0) {
            clearInterval(this.timer);
            await this.scoreGame();
        }
    }
    async scoreGame() {  // after time is up, score and display endgame message
        $('.submit-word', this.board).hide();
        const res = await axios.post('/display-score', { score: this.score });
        if (res.data.brokeRecord) {
            this.displayMessage(`NEW HIGH SCORE: ${this.score}`, 'ok');
        }
        else {
            this.displayMessage(`FINAL SCORE: ${this.score}`, 'ok');
        }
    }
}