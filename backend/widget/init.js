;(function(){
  const BACKEND = "https://port-0-saas-chatbot-m9r733wy8c5a422f.sel4.cloudtype.app";
  const SITE_KEY = new URLSearchParams(location.search).get("site_key") || "";

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

  // 4) 실제 채팅 로직이 담긴 JS 로드 (site_key 전달)
  const script = document.createElement("script");
  script.src = `${BACKEND}/widget/chatbot.js?site_key=${encodeURIComponent(SITE_KEY)}`;
  document.body.appendChild(script);
})();
