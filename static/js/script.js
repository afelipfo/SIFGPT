const container_chat = document.getElementById("container-chat");
const container_help = document.getElementById("container-help");
const chat_content = document.getElementById("chat-content");
const input = document.getElementById("input_question");
const loader = document.getElementById("loader");
const plane = document.getElementById("plane");
const textarea = document.getElementById('input_question');

let mediaRecorder;
let audioChunks = [];

textarea.addEventListener('textarea', function() {
    this.style.height = 'auto'; 
    this.style.height = this.scrollHeight + 'px'; 
    if (this.scrollHeight > 50) {
      this.style.height = '50px'; 
    }
  });

document.getElementById("micButton").addEventListener("click", function () {
  if (mediaRecorder && mediaRecorder.state === "recording") {
    mediaRecorder.stop(); // Detener la grabación si ya está en curso
    document.getElementById("micButton").innerHTML =
      '<i class="fas fa-microphone"></i>';
  } else {
    startRecording(); // Iniciar la grabación
    document.getElementById("micButton").innerHTML =
      '<i class="fas fa-stop"></i>';
  }
});

function startRecording() {
  navigator.mediaDevices
    .getUserMedia({ audio: true })
    .then((stream) => {
      mediaRecorder = new MediaRecorder(stream);
      mediaRecorder.start();

      mediaRecorder.ondataavailable = (event) => {
        audioChunks.push(event.data);
      };

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
        audioChunks = [];
        sendAudioToServer(audioBlob);
      };
    })
    .catch((error) => {
      console.error("Error al acceder al micrófono:", error);
    });
}

function sendAudioToServer(audioBlob) {
  const formData = new FormData();
  formData.append("audio", audioBlob, "recording.wav"); // Nombrar el archivo como .wav

  axios
    .post("/process_audio", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    })
    .then((response) => {
      console.log("Respuesta del servidor:", response); // Verificar la respuesta completa en la consola

      const transcription = response.data.transcript;
      console.log("Transcripción recibida:", transcription); // Verificar si la transcripción se está recibiendo

      if (transcription === null) {
        console.error("La transcripción es null.");
      } else {
        document.getElementById("input_question").value = transcription;
      }
    })
    .catch((error) => {
      console.error("Error al enviar el audio:", error);
    });
}

input.addEventListener("keydown", function (event) {
  if (event.key === "Enter" || event.keyCode === 13) {
    event.preventDefault(); // Prevents form submission or page reload
    ask();
  }
});

document
  .getElementById("input_question")
  .addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
      ask(); // Llama a la función ask() para enviar el mensaje
      event.preventDefault(); // Evita que se añada una nueva línea en el input
    }
  });

input.addEventListener("input", function () {
  this.style.height = "auto"; // Restablecer la altura para calcular la nueva altura correcta
  this.style.height = this.scrollHeight + "px"; // Ajustar la altura según el contenido
});

function ask() {
  const userInput = document.getElementById("input_question").value;
  const chatContent = document.getElementById("chat-content");
  const containerChat = document.getElementById("container-chat");
  const loader = document.getElementById("loader");
  const plane = document.getElementById("plane");

  if (userInput.trim() === "") return;

  // Mostrar el contenedor de chat
  containerChat.style.display = "block";

  // Añadir el mensaje del usuario al chat
  chatContent.innerHTML += `<div class="message-user">
        <p>
         ${marked.parse(userInput)}
        </p>
    </div>`;

  // Mostrar el spinner de carga
  loader.classList.remove("d-none");
  plane.classList.add("d-none");

  // Enviar la pregunta al servidor
  axios
    .post("/get_response", { message: userInput })
    .then((response) => {
      // Limpiar triple acento grave si está presente
      let botResponseMarkdown = response.data.response;
      if (
        botResponseMarkdown.startsWith("```") &&
        botResponseMarkdown.endsWith("```")
      ) {
        botResponseMarkdown = botResponseMarkdown.slice(3, -3).trim();
      }

      // Convertir los saltos de línea en <br> o usar <pre> para conservar el formato
      const botResponseHtml = marked.parse(
        botResponseMarkdown.replace(/\n/g, "<br>")
      );

      // Añadir la respuesta del bot al chat con el formato correcto
      chatContent.innerHTML += `
        <section class="message-bot">
            <div class="content-message">
                <img src="https://i.ibb.co/17TbXB8/logo-tunja.png" alt="logo" />
                <pre>${botResponseHtml}</pre>
            </div>
        </section>`;
      // Desplazar hacia abajo el chat
      chatContent.scrollTop = chatContent.scrollHeight;

      // Ocultar el spinner de carga
      loader.classList.add("d-none");
      plane.classList.remove("d-none");
    })
    .catch((error) => {
      console.error("Error al obtener la respuesta:", error);
      loader.classList.add("d-none");
      plane.classList.remove("d-none");
    });

  // Limpiar la entrada del usuario
  document.getElementById("input_question").value = "";
}

function addResponse(data) {
  container_help.style.display = "none";
  container_chat.style.display = "block";
  let html = `<div class="row p-2 d-flex justify-content-end">
        <div class="card text-bg-info border border-0 text-light" style="width: auto;">
            <div class="card-body">
                <p class="card-text">${data}</p>
            </div>
        </div>
    </div>`;
  chat_content.insertAdjacentHTML("beforeend", html);
  container_chat.scrollTop = container_chat.scrollHeight;
}

function addResponseTable(data, id_table) {
  container_help.style.display = "none";
  container_chat.style.display = "block";
  let html = `<div class="row p-2 d-flex justify-content-end">
        <div class="card text-bg-info border border-0 text-light" style="width: auto;">
            <div class="card-body">
                <p class="card-text">${data}</p>
                <a href="/download_table/${id_table}" class="btn btn-secondary btn-sm">Descargar excel <i class="fas fa-download"></i></a>
            </div>
        </div>
    </div>`;
  chat_content.insertAdjacentHTML("beforeend", html);
  container_chat.scrollTop = container_chat.scrollHeight;
}

function addQuestion(question) {
  container_help.style.display = "none";
  container_chat.style.display = "block";
  let html = `<div class="row p-2 d-flex justify-content-start">
        <div class="card text-bg-complement border border-0 text-dark" style="width: auto;">
            <div class="card-body">
                <p class="card-text">${question}</p>
            </div>
        </div>
    </div>`;
  input.value = "";
  chat_content.insertAdjacentHTML("beforeend", html);
  container_chat.scrollTop = container_chat.scrollHeight;
}

function setQuestion(btn) {
  console.log(btn);
  input.value = btn.innerText;
  ask();
}

function startLoader() {
  loader.classList.remove("d-none");
  plane.classList.add("d-none");
}

function stopLoader() {
  loader.classList.add("d-none");
  plane.classList.remove("d-none");
}

function reset() {
  chat_content.innerHTML = "";
  container_help.style.display = "block";
  container_chat.style.display = "none";
}
