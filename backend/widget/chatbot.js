console.log("🐞 chatbot.js loaded");

(() => {
  const params = new URLSearchParams(window.location.search);
  const SITE_KEY = params.get("site_key") || "";
  const BACKEND = window.__CHATBOT_BACKEND__ || "";

  // 전역 에러 로깅
  window.addEventListener("error", e => {
    console.error("Global JS Error:", e.error || e.message, e);
  });
  window.addEventListener("unhandledrejection", e => {
    console.error("Unhandled Promise Rejection:", e.reason);
  });

  console.log("▶ CHATBOT INIT:", { BACKEND, SITE_KEY });

  // 메시지 추가 헬퍼
  function appendMessage(text, sender) {
    const msg = document.createElement("div");
    msg.className = sender === "user" ? "msg user" : "msg bot";
    msg.innerText = text;
    const win = document.getElementById("chat-window");
    win.appendChild(msg);
    win.scrollTop = win.scrollHeight;
  }

  // ─── 토글(최상위 페이지) ─────────────────────────────────
  if (window.self === window.top) {
    // (여기에 기존의 아이콘/iframe 토글 코드를 두시면 됩니다)
  }

  // ─── 폼 이벤트(루트든 iframe 안이든 무조건!) ─────────────────
  window.addEventListener("DOMContentLoaded", () => {
    const chatForm  = document.getElementById("chat-form");
    const chatInput = document.getElementById("chat-input");
    if (!chatForm || !chatInput) return;  // 위젯이 안 들어온 페이지라면 아무 것도 안 함

    chatForm.addEventListener("submit", async (e) => {
      e.preventDefault();  // ★ 페이지 리로드 방지
      const question = chatInput.value.trim();
      if (!question) return;

      appendMessage(question, "user");
      chatInput.value = "";

      console.log("→ Sending to /chat", { question, site_key: SITE_KEY });
      try {
        const res = await fetch(`${BACKEND}/chat`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ question, site_key: SITE_KEY })
        });
        if (!res.ok) {
          const text = await res.text();
          console.error("❌ Chat API Error:", res.status, text);
          appendMessage(`Error ${res.status}: ${text}`, "bot");
          return;
        }
        const data = await res.json();
        console.log("← Response data:", data);
        appendMessage(data.answer, "bot");

      } catch (err) {
        console.error("🔥 Fetch failed:", err);
        appendMessage("네트워크 에러가 발생했습니다.", "bot");
      }
    });
  });
})();
