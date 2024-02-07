let timer;
let totalSeconds = 30 * 60; // 30 minutos em segundos

function startTimer() {
    timer = setInterval(updateTimer, 1000);
    document.getElementById("startBtn").disabled = true;
}

function stopTimer() {
    clearInterval(timer);
    document.getElementById("startBtn").disabled = false;
}

function resetTimer() {
    clearInterval(timer);
    totalSeconds = 30 * 60;
    updateTimerDisplay();
    document.getElementById("startBtn").disabled = false;
}

function updateTimer() {
    if (totalSeconds > 0) {
        totalSeconds--;
        updateTimerDisplay();
    } else {
        clearInterval(timer);
        // Chame sua função após 30 minutos
        alert("Tempo de sessão encerrado!");
        window.location.href = "logout";
    }
}

function updateTimerDisplay() {
    const hours = Math.floor(totalSeconds / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const seconds = totalSeconds % 60;

    const formattedTime = padNumber(hours) + ":" + padNumber(minutes) + ":" + padNumber(seconds);
    document.getElementById("timer").innerText = formattedTime;
}

function padNumber(number) {
    return number < 10 ? "0" + number : number;
}
