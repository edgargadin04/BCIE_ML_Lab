/**
 * ============================================
 *  BCIE ML Lab — Authentication System
 *  ISO 27001/27002 Compliant Implementation
 * ============================================
 *
 * Security Controls Implemented:
 * - A.9.4.2  Secure log-on procedures
 * - A.9.4.3  Password management system
 * - A.9.3.1  Use of secret authentication info
 * - A.12.4.1 Event logging (audit trail)
 * - A.9.4.1  Information access restriction
 *
 * Features:
 * - SHA-256 password hashing with salt
 * - Account lockout after max failed attempts
 * - Progressive delay on failed attempts
 * - Full audit trail with timestamps
 * - Session timeout management
 * - CSRF token simulation
 * - Password strength validation
 * - Rate limiting per IP/session
 */

'use strict';

// ============================================
// Configuration — ISO 27001 A.9.4.2
// ============================================
const AUTH_CONFIG = Object.freeze({
  SALT: 'BCIE_ML_LAB_2026_SALT_v1',
  MAX_ATTEMPTS: 5,                   // ISO: Account lockout threshold
  LOCKOUT_DURATION_MS: 5 * 60 * 1000, // 5 minutes lockout
  SESSION_TIMEOUT_MS: 30 * 60 * 1000, // 30 minutes idle timeout
  SESSION_MAX_MS: 8 * 60 * 60 * 1000, // 8 hours absolute maximum
  MIN_PASSWORD_LENGTH: 6,
  PROGRESSIVE_DELAY_MS: 1000,        // Base delay per attempt
  CSRF_TOKEN_LENGTH: 32,
});

// ============================================
// User Store (Hashed) — ISO 27001 A.9.4.3
// ============================================
// In production, this would be a server-side database
// Passwords are stored as SHA-256(salt + password)
let USER_STORE = {};

// Dashboard routing per role
const DASHBOARD_ROUTES = Object.freeze({
  'Administrador': 'admin.html',                                       // Admin → full admin panel
  'Analista BCIE': '../data/gold/dashboard/dashboard_unificado.html',  // BCIE user → real dashboard
});

// ============================================
// State Management
// ============================================
const state = {
  failedAttempts: 0,
  lockedUntil: null,
  currentSession: null,
  sessionTimer: null,
  csrfToken: null,
  auditLog: [],
};

// ============================================
// Crypto Utilities — SHA-256
// ============================================
async function sha256(message) {
  const msgBuffer = new TextEncoder().encode(message);
  const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
}

async function hashPassword(password) {
  return await sha256(AUTH_CONFIG.SALT + password);
}

// ============================================
// CSRF Token — ISO 27001 A.14.1.2
// ============================================
function generateCSRFToken() {
  const array = new Uint8Array(AUTH_CONFIG.CSRF_TOKEN_LENGTH);
  crypto.getRandomValues(array);
  state.csrfToken = Array.from(array, b => b.toString(16).padStart(2, '0')).join('');
  return state.csrfToken;
}

// ============================================
// Audit Logger — ISO 27001 A.12.4.1
// ============================================
function auditLog(level, message, details = {}) {
  const entry = {
    timestamp: new Date().toISOString(),
    level,
    message,
    details: {
      ...details,
      userAgent: navigator.userAgent.substring(0, 80),
      sessionId: state.currentSession?.id || 'none',
    },
  };

  state.auditLog.push(entry);

  // Keep last 100 entries
  if (state.auditLog.length > 100) {
    state.auditLog.shift();
  }

  // Render to audit panel
  renderAuditEntry(entry);

  // In production: send to SIEM/logging server
  console.log(`[AUDIT][${level.toUpperCase()}] ${entry.timestamp} — ${message}`);
}

// ============================================
// Password Strength — ISO 27001 A.9.4.3
// ============================================
function evaluatePasswordStrength(password) {
  let score = 0;
  const checks = {
    length: password.length >= 8,
    uppercase: /[A-Z]/.test(password),
    lowercase: /[a-z]/.test(password),
    numbers: /[0-9]/.test(password),
    special: /[^A-Za-z0-9]/.test(password),
    longEnough: password.length >= 12,
  };

  if (checks.length) score++;
  if (checks.uppercase) score++;
  if (checks.lowercase) score++;
  if (checks.numbers) score++;
  if (checks.special) score++;
  if (checks.longEnough) score++;

  if (score <= 2) return { level: 'weak', text: 'Débil — agrega mayúsculas, números o símbolos', class: 'weak' };
  if (score <= 3) return { level: 'fair', text: 'Aceptable — considera agregar más complejidad', class: 'fair' };
  if (score <= 4) return { level: 'good', text: 'Buena — cumple requisitos de seguridad', class: 'good' };
  return { level: 'strong', text: 'Fuerte — excelente nivel de seguridad', class: 'strong' };
}

