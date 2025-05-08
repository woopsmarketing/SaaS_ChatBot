// ─── chatbot.js ───────────────────────────────────────────────────────
console.log("🐞 chatbot.js loaded");

(() => {
  // 전역에서 꺼낸 값
  const BACKEND  = window.__CHATBOT_BACKEND__  || "";
  const SITE_KEY = window.__CHATBOT_SITE_KEY__ || "";
  console.log("🐞 CHATBOT INIT:", { BACKEND, SITE_KEY });

  function appendMessage(txt, who) {
    const msg = document.createElement("div");
    msg.className = `msg ${who}`;
    msg.innerText = txt;
    const win = document.getElementById("chat-window");
    win.appendChild(msg);
    win.scrollTop = win.scrollHeight;
  }

  window.addEventListener("DOMContentLoaded", () => {
    const chatForm  = document.getElementById("chat-form");
    const chatInput = document.getElementById("chat-input");
    if (!chatForm) return;

    chatForm.addEventListener("submit", async e => {
      e.preventDefault();           // 새로고침 막기
      const question = chatInput.value.trim();
      if (!question) return;

      appendMessage(question, "user");
      chatInput.value = "";

      console.log("→ Sending to /chat", { question, site_key: SITE_KEY });
      try {
        const res = await fetch(`${BACKEND}/chat`, {
          method:  "POST",
          headers: { "Content-Type":"application/json" },
          body:    JSON.stringify({ question, site_key: SITE_KEY })
        });

        if (!res.ok) {
          const txt = await res.text();
          console.error("❌ Chat API Error:", res.status, txt);
          return appendMessage(`Error ${res.status}: ${txt}`, "bot");
        }

        const data = await res.json();
        console.log("← Response data:", data);
        appendMessage(data.answer, "bot");

      } catch(err) {
        console.error("🔥 Fetch failed:", err);
        appendMessage("네트워크 에러가 발생했습니다.", "bot");
      }
    });
  });
})();
