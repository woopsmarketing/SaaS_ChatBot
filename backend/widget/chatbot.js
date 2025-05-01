// backend/widget/chatbot.js
console.log("chatbot.js loaded");

(() => {
  // 쿼리에서 site_key 읽기
  const params = new URLSearchParams(window.location.search);
  const SITE_KEY = params.get("site_key") || "";

  // helper: 메시지 append (iframe 내부용)
  function appendMessage(text, sender) {
    const msg = document.createElement("div");
    msg.className = sender === "user" ? "msg user" : "msg bot";
    msg.innerText = text;
    document.getElementById("chat-window").appendChild(msg);
    document.getElementById("chat-window").scrollTop = 
      document.getElementById("chat-window").scrollHeight;
  }

  // 루트 창인지(≡위젯을 심는 페이지) 판단
  if (window.self === window.top) {
    // ─── OUTER ───────────────────────────────────────────────────────
    // 1) 아이콘 & iframe 스타일 삽입
    const style = document.createElement("style");
    style.textContent = `
      .chat-icon {
        position: fixed;
        bottom: 20px; right: 20px;
        width: 50px; height: 50px;
        background: #007bff; color: #fff;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 24px; cursor: pointer;
        z-index: 99999;
      }
      .chat-iframe-container {
        position: fixed;
        bottom: 80px; right: 20px;
        width: 300px; height: 400px;
        border: none;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        display: none;
        z-index: 99998;
      }
    `;
    document.head.appendChild(style);

    // 2) 채팅 아이콘 추가
    const icon = document.createElement("div");
    icon.className = "chat-icon";
    icon.innerText = "💬";
    document.body.appendChild(icon);

    // 3) iframe 추가 (chatbox.html 로딩, site_key 전달)
    const iframe = document.createElement("iframe");
    iframe.className = "chat-iframe-container";
    iframe.src = `/widget/chatbox.html?site_key=${encodeURIComponent(SITE_KEY)}`;
    document.body.appendChild(iframe);

    // 4) 클릭 시 iframe toggle
    icon.addEventListener("click", () => {
      iframe.style.display = iframe.style.display === "block" ? "none" : "block";
    });
  } else {
    // ─── IFRAME ───────────────────────────────────────────────────────
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
          const res = await fetch("/chat", {
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