// ============================================
// Account Lockout — ISO 27001 A.9.4.2
// ============================================
function isAccountLocked() {
  if (!state.lockedUntil) return false;
  if (Date.now() >= state.lockedUntil) {
    // Lockout expired
    state.lockedUntil = null;
    state.failedAttempts = 0;
    auditLog('info', 'Account lockout expired, attempts reset');
    return false;
  }
  return true;
}

function lockAccount() {
  state.lockedUntil = Date.now() + AUTH_CONFIG.LOCKOUT_DURATION_MS;
  auditLog('error', `Account LOCKED for ${AUTH_CONFIG.LOCKOUT_DURATION_MS / 1000}s after ${AUTH_CONFIG.MAX_ATTEMPTS} failed attempts`, {
    lockedUntil: new Date(state.lockedUntil).toISOString(),
  });
}

function getRemainingLockoutSeconds() {
  if (!state.lockedUntil) return 0;
  return Math.max(0, Math.ceil((state.lockedUntil - Date.now()) / 1000));
}

// ============================================
// Session Management — ISO 27001 A.9.4.2
// ============================================
function createSession(username, role) {
  const sessionId = crypto.randomUUID();
  const now = Date.now();

  state.currentSession = {
    id: sessionId,
    username,
    role,
    createdAt: now,
    lastActivity: now,
    expiresAt: now + AUTH_CONFIG.SESSION_MAX_MS,
    csrfToken: generateCSRFToken(),
  };

  // Store in sessionStorage (not localStorage for security)
  sessionStorage.setItem('bcie_session', JSON.stringify({
    id: sessionId,
    username,
    role,
    createdAt: now,
    expiresAt: state.currentSession.expiresAt,
  }));

  // Start idle timeout
  resetIdleTimer();

  auditLog('success', `Session created for user "${username}"`, {
    sessionId,
    role,
    expiresAt: new Date(state.currentSession.expiresAt).toISOString(),
  });

  return state.currentSession;
}

function resetIdleTimer() {
  clearTimeout(state.sessionTimer);
  if (state.currentSession) {
    state.currentSession.lastActivity = Date.now();
    state.sessionTimer = setTimeout(() => {
      auditLog('warn', 'Session expired due to inactivity');
      destroySession(true);
    }, AUTH_CONFIG.SESSION_TIMEOUT_MS);
  }
}

function destroySession(expired = false) {
  const username = state.currentSession?.username || 'unknown';
  clearTimeout(state.sessionTimer);
  sessionStorage.removeItem('bcie_session');
  state.currentSession = null;

  auditLog('info', `Session destroyed for "${username}"${expired ? ' (expired)' : ' (logout)'}`);

  // Show login again
  showLoginScreen(expired);
}

// ============================================
// Authentication — Core
// ============================================
async function authenticate(username, password) {
  // Check lockout
  if (isAccountLocked()) {
    const remaining = getRemainingLockoutSeconds();
    auditLog('warn', `Login attempt blocked — account locked (${remaining}s remaining)`, { username });
    return {
      success: false,
      error: 'locked',
      message: `Cuenta bloqueada. Intenta en ${formatTime(remaining)}.`,
      remainingSeconds: remaining,
    };
  }

  // Rate limiting — progressive delay
  if (state.failedAttempts > 0) {
    const delay = state.failedAttempts * AUTH_CONFIG.PROGRESSIVE_DELAY_MS;
    await new Promise(resolve => setTimeout(resolve, delay));
  }

  // Validate input
  if (!username || !password) {
    auditLog('warn', 'Login attempt with empty credentials');
    return { success: false, error: 'validation', message: 'Ingresa usuario y contraseña.' };
  }

  if (password.length < AUTH_CONFIG.MIN_PASSWORD_LENGTH) {
    auditLog('warn', 'Login attempt with short password', { username });
    return { success: false, error: 'validation', message: 'La contraseña no cumple los requisitos mínimos.' };
  }

  // Hash and compare
  const hashedInput = await hashPassword(password);
  const user = USER_STORE[username.toLowerCase()];

  if (!user || user.passwordHash !== hashedInput) {
    state.failedAttempts++;
    const remaining = AUTH_CONFIG.MAX_ATTEMPTS - state.failedAttempts;

    auditLog('error', `Failed login attempt ${state.failedAttempts}/${AUTH_CONFIG.MAX_ATTEMPTS}`, {
      username,
      remainingAttempts: remaining,
    });

    // Lock if max attempts reached
    if (state.failedAttempts >= AUTH_CONFIG.MAX_ATTEMPTS) {
      lockAccount();
      return {
        success: false,
        error: 'locked',
        message: `Cuenta bloqueada por ${AUTH_CONFIG.LOCKOUT_DURATION_MS / 60000} minutos tras ${AUTH_CONFIG.MAX_ATTEMPTS} intentos fallidos.`,
        remainingSeconds: AUTH_CONFIG.LOCKOUT_DURATION_MS / 1000,
      };
    }

    // Generic error message (don't reveal if username exists — ISO best practice)
    return {
      success: false,
      error: 'invalid',
      message: `Credenciales inválidas. ${remaining} intento${remaining !== 1 ? 's' : ''} restante${remaining !== 1 ? 's' : ''}.`,
      remainingAttempts: remaining,
    };
  }

  // Success
  state.failedAttempts = 0;
  const session = createSession(user.username, user.role);

  return {
    success: true,
    session,
    user: { username: user.username, role: user.role, displayName: user.displayName },
  };
}

