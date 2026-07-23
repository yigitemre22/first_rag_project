const sendBtn = document.getElementById("send-btn");
const questionInput = document.getElementById("question");
const chatBox = document.getElementById("chat-box");
const pdfUpload=document.getElementById("pdf-upload");
const newChatBtn = document.getElementById("new-chat")

let selectedDocument=null;

sendBtn.addEventListener("click", sendQuestion);

questionInput.addEventListener("keydown", (e)=>{
    if(e.key==="Enter"){
        sendQuestion();
    }
});

pdfUpload.addEventListener("change",uploadPDF);

window.addEventListener("DOMContentLoaded",loadDocuments)

newChatBtn.addEventListener("click",newChat)

function scrollBottom(){
    chatBox.scrollTop = chatBox.scrollHeight;
}

function addUserMessage(text){

    chatBox.innerHTML += `
    <div class="message user">

        <div class="bubble">
            ${text}
        </div>

        <div class="avatar">
            👤
        </div>

    </div>
    `;

    scrollBottom();
}

function showLoading(){

    chatBox.innerHTML += `
    <div class="message bot" id="loading">

        <div class="avatar">
            🤖
        </div>

        <div class="bubble">

            <div class="typing">

                <span></span>
                <span></span>
                <span></span>

            </div>

        </div>

    </div>
    `;

    scrollBottom();
}

function removeLoading(){

    const loading = document.getElementById("loading");

    if(loading){
        loading.remove();
    }
}

async function typeWriter(element,text){

    element.innerHTML="";

    for(let i=0;i<text.length;i++){

        element.innerHTML += text[i];

        scrollBottom();

        await new Promise(r=>setTimeout(r,10));
    }
}

async function sendQuestion(){

    const question = questionInput.value.trim();

    if(!question) return;

    addUserMessage(question);

    questionInput.value = "";

    sendBtn.disabled = true;
    questionInput.disabled = true;

    showLoading();

    try{
        console.log("Selected document:", selectedDocument);
        console.log("Gönderilen:", selectedDocument);
        const response = await fetch("/chat",{

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({
                question:question,
                filename:selectedDocument
            })

        });

        const data = await response.json();

        removeLoading();

        let sourcesHTML = "";

        if(data.sources && data.sources.length > 0){

            sourcesHTML = `
            <div class="sources">

                <b>📄 Kaynaklar</b>

                <ul>
            `;

            data.sources.forEach(source=>{

                sourcesHTML += `
                <li>

                    ${source.filename}

                    - Sayfa ${source.page}

                </li>
                `;
            });

            sourcesHTML += `
                </ul>

            </div>
            `;
        }

        const id = "bot-" + Date.now();

        chatBox.innerHTML += `
        <div class="message bot">

            <div class="avatar">
                🤖
            </div>

            <div class="bubble">

                <div id="${id}"></div>

                ${sourcesHTML}

            </div>

        </div>
        `;

        await typeWriter(
            document.getElementById(id),
            data.answer
        );

    }
    catch(err){

        removeLoading();

        chatBox.innerHTML += `
        <div class="message bot">

            <div class="avatar">
                🤖
            </div>

            <div class="bubble">

                Beklenmeyen bir hata oluştu.

            </div>

        </div>
        `;

        console.error(err);

    }

    sendBtn.disabled = false;
    questionInput.disabled = false;

    questionInput.focus();

    scrollBottom();
}

async function uploadPDF() {
    console.log("Upload başladı");

    const file=pdfUpload.files[0];

    if(!file) return;

    const formData=new FormData();

    formData.append("file",file)

    const response =await fetch("/upload",{
            method:"POST",
            body:formData
    });

    const data= await response.json();

    alert(`${data.filename} uploaded.`)

    await loadDocuments();
}


async function loadDocuments() {
    const response=await fetch("/documents");

    const data=await response.json();

    const list=document.getElementById("document-list");

    document.getElementById("selected-file").innerText=selectedDocument ? "Selected: "+selectedDocument : "All Documents";

    list.innerHTML= "";

    data.documents.forEach(doc=>{

      list.innerHTML += `
<div
    class="document ${selectedDocument === doc ? "selected" : ""}"
    onclick="selectDocument('${doc}')"
>
    📄 ${doc}
</div>
`;
    });
}

function selectDocument(doc) {

    if(selectedDocument === doc){

        selectedDocument = null;

    }else{

        selectedDocument = doc;

    }

    loadDocuments();
}

async function newChat() {
    
    await fetch("/new-chat",{
        method:"POST"
    });

    selectDocument=null;

    await loadDocuments();
    
    chatBox.innerHTML=`
        <div class="message bot">
            <div class="avatar">
                🤖
            </div>

            <div class="bubble">

                Merhaba 👋<br><br>

                Belgeleriniz hakkında soru sorabilirsiniz.

            </div>

        </div>
    `;
    questionInput.focus();
}