// backend/widget/init.js
;(function(){
  const BACKEND = "https://port-0-saas-chatbot-m9r733wy8c5a422f.sel4.cloudtype.app";
  const SITE_KEY = new URLSearchParams(location.search).get("site_key") || "";

  // 1) CSS 로드
  const css = document.createElement("link");
  css.rel = "stylesheet";
  css.href = `${BACKEND}/widget/chatbox.css`;
  document.head.appendChild(css);

  // 2) 아이콘 생성
  const icon = document.createElement("div");
  icon.id = "chat-icon";
  Object.assign(icon.style, {
    position: "fixed",
    bottom: "20px",
    right: "20px",
    width: "50px",
    height: "50px",
    borderRadius: "50%",
    background: "#007bff",
    color: "#fff",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    cursor: "pointer",
    zIndex: 10000,
  });
  icon.innerText = "💬";
  document.body.appendChild(icon);

  // 3) 채팅창 컨테이너 생성 (초기 숨김)
  const container = document.createElement("div");
  container.id = "chat-container";
  Object.assign(container.style, {
    position: "fixed",
    bottom: "90px",
    right: "20px",
    width: "300px",
    height: "400px",
    boxShadow: "0 0 10px rgba(0,0,0,0.2)",
    borderRadius: "8px",
    background: "#fff",
    display: "none",
    flexDirection: "column",
    zIndex: 9999,
  });
  container.innerHTML = `
    <div id="chat-window" style="flex:1; overflow:auto; padding:8px;"></div>
    <form id="chat-form" style="display:flex; border-top:1px solid #ddd;">
      <input id="chat-input" style="flex:1; padding:8px; border:none; outline:none;" placeholder="질문을 입력하세요…" />
      <button type="submit" style="padding:8px;">전송</button>
    </form>
  `;
  document.body.appendChild(container);

  // 4) 아이콘 클릭 → 채팅창 토글
  icon.addEventListener("click", ()=>{
    container.style.display = container.style.display === "none" ? "flex" : "none";
  });

  // 5) chatbot.js 로드 (site_key 전달)
  const script = document.createElement("script");
  script.src = `${BACKEND}/widget/chatbot.js?site_key=${SITE_KEY}`;
  document.head.appendChild(script);
})();