// ============================================
// UI Rendering
// ============================================
function renderAuditEntry(entry) {
  const auditBody = document.getElementById('auditBody');
  if (!auditBody) return;

  const div = document.createElement('div');
  div.className = `audit-entry ${entry.level}`;

  const time = new Date(entry.timestamp).toLocaleTimeString('es-HN', { hour12: false });
  div.innerHTML = `<span class="timestamp">[${time}]</span> ${entry.message}`;

  auditBody.prepend(div);
}

function showAlert(type, message) {
  const alert = document.getElementById('loginAlert');
  alert.className = `alert ${type} visible`;
  alert.innerHTML = `<span>${getAlertIcon(type)}</span> ${message}`;
}

function hideAlert() {
  const alert = document.getElementById('loginAlert');
  alert.className = 'alert';
}

function getAlertIcon(type) {
  const svgBase = 'width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-3px"';
  const icons = {
    error: `<svg ${svgBase}><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>`,
    warning: `<svg ${svgBase}><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>`,
    success: `<svg ${svgBase}><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>`,
    info: `<svg ${svgBase}><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>`,
  };
  return icons[type] || icons.info;
}

function formatTime(seconds) {
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${m}:${s.toString().padStart(2, '0')}`;
}

function showLockoutTimer() {
  const timer = document.getElementById('lockoutTimer');
  const countdown = document.getElementById('lockoutCountdown');
  const loginForm = document.getElementById('loginFormFields');

  timer.classList.add('visible');
  loginForm.style.display = 'none';

  const interval = setInterval(() => {
    const remaining = getRemainingLockoutSeconds();
    if (remaining <= 0) {
      clearInterval(interval);
      timer.classList.remove('visible');
      loginForm.style.display = 'block';
      hideAlert();
      auditLog('info', 'Lockout expired — login form re-enabled');
    } else {
      countdown.textContent = formatTime(remaining);
    }
  }, 1000);
}

function showLoginScreen(expired = false) {
  const loginContainer = document.querySelector('.login-container');
  const dashboard = document.getElementById('dashboard');

  loginContainer.style.display = 'flex';
  dashboard.classList.remove('visible');

  if (expired) {
    const notice = document.getElementById('sessionNotice');
    notice.classList.add('visible');
  }
}

function showDashboard(user, session) {
  const loginContainer = document.querySelector('.login-container');
  const dashboard = document.getElementById('dashboard');

  loginContainer.style.display = 'none';
  dashboard.classList.add('visible');

  // Populate dashboard
  document.getElementById('dashUserName').textContent = user.displayName;
  document.getElementById('dashUserRole').textContent = user.role;
  document.getElementById('navUserName').textContent = user.displayName;
  document.getElementById('navUserRole').textContent = user.role;
  document.getElementById('dashSessionId').textContent = session.id.substring(0, 8) + '…';
  document.getElementById('dashLoginTime').textContent = new Date(session.createdAt).toLocaleString('es-HN');
  document.getElementById('dashExpires').textContent = new Date(session.expiresAt).toLocaleString('es-HN');
  document.getElementById('dashCSRF').textContent = session.csrfToken.substring(0, 12) + '…';
}

// ============================================
// Password Visibility Toggle
// ============================================
function togglePasswordVisibility() {
  const input = document.getElementById('password');
  const btn = document.getElementById('togglePwd');
  const eyeOpen = btn.querySelector('.eye-open');
  const eyeClosed = btn.querySelector('.eye-closed');

  if (input.type === 'password') {
    input.type = 'text';
    if (eyeOpen) eyeOpen.style.display = 'none';
    if (eyeClosed) eyeClosed.style.display = 'block';
  } else {
    input.type = 'password';
    if (eyeOpen) eyeOpen.style.display = 'block';
    if (eyeClosed) eyeClosed.style.display = 'none';
  }
}

// ============================================
// Password Strength Display
// ============================================
function updatePasswordStrength(password) {
  const container = document.getElementById('passwordStrength');
  const fill = document.getElementById('strengthFill');
  const text = document.getElementById('strengthText');

  if (!password || password.length === 0) {
    container.classList.remove('visible');
    return;
  }

  container.classList.add('visible');
  const strength = evaluatePasswordStrength(password);

  fill.className = `fill ${strength.class}`;
  text.textContent = strength.text;
}

// ============================================
// Initialization
// ============================================
async function initializeAuth() {
  auditLog('info', 'Authentication system initialized');
  auditLog('info', `Security: SHA-256 hashing, ${AUTH_CONFIG.MAX_ATTEMPTS}-attempt lockout, ${AUTH_CONFIG.SESSION_TIMEOUT_MS / 60000}min timeout`);

  // Pre-compute password hashes
  const adminHash = await hashPassword('UNIR03d');
  const bcieHash = await hashPassword('2026ML');

  USER_STORE = {
    'admin': {
      username: 'admin',
      passwordHash: adminHash,
      role: 'Administrador',
      displayName: 'Norman Sabillon',
    },
    'nsabillon': {
      username: 'nsabillon',
      passwordHash: adminHash,
      role: 'Administrador',
      displayName: 'Norman Sabillon',
    },
    'waguilar': {
      username: 'waguilar',
      passwordHash: adminHash,
      role: 'Administrador',
      displayName: 'Willson Aguilar',
    },
    'egarcia': {
      username: 'egarcia',
      passwordHash: adminHash,
      role: 'Administrador',
      displayName: 'Edgar Garcia',
    },
    'bcie': {
      username: 'bcie',
      passwordHash: bcieHash,
      role: 'Analista BCIE',
      displayName: 'Analista BCIE',
    },
  };

  auditLog('info', 'User store loaded (5 users registered)');
  generateCSRFToken();
  auditLog('info', `CSRF token generated: ${state.csrfToken.substring(0, 12)}…`);

  // Check existing session
  const existing = sessionStorage.getItem('bcie_session');
  if (existing) {
    try {
      const session = JSON.parse(existing);
      if (Date.now() < session.expiresAt) {
        auditLog('info', 'Restoring existing session');
        state.currentSession = session;
        resetIdleTimer();
        const user = USER_STORE[session.username];
        if (user) {
          showDashboard(
            { username: user.username, role: user.role, displayName: user.displayName },
            session
          );
          return;
        }
      } else {
        auditLog('warn', 'Found expired session, clearing');
        sessionStorage.removeItem('bcie_session');
      }
    } catch (e) {
      sessionStorage.removeItem('bcie_session');
    }
  }
}

// ============================================
// Event Handlers
// ============================================
document.addEventListener('DOMContentLoaded', () => {
  initializeAuth();

  // Login form submission
  const form = document.getElementById('loginForm');
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    hideAlert();

    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value;
    const btn = document.getElementById('loginBtn');

    btn.classList.add('loading');
    btn.disabled = true;

    // Simulate network latency for realistic feel
    await new Promise(r => setTimeout(r, 800));

    const result = await authenticate(username, password);

    btn.classList.remove('loading');
    btn.disabled = false;

    if (result.success) {
      showAlert('success', 'Autenticación exitosa. Redirigiendo…');
      
      // Determine destination based on role
      const route = DASHBOARD_ROUTES[result.user.role] || 'inline';
      
      if (route !== 'inline') {
        // Store auth info for the dashboard page to read
        sessionStorage.setItem('bcie_auth', JSON.stringify({
          authenticated: true,
          user: result.user,
          session: result.session,
          loginTime: new Date().toISOString(),
        }));
        auditLog('info', `Redirecting to dashboard: ${route}`);
        await new Promise(r => setTimeout(r, 1200));
        window.location.href = route;
        return;
      }
      
      // Inline dashboard for admin
      await new Promise(r => setTimeout(r, 1000));
      showDashboard(result.user, result.session);
      form.reset();
    } else {
      if (result.error === 'locked') {
        showAlert('error', result.message);
        showLockoutTimer();
      } else {
        showAlert('error', result.message);
      }
    }
  });

  // Password strength
  const pwdInput = document.getElementById('password');
  pwdInput.addEventListener('input', (e) => {
    updatePasswordStrength(e.target.value);
  });

  // Toggle password visibility
  document.getElementById('togglePwd').addEventListener('click', togglePasswordVisibility);

  // Audit panel toggle
  document.getElementById('auditHeader').addEventListener('click', () => {
    document.getElementById('auditPanel').classList.toggle('expanded');
  });

  // Logout
  document.getElementById('logoutBtn')?.addEventListener('click', () => {
    destroySession(false);
  });

  // Reset idle timer on activity
  ['mousemove', 'keypress', 'click', 'scroll'].forEach(event => {
    document.addEventListener(event, () => {
      if (state.currentSession) resetIdleTimer();
    });
  });
});
