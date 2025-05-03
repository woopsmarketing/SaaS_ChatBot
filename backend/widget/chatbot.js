// backend/widget/chatbot.js
console.log("chatbot.js loaded");

(() => {
  const params = new URLSearchParams(window.location.search);
  const SITE_KEY = params.get("site_key") || "";

  // (A) init.js 에서 심어둔 백엔드 주소 읽기
  const BACKEND = window.__CHATBOT_BACKEND__ || "";

  // 메시지 append 헬퍼 (iframe 내부)
  function appendMessage(text, sender) {
    const msg = document.createElement("div");
    msg.className = sender === "user" ? "msg user" : "msg bot";
    msg.innerText = text;
    document.getElementById("chat-window").appendChild(msg);
    document.getElementById("chat-window").scrollTop =
      document.getElementById("chat-window").scrollHeight;
  }

  if (window.self === window.top) {
    // … (아이콘, iframe 토글 부분 그대로) …

  } else {
    // ─── IFRAME 내부 로직 ───────────────────────────────────────────
    window.addEventListener("DOMContentLoaded", () => {
      const chatForm  = document.getElementById("chat-form");
      const chatInput = document.getElementById("chat-input");

      chatForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const question = chatInput.value.trim();
        if (!question) return;

        appendMessage(question, "user");
        chatInput.value = "";

        try {
          // ★ 여기만 변경: /chat 이 아니라 백엔드 전체 URL로!
          const res = await fetch(`${BACKEND}/chat`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question, site_key: SITE_KEY })
          });
          const data = await res.json();
          appendMessage(data.answer, "bot");
        } catch (err) {
          appendMessage("에러가 발생했습니다.", "bot");
          console.error(err);
        }
      });
    });
  }
})();
