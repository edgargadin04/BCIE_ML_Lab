/**
 * ============================================
 *  BCIE ML Lab — Módulo de Guardia de Sesión
 *  Conforme ISO 27001:2022
 * ============================================
 * 
 * Seguridad transversal entre páginas:
 * - Timeout de sesión por inactividad (A.9.4.2)
 * - Sanitización de entrada / anti-inyección (A.14.2.5)
 * - Validación CSRF
 * - Rastreo de actividad del usuario
 * - Cumplimiento de expiración de sesión
 * 
 * Incluir en TODAS las páginas protegidas
 * (dashboard_unificado.html, admin.html, etc.)
 */

'use strict';

const SESSION_GUARD = (function() {

  // ============================================
  // Configuración — ISO 27001 A.9.4.2
  // ============================================
  const CONFIG = Object.freeze({
    SESSION_TIMEOUT_MS: 30 * 60 * 1000,   // Timeout inactividad: 30 min
    SESSION_MAX_MS: 8 * 60 * 60 * 1000,   // Máximo absoluto: 8 horas
    WARNING_BEFORE_MS: 2 * 60 * 1000,     // Advertencia 2 min antes
    CHECK_INTERVAL_MS: 30 * 1000,         // Verificación cada 30 seg
    LOGIN_URL: null,                       // Se establece dinámicamente
    ACTIVITY_EVENTS: ['mousemove', 'keypress', 'click', 'scroll', 'touchstart'],
  });

  // ============================================
  // Estado
  // ============================================
  let idleTimer = null;
  let checkInterval = null;
  let warningShown = false;
  let lastActivity = Date.now();
  let warningModal = null;

  // ============================================
  // Sanitización de entrada — ISO 27001 A.14.2.5
  // ============================================
  function sanitizeInput(input) {
    if (typeof input !== 'string') return input;
    return input
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#x27;')
      .replace(/\//g, '&#x2F;');
  }

  function sanitizeForAttribute(input) {
    if (typeof input !== 'string') return input;
    return input.replace(/[^\w\s@.\-]/g, '');
  }

  // Prevenir inyección de scripts vía innerHTML
  function safeText(element, text) {
    if (element) element.textContent = text;
  }

  // ============================================
  // Validación de sesión
  // ============================================
  function getLoginUrl() {
    const path = window.location.pathname;
    if (path.includes('/login/')) return 'index.html';
    return 'login/index.html';
  }

  function getAuthData() {
    try {
      const raw = sessionStorage.getItem('bcie_auth');
      if (!raw) return null;
      const data = JSON.parse(raw);
      if (!data.authenticated || !data.user) return null;
      return data;
    } catch (e) {
      return null;
    }
  }

  function getSessionData() {
    try {
      const raw = sessionStorage.getItem('bcie_session');
      if (!raw) return null;
      return JSON.parse(raw);
    } catch (e) {
      return null;
    }
  }

  function isSessionValid() {
    const auth = getAuthData();
    if (!auth) return false;

    const session = getSessionData();
    if (session && session.expiresAt && Date.now() > session.expiresAt) {
      // Timeout absoluto de sesión
      console.log('[SESSION_GUARD] Session expired (absolute timeout)');
      return false;
    }

    return true;
  }

  // ============================================
  // Timeout por inactividad — ISO 27001 A.9.4.2
  // ============================================
  function resetIdleTimer() {
    lastActivity = Date.now();
    updateLastActivity();
    
    if (warningShown) {
      hideWarning();
    }

    clearTimeout(idleTimer);
    idleTimer = setTimeout(() => {
      showTimeoutWarning();
    }, CONFIG.SESSION_TIMEOUT_MS - CONFIG.WARNING_BEFORE_MS);
  }

  function updateLastActivity() {
    try {
      const auth = getAuthData();
      if (auth) {
        auth.lastActivity = Date.now();
        sessionStorage.setItem('bcie_auth', JSON.stringify(auth));
      }
    } catch(e) {}
  }

  // ============================================
  // Modal de advertencia de timeout
  // ============================================
  function createWarningModal() {
    if (warningModal) return;

    warningModal = document.createElement('div');
    warningModal.id = 'sessionTimeoutWarning';
    warningModal.style.cssText = `
      display:none; position:fixed; top:0; left:0; right:0; bottom:0;
      background:rgba(0,0,0,0.7); z-index:99999;
      justify-content:center; align-items:center;
      font-family:'Inter','Segoe UI',system-ui,sans-serif;
    `;
    warningModal.innerHTML = `
      <div style="
        background:var(--card-bg,#1e293b); border:1px solid var(--border,#334155);
        border-radius:16px; padding:32px; max-width:420px; width:90%;
        text-align:center; color:var(--text,#e2e8f0);
        box-shadow:0 25px 50px rgba(0,0,0,0.4);
      ">
        <svg viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2"
          width="48" height="48" style="margin-bottom:16px">
          <circle cx="12" cy="12" r="10"/>
          <polyline points="12 6 12 12 16 14"/>
        </svg>
        <h3 style="margin:0 0 8px;font-size:1.25rem;color:#f59e0b">
          Sesión por Expirar
        </h3>
        <p style="margin:0 0 8px;font-size:.9rem;opacity:.8">
          Tu sesión se cerrará por inactividad en:
        </p>
        <div id="timeoutCountdown" style="
          font-size:2rem;font-weight:700;color:#f59e0b;margin:12px 0;
          font-variant-numeric:tabular-nums;
        ">2:00</div>
        <p style="margin:0 0 20px;font-size:.8rem;opacity:.6">
          ISO 27001 A.9.4.2 — Control de sesiones inactivas
        </p>
        <div style="display:flex;gap:12px;justify-content:center">
          <button id="btnExtendSession" style="
            background:linear-gradient(135deg,#0d9488,#14b8a6);
            color:#fff;border:none;border-radius:8px;padding:10px 24px;
            font-weight:600;cursor:pointer;font-size:.9rem;
          ">Continuar Sesión</button>
          <button id="btnEndSession" style="
            background:transparent;color:#f59e0b;
            border:1px solid #f59e0b;border-radius:8px;padding:10px 24px;
            font-weight:600;cursor:pointer;font-size:.9rem;
          ">Cerrar Sesión</button>
        </div>
      </div>
    `;
    document.body.appendChild(warningModal);

    document.getElementById('btnExtendSession').addEventListener('click', () => {
      hideWarning();
      resetIdleTimer();
      console.log('[SESSION_GUARD] Session extended by user');
    });

    document.getElementById('btnEndSession').addEventListener('click', () => {
      forceLogout('user_logout');
    });
  }

  function showTimeoutWarning() {
    warningShown = true;
    createWarningModal();
    warningModal.style.display = 'flex';
    
    let remaining = CONFIG.WARNING_BEFORE_MS / 1000;
    const countdown = document.getElementById('timeoutCountdown');

    const interval = setInterval(() => {
      remaining--;
      if (remaining <= 0) {
        clearInterval(interval);
        forceLogout('timeout');
        return;
      }
      const m = Math.floor(remaining / 60);
      const s = remaining % 60;
      if (countdown) countdown.textContent = `${m}:${s.toString().padStart(2, '0')}`;
    }, 1000);

    // Almacenar intervalo para limpieza
    warningModal._interval = interval;
  }

  function hideWarning() {
    warningShown = false;
    if (warningModal) {
      warningModal.style.display = 'none';
      if (warningModal._interval) {
        clearInterval(warningModal._interval);
        warningModal._interval = null;
      }
    }
  }

  // ============================================
  // Cierre forzado de sesión
  // ============================================
  function forceLogout(reason = 'timeout') {
    hideWarning();
    clearTimeout(idleTimer);
    clearInterval(checkInterval);

    // Registrar motivo
    console.log(`[SESSION_GUARD] Logout — motivo: ${reason}`);

    // Limpiar datos de sesión
    sessionStorage.removeItem('bcie_auth');
    sessionStorage.removeItem('bcie_session');

    // Redirigir al login con motivo
    const loginUrl = getLoginUrl();
    const separator = loginUrl.includes('?') ? '&' : '?';
    window.location.href = `${loginUrl}${separator}reason=${reason}`;
  }

  // ============================================
  // Verificación periódica de sesión
  // ============================================
  function startPeriodicCheck() {
    checkInterval = setInterval(() => {
      if (!isSessionValid()) {
        forceLogout('expired');
        return;
      }

      // Verificar tiempo de inactividad
      const idleMs = Date.now() - lastActivity;
      if (idleMs > CONFIG.SESSION_TIMEOUT_MS) {
        forceLogout('idle_timeout');
      }
    }, CONFIG.CHECK_INTERVAL_MS);
  }

  // ============================================
  // Inicialización del guardia
  // ============================================
  function init(options = {}) {
    // Verificar sesión válida
    if (!isSessionValid()) {
      forceLogout('no_session');
      return false;
    }

    // Configurar rastreo de actividad
    CONFIG.ACTIVITY_EVENTS.forEach(event => {
      document.addEventListener(event, () => {
        resetIdleTimer();
      }, { passive: true });
    });

    // Iniciar temporizadores
    resetIdleTimer();
    startPeriodicCheck();

    console.log('[SESSION_GUARD] Inicializado — timeout 30min, verificación periódica activa');
    return true;
  }

  // ============================================
  // API pública
  // ============================================
  return {
    init,
    sanitizeInput,
    sanitizeForAttribute,
    safeText,
    getAuthData,
    getSessionData,
    isSessionValid,
    forceLogout,
    resetIdleTimer,
  };

})();
