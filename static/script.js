/* Abre e fecha o menu lateral em modo mobile */

const menuMobile = document.querySelector(".menu-mobile");
const menuIcon = menuMobile.querySelector("i");
const body = document.querySelector("body");

const setMenu = (open) => {
  body.classList.toggle("menu-nav-active", open);
  menuIcon.classList.toggle("bi-list", !open);
  menuIcon.classList.toggle("bi-x", open);
  menuMobile.setAttribute("aria-expanded", String(open));
  menuMobile.setAttribute("aria-label", open ? "Fechar menu" : "Abrir menu");
};

menuMobile.addEventListener("click", () => {
  setMenu(!body.classList.contains("menu-nav-active"));
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && body.classList.contains("menu-nav-active")) setMenu(false);
});


/* Fecha o menu quando clicar em algum item e muda o icone para List*/

document.querySelectorAll(".nav-item").forEach((item) => {
  item.addEventListener("click", () => {
    if (body.classList.contains("menu-nav-active")) setMenu(false);
  });
});


// Animar os itens com data-anime quando entram na tela (uma vez só).
// IntersectionObserver evita recalcular layout a cada evento de scroll.

const animated = document.querySelectorAll("[data-anime]");
const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

if (reduceMotion || !("IntersectionObserver" in window)) {
  animated.forEach((element) => element.classList.add("animate"));
} else {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("animate");
        observer.unobserve(entry.target);
      }
    });
  }, { rootMargin: "0px 0px -10% 0px" });
  animated.forEach((element) => observer.observe(element));
}


// Formulário de contato: envia via fetch e mostra o retorno no próprio card.
// Sem JS, o form continua funcionando com POST normal + redirect.

const contactForm = document.querySelector("#contact-form");
const btnEnviar = document.querySelector("#btn-enviar");
const btnEnviarLoader = document.querySelector("#btn-enviar-loader");
const contactStatus = document.querySelector("#contact-status");

const translate = (key, fallback) => (window.issqaT && window.issqaT(key)) || fallback;

const setSending = (sending) => {
  btnEnviar.style.display = sending ? "none" : "";
  btnEnviarLoader.style.display = sending ? "inline-block" : "none";
};

const showContactStatus = (ok, key, fallback) => {
  const alert = document.createElement("div");
  alert.className = `alert alert-${ok ? "success" : "danger"} mb-0`;
  const icon = document.createElement("i");
  icon.className = `bi bi-${ok ? "check-circle-fill" : "exclamation-triangle-fill"} me-2`;
  icon.setAttribute("aria-hidden", "true");
  const text = document.createElement("span");
  text.setAttribute("data-i18n", key);
  text.textContent = translate(key, fallback);
  alert.append(icon, text);
  contactStatus.replaceChildren(alert);
};

if (contactForm) {
  contactForm.addEventListener("submit", async (event) => {
    if (!window.fetch) return;
    event.preventDefault();
    setSending(true);
    contactStatus.replaceChildren();
    try {
      const response = await fetch(contactForm.action, {
        method: "POST",
        body: new FormData(contactForm),
        headers: { "X-Requested-With": "fetch", Accept: "application/json" },
      });
      const data = await response.json();
      showContactStatus(data.ok, data.key, data.message);
      if (data.ok) contactForm.reset();
    } catch (error) {
      showContactStatus(false, "contact-err-send",
        "Não foi possível enviar agora. Tente novamente ou fale pelo WhatsApp.");
    } finally {
      setSending(false);
    }
  });

  // Voltar pelo histórico (bfcache) não pode deixar o botão preso em "Enviando".
  window.addEventListener("pageshow", () => setSending(false));
}

// Tira a mensagem de sucesso (fallback sem JS) depois de 5 segundos

setTimeout(() => {
  const alerta = document.querySelector('#alerta[data-autohide="true"]');
  if (alerta) alerta.style.display = 'none';
}, 5000)
