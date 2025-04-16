document.addEventListener("DOMContentLoaded", function() {
    const recordBtn = document.getElementById("record");
    const stopBtn = document.getElementById("stop");
    const timer = document.getElementById("timer");
    const audioEl = document.getElementById("audio");
    const form = document.getElementById("qaForm");
  
    let mediaRecorder, chunks = [], timerInterval;
  
    recordBtn.addEventListener("click", async () => {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorder = new MediaRecorder(stream);
      chunks = [];
  
      mediaRecorder.ondataavailable = e => chunks.push(e.data);
  
      mediaRecorder.onstop = () => {
        const blob = new Blob(chunks, { type: "audio/wav" });
        const file = new File([blob], "question.wav");
  
        const dt = new DataTransfer();
        dt.items.add(file);
        const fileInput = document.createElement("input");
        fileInput.type = "file";
        fileInput.name = "audio_data";
        fileInput.files = dt.files;
        fileInput.hidden = true;
        form.appendChild(fileInput);
  
        const audioURL = URL.createObjectURL(blob);
        audioEl.src = audioURL;
        audioEl.style.display = "block";
      };
  
      mediaRecorder.start();
  
      let seconds = 0;
      timerInterval = setInterval(() => {
        seconds++;
        timer.textContent = `${String(Math.floor(seconds / 60)).padStart(2, '0')}:${String(seconds % 60).padStart(2, '0')}`;
      }, 1000);
  
      recordBtn.disabled = true;
      stopBtn.disabled = false;
    });
  
    stopBtn.addEventListener("click", () => {
      mediaRecorder.stop();
      clearInterval(timerInterval);
      timer.textContent = "00:00";
      recordBtn.disabled = false;
      stopBtn.disabled = true;
    });
  });