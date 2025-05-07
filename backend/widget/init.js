// backend/widget/init.js
;(function(){
  // 0) 사용자 설정 — 반드시 실제 배포 URL 로 바꿔주세요.
  const BACKEND = "https://port-0-saas-chatbot-m9r733wy8c5a422f.sel4.cloudtype.app";
  const SITE_KEY = new URLSearchParams(location.search).get("site_key") || "";

  // 1) 전역에 백엔드 주소/사이트키 저장 (chatbot.js 에서 사용)
  window.__CHATBOT_BACKEND__ = BACKEND;
  window.__CHATBOT_SITE_KEY__ = SITE_KEY;

  // 2) CSS 로드
  const cssEl = document.createElement("link");
  cssEl.rel  = "stylesheet";
  cssEl.href = `${BACKEND}/widget/chatbox.css`;
  document.head.appendChild(cssEl);

  // 3) 위젯 HTML 삽입
  const widget = document.createElement("div");
  widget.className = "chat-widget";
  widget.innerHTML = `
    <div class="chat-window">
      <div class="messages" id="chat-window"></div>
      <form id="chat-form" class="chat-form">
        <input id="chat-input" class="chat-input"
               placeholder="질문을 입력하세요…" autocomplete="off" />
        <button type="submit" class="chat-submit">전송</button>
      </form>
    </div>
    <div class="chat-toggle">💬</div>
  `;
  document.body.appendChild(widget);

  // 4) 토글 처리는 CSS 클래스 토글만으로
  const toggleBtn = widget.querySelector(".chat-toggle");
  toggleBtn.addEventListener("click", () => {
    widget.classList.toggle("open");
  });

  // 5) chatbot.js 스크립트 로드
  const script = document.createElement("script");
  script.src = `${BACKEND}/widget/chatbot.js?site_key=${SITE_KEY}`;
  script.defer = true;
  document.head.appendChild(script);

  console.log("✅ Chat widget injected:", { BACKEND, SITE_KEY });
})();
