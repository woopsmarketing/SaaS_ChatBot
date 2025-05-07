// backend/widget/chatbot.js
console.log("🐞 chatbot.js loaded");

// 즉시 실행 함수 시작
(() => {
  const params = new URLSearchParams(window.location.search);
  const SITE_KEY = params.get("site_key") || "";
  // init.js 에서 심어둔 백엔드 주소 (없으면 "")
  const BACKEND = window.__CHATBOT_BACKEND__ || "";

  // 전역 JS 에러, Promise 미처리 거부 잡기
  window.addEventListener("error", e => {
    console.error("Global JS Error:", e.error || e.message, e);
  });
  window.addEventListener("unhandledrejection", e => {
    console.error("Unhandled Promise Rejection:", e.reason);
  });

  // (이 페이지만의) 로그를 찍어봅니다.
  console.log("▶ SITE_KEY:", SITE_KEY, "BACKEND:", BACKEND);

  function appendMessage(text, sender) {
    const msg = document.createElement("div");
    msg.className = sender === "user" ? "msg user" : "msg bot";
    msg.innerText = text;
    document.getElementById("chat-window").appendChild(msg);
    document.getElementById("chat-window").scrollTop =
      document.getElementById("chat-window").scrollHeight;
  }

  if (window.self === window.top) {
    // ─── “루트 페이지” 에서 수행할 아이콘/iframe 토글 부분 ─────────────────
    // (생략: 기존에 잘 동작하던 그 부분)
  } else {
    // ─── IFRAME 내부 로직 ────────────────────────────────────────────────
    window.addEventListener("DOMContentLoaded", () => {
      const chatForm  = document.getElementById("chat-form");
      const chatInput = document.getElementById("chat-input");

      chatForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const question = chatInput.value.trim();
        if (!question) return;

        // 사용자 메시지 찍기
        appendMessage(question, "user");
        chatInput.value = "";

        // 디버그: 호출 직전 상태를 찍어봅시다.
        console.log("→ Sending to /chat :", { question, site_key: SITE_KEY });
        console.log("→ Full URL:", `${BACKEND}/chat`);

        try {
          const res = await fetch(`${BACKEND}/chat`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question, site_key: SITE_KEY })
          });

          // HTTP 에러 상태를 잡아냅니다.
          if (!res.ok) {
            const text = await res.text();
            console.error("❌ Chat API Error:", res.status, text);
            appendMessage(`Error ${res.status}: ${text}`, "bot");
            return;
          }

          // JSON 파싱 에러도 잡기
          let data;
          try {
            data = await res.json();
          } catch (parseErr) {
            const txt = await res.text();
            console.error("❌ JSON parse failed:", parseErr, "raw:", txt);
            appendMessage("서버 응답 파싱 실패", "bot");
            return;
          }

          console.log("← Response data:", data);
          appendMessage(data.answer, "bot");

        } catch (err) {
          console.error("🔥 Fetch failed:", err);
          appendMessage("네트워크 에러가 발생했습니다.", "bot");
        }
      });
    });
  }
})();
