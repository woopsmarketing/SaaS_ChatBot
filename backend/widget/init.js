// backend/widget/init.js
;(function(){
  const BACKEND = "https://port-0-saas-chatbot-m9r733wy8c5a422f.sel4.cloudtype.app";

  // (1) 이 스크립트 태그 자신을 찾기
  const thisScript = document.currentScript
                   || document.querySelector('script[src*="widget/init.js"]');
  if (!thisScript) {
    console.error("[Chatbot] init.js: script tag not found");
    return;
  }

  // ② URL 객체로 parsing 해서 쿼리스트링에서 꺼내기
  // (2) data-site-key 혹은 query-string에서 site_key 뽑기
  const dataKey = thisScript.getAttribute("data-site-key");
  const queryKey = (new URL(thisScript.src)).searchParams.get("site_key");
  const SITE_KEY = dataKey || queryKey || "";
  console.log("[Chatbot] INIT script src:", thisScript.src);
  console.log("[Chatbot] SITE_KEY resolved to:", SITE_KEY);

  // ③ 전역에 심어두기
  window.__CHATBOT_BACKEND__  = BACKEND;
  window.__CHATBOT_SITE_KEY__ = SITE_KEY;

  // ④ CSS, 아이콘, 컨테이너 … 그대로
  const link = document.createElement("link");
  link.rel = "stylesheet";
  link.href = `${BACKEND}/widget/chatbox.css`;
  document.head.appendChild(link);

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
  widget.querySelector(".chat-toggle")
        .addEventListener("click", ()=> widget.classList.toggle("open"));

  // ⑤ chatbot.js 로드 (이제는 쿼리 안 붙여도 됩니다)
  const script = document.createElement("script");
  script.src = `${BACKEND}/widget/chatbot.js`;
  document.head.appendChild(script);
})();
