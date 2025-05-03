;(function(){
  console.log("chatbot.js loaded");
  // 1) site_key 읽기
  const SITE_KEY = new URLSearchParams(location.search).get("site_key") || "";

  // 2) DOM 요소 가져오기
  const widget = document.querySelector(".chat-widget");
  const win    = widget.querySelector("#chat-window");
  const form   = widget.querySelector("#chat-form");
  const input  = widget.querySelector("#chat-input");

  // 3) 메시지 출력 헬퍼
  function appendMessage(text, who) {
    const msg = document.createElement("div");
    msg.className = `msg ${who}`;
    msg.innerText = text;
    win.appendChild(msg);
    win.scrollTop = win.scrollHeight;
  }

  // 4) 폼 제출 시 LLM 호출
  form.addEventListener("submit", async e => {
    e.preventDefault();
    const question = input.value.trim();
    if (!question) return;

    appendMessage(question, "user");
    input.value = "";

    try {
      const res = await fetch("/chat/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question, site_key: SITE_KEY })
      });
      const { answer } = await res.json();
      appendMessage(answer, "bot");
    } catch (err) {
      appendMessage("에러가 발생했습니다.", "bot");
      console.error(err);
    }
  });
})();
