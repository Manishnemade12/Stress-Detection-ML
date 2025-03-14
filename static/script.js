function getAdvice() {
    fetch("/get_advice")
    .then(response => response.json())
    .then(data => {
        document.getElementById("result").innerHTML =
            "Emotion: " + data.emotion + "<br>Advice: " + data.advice;
    });
}