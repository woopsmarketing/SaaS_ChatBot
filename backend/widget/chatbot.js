// backend/widget/chatbot.js
console.log("🐞 chatbot.js loaded");

(() => {
  // 1) 전역에서 넘겨받은 백엔드/사이트키 혹은 URL 쿼리
  const BACKEND  = window.__CHATBOT_BACKEND__ || window.location.origin;
  const SITE_KEY = window.__CHATBOT_SITE_KEY__ || new URLSearchParams(location.search).get("site_key") || "";

  console.log("▶ CHATBOT INIT", { BACKEND, SITE_KEY });

  // 2) 전역 에러·Promise 거부 잡기
  window.addEventListener("error", e => {
    console.error("Global JS Error:", e.error || e.message, e);
  });
  window.addEventListener("unhandledrejection", e => {
    console.error("Unhandled Promise Rejection:", e.reason);
  });

  // 3) 메시지 붙이기 헬퍼
  function appendMessage(text, sender) {
    const win = document.getElementById("chat-window");
    const msg = document.createElement("div");
    msg.className = `msg ${sender}`;
    msg.innerText = text;
    win.appendChild(msg);
    win.scrollTop = win.scrollHeight;
  }

  // 4) “루트 페이지” vs “iframe 내부” 분기
  if (window.self === window.top) {
    // (생략) init.js 단계에서 이미 DOM 생성/토글 처리했으므로 아무것도 안 해도 됩니다.
    return;
  }

  // ─── IFRAME 내부 로직 ────────────────────────────────────────────────
  window.addEventListener("DOMContentLoaded", () => {
    const form  = document.getElementById("chat-form");
    const input = document.getElementById("chat-input");

    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const question = input.value.trim();
      if (!question) return;

      appendMessage(question, "user");
      input.value = "";

      // 5) 실제 호출
      const url = `${BACKEND}/chat`;
      console.log("→ POST to Chat API:", url, { question, site_key: SITE_KEY });

      try {
        const res = await fetch(url, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ question, site_key: SITE_KEY })
        });

        // 6) HTTP 에러 처리
        if (!res.ok) {
          const text = await res.text();
          console.error("❌ Chat API Error:", res.status, text);
          appendMessage(`Error ${res.status}: ${text}`, "bot");
          return;
        }

        // 7) JSON 파싱
        let data;
        try {
          data = await res.json();
        } catch (parseErr) {
          const raw = await res.text();
          console.error("❌ JSON parse failed:", parseErr, "raw:", raw);
          appendMessage("서버 응답 파싱 실패", "bot");
          return;
        }

        console.log("← Chat API Response:", data);
        appendMessage(data.answer, "bot");

      } catch (networkErr) {
        console.error("🔥 Fetch failed:", networkErr);
        appendMessage("네트워크 에러가 발생했습니다.", "bot");
      }
    });
  });
})();
