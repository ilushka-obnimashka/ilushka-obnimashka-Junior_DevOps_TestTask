(() => {
  const root = document.getElementById("jobmatch");
  if (!root) return;
  const theme = root.querySelector("#theme");
  const setTheme = (value) => {
    root.dataset.theme = value;
    const label = value === "dark" ? "Светлая тема" : "Тёмная тема";
    theme.querySelector("span").textContent = label;
    theme.setAttribute("aria-label", `Включить ${value === "dark" ? "светлую" : "тёмную"} тему`);
  };
  try {
    setTheme(localStorage.getItem("jobmatch-theme") === "light" ? "light" : "dark");
  } catch {
    setTheme("dark");
  }
  theme.addEventListener("click", () => {
    const value = root.dataset.theme === "dark" ? "light" : "dark";
    setTheme(value);
    try {
      localStorage.setItem("jobmatch-theme", value);
    } catch {
      /* Optional preference. */
    }
  });
  const card = root.querySelector("#candidate");
  if (!card) return;
  const accept = root.querySelector("#accept");
  const info = root.querySelector("#info");
  const rewind = root.querySelector("#rewind");
  const about = root.querySelector("#about-panel");
  const match = root.querySelector("#match-panel");
  const actions = root.querySelector("#card-actions");
  const hint = root.querySelector("#deck-hint");
  const toastArea = root.querySelector("#toast-area");
  let pending = false;
  let matched = false;
  let start = null;
  let swipeX = 0;
  let toastTimer;
  function toast(message) {
    clearTimeout(toastTimer);
    toastArea.replaceChildren();
    const box = document.createElement("div");
    box.className = "toast";
    const text = document.createElement("span");
    text.textContent = message;
    const close = document.createElement("button");
    close.textContent = "×";
    close.setAttribute("aria-label", "Закрыть уведомление");
    close.addEventListener("click", () => box.remove());
    box.append(text, close);
    toastArea.append(box);
    toastTimer = setTimeout(() => box.remove(), 6500);
  }
  const notificationButton = root.querySelector("#notification");
  let notificationPending = false;
  notificationButton.addEventListener("click", async () => {
    if (notificationPending) return;
    notificationPending = true;
    notificationButton.disabled = true;
    notificationButton.setAttribute("aria-busy", "true");
    notificationButton.textContent = "Придумываю подкат…";
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 90000);
    try {
      const response = await fetch("/api/notification/", {
        signal: controller.signal,
        cache: "no-store",
      });
      if (!response.ok) throw new Error("Notification request failed");
      const data = await response.json();
      if (typeof data.message !== "string" || !data.message.trim()) {
        throw new Error("Invalid notification response");
      }
      toast(data.message);
    } catch {
      toast("Подкат застрял по дороге. Попробуй ещё раз — сервер не ответил корректно.");
    } finally {
      clearTimeout(timeout);
      notificationPending = false;
      notificationButton.disabled = false;
      notificationButton.removeAttribute("aria-busy");
      notificationButton.textContent = "Подкат от DevOps ✦";
    }
  });
  function showAbout(show) {
    about.hidden = !show;
    info.setAttribute("aria-expanded", String(show));
    info.setAttribute("aria-label", show ? "Вернуться к фото" : "Обо мне");
  }
  function resetDrag() {
    start = null;
    swipeX = 0;
    card.classList.remove("dragging");
    card.style.transform = "";
    card.querySelector(".swipe-stamp").style.opacity = "";
  }
  function reject() {
    if (pending || matched) return;
    resetDrag();
    card.classList.remove("nudge");
    void card.offsetWidth;
    card.classList.add("nudge");
    toast("Других кандидатов не завезли. Давай ещё раз, только вправо 🙂");
  }
  card.addEventListener("animationend", () => card.classList.remove("nudge"));
  async function makeMatch() {
    if (pending || matched) return;
    resetDrag();
    pending = true;
    [accept, info, rewind].forEach((button) => {
      button.disabled = true;
    });
    accept.setAttribute("aria-busy", "true");
    hint.textContent = "Проверяем совместимость…";
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 90000);
    try {
      const response = await fetch("/api/match/", { signal: controller.signal, cache: "no-store" });
      if (!response.ok) throw new Error("Match request failed");
      const data = await response.json();
      if (data.matched !== true || typeof data.message !== "string")
        throw new Error("Invalid response");
      matched = true;
      showAbout(false);
      root.querySelector("#match-message").textContent = data.message;
      card.hidden = true;
      match.hidden = false;
      actions.hidden = true;
      hint.textContent = "Первый шаг сделан. Теперь можно познакомиться.";
      match.querySelector("a").focus({ preventScroll: true });
    } catch {
      toast("Не удалось связаться с сервером. Нажми на сердце ещё раз.");
      hint.textContent = "Свайпни вправо или нажми на сердце";
    } finally {
      clearTimeout(timeout);
      pending = false;
      [accept, info, rewind].forEach((button) => {
        button.disabled = false;
      });
      accept.removeAttribute("aria-busy");
    }
  }
  accept.addEventListener("click", makeMatch);
  rewind.addEventListener("click", reject);
  info.addEventListener("click", () => showAbout(about.hidden));
  root.querySelector("#again").addEventListener("click", () => {
    matched = false;
    match.hidden = true;
    card.hidden = false;
    actions.hidden = false;
    hint.textContent = "Свайпни вправо или нажми на сердце";
    accept.focus({ preventScroll: true });
  });
  card.addEventListener("pointerdown", (event) => {
    if (pending || matched || !about.hidden || !event.isPrimary || event.button !== 0) return;
    start = { x: event.clientX, y: event.clientY };
    swipeX = 0;
    card.setPointerCapture(event.pointerId);
  });
  card.addEventListener("pointermove", (event) => {
    if (!start) return;
    const dx = event.clientX - start.x;
    const dy = event.clientY - start.y;
    if (Math.abs(dy) > 30 && Math.abs(dy) > Math.abs(dx)) {
      resetDrag();
      return;
    }
    swipeX = dx;
    card.classList.add("dragging");
    card.style.transform = `translateX(${Math.max(-100, Math.min(150, dx))}px) rotate(${Math.max(-8, Math.min(12, dx / 18))}deg)`;
    card.querySelector(".swipe-stamp").style.opacity = String(Math.min(1, Math.max(0, dx / 100)));
  });
  card.addEventListener("pointerup", () => {
    if (!start) return;
    const dx = swipeX;
    resetDrag();
    if (dx > 80) makeMatch();
    else if (dx < -65) reject();
  });
  card.addEventListener("pointercancel", resetDrag);
  card.addEventListener("lostpointercapture", resetDrag);
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      showAbout(false);
      toastArea.replaceChildren();
    }
  });
})();
