;(function(){
  const BACKEND = "https://port-0-saas-chatbot-m9r733wy8c5a422f.sel4.cloudtype.app";
  const SITE_KEY = new URLSearchParams(location.search).get("site_key") || "";

  
  // (1) window 전역에 백엔드 주소 저장
  window.__CHATBOT_BACKEND__ = BACKEND;

  // 1) CSS 로드
  const link = document.createElement("link");
  link.rel = "stylesheet";
  link.href = `${BACKEND}/widget/chatbox.css`;
  document.head.appendChild(link);

  // 2) 위젯 컨테이너 생성
  const widget = document.createElement("div");
  widget.className = "chat-widget";
  widget.innerHTML = `
    <div class="chat-window">
      <div class="messages" id="chat-window"></div>
      <form id="chat-form" class="chat-form">
        <input id="chat-input" class="chat-input"
               placeholder="질문을 입력하세요…" autocomplete="off"/>
        <button type="submit" class="chat-submit">전송</button>
      </form>
    </div>
    <div class="chat-toggle">💬</div>
  `;
  document.body.appendChild(widget);

  // 3) 토글 버튼 이벤트
  widget.querySelector(".chat-toggle")
    .addEventListener("click", ()=> widget.classList.toggle("open"));

  // (5) chatbot.js 로드 (site_key 전달)
  const script = document.createElement("script");
  script.src = `${BACKEND}/widget/chatbot.js?site_key=${SITE_KEY}`;
  document.head.appendChild(script);
})();
