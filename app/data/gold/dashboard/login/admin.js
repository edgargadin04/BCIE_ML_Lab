'use strict';
// ============================================
// i18n — Internacionalización
// ============================================
let currentLang = localStorage.getItem('bcie-lang') || 'es';
const I18N = {
  es: {
    'nav.subtitle':'Panel de Administración','nav.logout':'Cerrar Sesión',
    'nav.search':'Buscar usuarios, modelos, eventos...',
    'tab.overview':'Resumen','tab.users':'Usuarios','tab.models':'Modelos ML',
    'tab.dashboards':'Dashboards','tab.etl':'Datos & ETL','tab.audit':'Audit Log',
    'tab.sessions':'Sesiones Activas','tab.health':'Health Check','tab.config':'Configuración',
    'tab.alerts':'Alertas',
    'sidebar.principal':'Principal','sidebar.security':'Seguridad',
    'overview.title':'Resumen del Sistema','overview.users':'Usuarios Activos',
    'overview.models':'Modelos ML','overview.dashboards':'Dashboards','overview.iso':'Controles ISO',
    'overview.activity':'Actividad Reciente','overview.logins':'Logins por Día','overview.bytype':'Modelos por Tipo',
    'users.title':'Gestión de Usuarios','users.add':'Agregar Usuario',
    'users.username':'Usuario','users.name':'Nombre','users.role':'Rol',
    'users.status':'Estado','users.lastaccess':'Último Acceso','users.actions':'Acciones',
    'users.edit':'Editar','users.reset':'Reset','users.deactivate':'Desactivar','users.activate':'Activar',
    'users.active':'Activo','users.inactive':'Inactivo','users.history':'Historial de Actividad',
    'users.viewhistory':'Ver historial',
    'models.title':'Modelos de Machine Learning','models.all':'Todos',
    'models.viewdash':'Ver Dashboard','models.detail':'Detalle',
    'models.comparison':'Comparativa de Modelos',
    'audit.title':'Registro de Auditoría (ISO 27001 A.12.4.1)',
    'audit.all':'Todos los niveles','audit.export':'Exportar CSV',
    'audit.level':'Nivel','audit.event':'Evento',
    'sessions.title':'Sesiones Activas','sessions.start':'Inicio',
    'sessions.duration':'Duración','sessions.offline':'Offline',
    'health.title':'Health Check del Sistema','health.uptime':'Uptime del Sistema (7 días)',
    'health.healthy':'Saludable','health.degraded':'Degradado','health.down':'Caído',
    'health.latency':'Latencia','health.uptimepct':'Uptime',
    'config.title':'Configuración del Sistema',
    'etl.title':'Datos & Pipeline ETL',
    'search.noresults':'Sin resultados',
    'notif.title':'Notificaciones',
    'alerts.title':'Alertas Programables','alerts.add':'Nueva Alerta',
    'alerts.rules':'Reglas de Alerta','alerts.history':'Historial de Alertas',
    'alerts.enabled':'Activa','alerts.disabled':'Inactiva',
    'alerts.thresh':'Umbral','alerts.triggered':'Disparada',
    'modal.adduser':'Agregar Usuario','modal.cancel':'Cancelar','modal.create':'Crear Usuario',
    'modal.username':'Nombre de Usuario','modal.fullname':'Nombre Completo',
    'modal.role':'Rol','modal.password':'Contraseña Temporal',
    'modal.metrics':'MÉTRICAS','modal.details':'DETALLES',
    'modal.folder':'Carpeta','modal.trained':'Entrenado','modal.dataset':'Dataset',
    'modal.edituser':'Editar Usuario','modal.save':'Guardar Cambios',
    'modal.resetpw':'Restablecer Contraseña','modal.newpw':'Nueva Contraseña',
    'modal.confirmpw':'Confirmar Contraseña','modal.resetbtn':'Restablecer',
    'modal.deleteuser':'Eliminar Usuario','modal.deleteconfirm':'¿Eliminar este usuario permanentemente?',
    'modal.deletebtn':'Eliminar','modal.created':'Creado',
    'pw.weak':'Débil','pw.fair':'Regular','pw.good':'Buena','pw.strong':'Fuerte',
    'pw.requirements':'Requisitos: mín. 6 caracteres, 1 mayúscula, 1 número',
    'toast.saved':'Cambios guardados exitosamente',
    'toast.pwreset':'Contraseña restablecida exitosamente',
    'toast.deleted':'Usuario eliminado exitosamente',
    'tooltip.mape':'Error Absoluto Porcentual Medio — menor es mejor',
    'tooltip.rmse':'Raíz del Error Cuadrático Medio en USD',
    'tooltip.r2':'Coeficiente de Determinación (0-1) — mayor es mejor',
    'tooltip.silhouette':'Índice de separación de clusters (-1 a 1) — mayor es mejor',
    'tooltip.clusters':'Número óptimo de agrupaciones identificadas',
    'tooltip.inertia':'Suma de distancias al centroide — menor es mejor',
    'rbac.title':'Permisos por Rol (RBAC)','rbac.section':'Sección','rbac.full':'Completo','rbac.read':'Solo lectura','rbac.none':'Sin acceso',
    'timeout.title':'Sesión por expirar','timeout.msg':'Su sesión se cerrará por inactividad en','timeout.extend':'Extender Sesión',
    'pdf.title':'Reporte PDF del Sistema',
  },
  en: {
    'nav.subtitle':'Administration Panel','nav.logout':'Log Out',
    'nav.search':'Search users, models, events...',
    'tab.overview':'Overview','tab.users':'Users','tab.models':'ML Models',
    'tab.dashboards':'Dashboards','tab.etl':'Data & ETL','tab.audit':'Audit Log',
    'tab.sessions':'Active Sessions','tab.health':'Health Check','tab.config':'Settings',
    'tab.alerts':'Alerts',
    'sidebar.principal':'Main','sidebar.security':'Security',
    'overview.title':'System Overview','overview.users':'Active Users',
    'overview.models':'ML Models','overview.dashboards':'Dashboards','overview.iso':'ISO Controls',
    'overview.activity':'Recent Activity','overview.logins':'Logins per Day','overview.bytype':'Models by Type',
    'users.title':'User Management','users.add':'Add User',
    'users.username':'Username','users.name':'Name','users.role':'Role',
    'users.status':'Status','users.lastaccess':'Last Access','users.actions':'Actions',
    'users.edit':'Edit','users.reset':'Reset','users.deactivate':'Deactivate','users.activate':'Activate',
    'users.active':'Active','users.inactive':'Inactive','users.history':'Activity History',
    'users.viewhistory':'View history',
    'models.title':'Machine Learning Models','models.all':'All',
    'models.viewdash':'View Dashboard','models.detail':'Detail',
    'models.comparison':'Model Comparison',
    'audit.title':'Audit Log (ISO 27001 A.12.4.1)',
    'audit.all':'All levels','audit.export':'Export CSV',
    'audit.level':'Level','audit.event':'Event',
    'sessions.title':'Active Sessions','sessions.start':'Started',
    'sessions.duration':'Duration','sessions.offline':'Offline',
    'health.title':'System Health Check','health.uptime':'System Uptime (7 days)',
    'health.healthy':'Healthy','health.degraded':'Degraded','health.down':'Down',
    'health.latency':'Latency','health.uptimepct':'Uptime',
    'config.title':'System Settings',
    'etl.title':'Data & ETL Pipeline',
    'search.noresults':'No results',
    'notif.title':'Notifications',
    'alerts.title':'Programmable Alerts','alerts.add':'New Alert',
    'alerts.rules':'Alert Rules','alerts.history':'Alert History',
    'alerts.enabled':'Active','alerts.disabled':'Inactive',
    'alerts.thresh':'Threshold','alerts.triggered':'Triggered',
    'modal.adduser':'Add User','modal.cancel':'Cancel','modal.create':'Create User',
    'modal.username':'Username','modal.fullname':'Full Name',
    'modal.role':'Role','modal.password':'Temporary Password',
    'modal.metrics':'METRICS','modal.details':'DETAILS',
    'modal.folder':'Folder','modal.trained':'Trained','modal.dataset':'Dataset',
    'modal.edituser':'Edit User','modal.save':'Save Changes',
    'modal.resetpw':'Reset Password','modal.newpw':'New Password',
    'modal.confirmpw':'Confirm Password','modal.resetbtn':'Reset',
    'modal.deleteuser':'Delete User','modal.deleteconfirm':'Delete this user permanently?',
    'modal.deletebtn':'Delete','modal.created':'Created',
    'pw.weak':'Weak','pw.fair':'Fair','pw.good':'Good','pw.strong':'Strong',
    'pw.requirements':'Requirements: min. 6 chars, 1 uppercase, 1 number',
    'toast.saved':'Changes saved successfully',
    'toast.pwreset':'Password reset successfully',
    'toast.deleted':'User deleted successfully',
    'tooltip.mape':'Mean Absolute Percentage Error — lower is better',
    'tooltip.rmse':'Root Mean Square Error in USD',
    'tooltip.r2':'Coefficient of Determination (0-1) — higher is better',
    'tooltip.silhouette':'Cluster separation index (-1 to 1) — higher is better',
    'tooltip.clusters':'Optimal number of clusters identified',
    'tooltip.inertia':'Sum of distances to centroid — lower is better',
    'rbac.title':'Role-Based Permissions (RBAC)','rbac.section':'Section','rbac.full':'Full access','rbac.read':'Read only','rbac.none':'No access',
    'timeout.title':'Session expiring','timeout.msg':'Your session will close due to inactivity in','timeout.extend':'Extend Session',
    'pdf.title':'System PDF Report',
  }
};
function t(key) { return (I18N[currentLang] && I18N[currentLang][key]) || key; }
function applyI18n() {
  document.querySelectorAll('[data-i18n]').forEach(el => {
    el.textContent = t(el.getAttribute('data-i18n'));
  });
  const search = document.getElementById('globalSearch');
  if (search) search.placeholder = t('nav.search');
  document.getElementById('langLabel').textContent = currentLang.toUpperCase();
  renderAll();
}
function toggleLanguage() {
  currentLang = currentLang === 'es' ? 'en' : 'es';
  localStorage.setItem('bcie-lang', currentLang);
  applyI18n();
  const activeTab = document.querySelector('.sidebar-item.active');
  if (activeTab) {
    const tabId = activeTab.getAttribute('data-tab');
    document.getElementById('bcCurrent').textContent = t('tab.' + tabId);
  }
}

// ============================================
// Almacén de datos
// Usuarios base (siempre disponibles en cualquier navegador/dominio)
const BASE_USERS = [
  { id:1, username:'admin', displayName:'Administrador BCIE', role:'Administrador', status:'active', lastAccess:'26/02/2026 18:10', created:'01/01/2026' },
  { id:2, username:'nsabillon', displayName:'Norman Sabillon', role:'Administrador', status:'active', lastAccess:'26/02/2026 19:49', created:'26/02/2026' },
  { id:3, username:'waguilar', displayName:'Willson Aguilar', role:'Administrador', status:'active', lastAccess:'26/02/2026 19:49', created:'26/02/2026' },
  { id:4, username:'egarcia', displayName:'Edgar Garcia', role:'Administrador', status:'active', lastAccess:'26/02/2026 19:49', created:'26/02/2026' },
  { id:5, username:'bcie', displayName:'Analista BCIE', role:'Analista BCIE', status:'active', lastAccess:'26/02/2026 18:05', created:'26/02/2026' },
  { id:6, username:'testviewer', displayName:'Test Viewer User', role:'Viewer', status:'active', lastAccess:'—', created:'23/03/2026' },
];

// Fusionar: base + usuarios creados dinámicamente + lastAccess real
const baseUsernames = BASE_USERS.map(u => u.username);
const localUsers = JSON.parse(localStorage.getItem('bcie_users')) || [];

// Para usuarios base: usar lastAccess del localStorage si existe (dato real)
let USERS = BASE_USERS.map(bu => {
  const lu = localUsers.find(u => u.username === bu.username);
  if (lu && lu.lastAccess && lu.lastAccess !== '—') {
    return { ...bu, lastAccess: lu.lastAccess };
  }
  return bu;
});

// Agregar usuarios dinámicos (creados desde la UI)
const dynamicUsers = localUsers.filter(u => !baseUsernames.includes(u.username));
USERS = [...USERS, ...dynamicUsers];

// Sincronizar siempre
localStorage.setItem('bcie_users', JSON.stringify(USERS));

function saveUsersData() {
  localStorage.setItem('bcie_users', JSON.stringify(USERS));
}

async function hashBciePassword(password) {
  const msgBuffer = new TextEncoder().encode('BCIE_ML_LAB_2026_SALT_v1' + password);
  const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
}
const MODELS = [
  { name:'Prophet', folder:'aprobaciones_prophet_2026', type:'forecasting', status:'Finalizado', metrics:{mape:'8.2%',rmse:'$245M',r2:'0.87'}, trained:'25/02/2026', dashUrl:'../dashboard_unificado.html#forecasting'},
  { name:'NeuralProphet', folder:'aprobaciones_neu_prophet_2026', type:'forecasting', status:'Finalizado', metrics:{mape:'7.1%',rmse:'$198M',r2:'0.91'}, trained:'25/02/2026', dashUrl:'../dashboard_unificado.html#forecasting'},
  { name:'StatsForecast', folder:'aprobaciones_StatsForecast_2026', type:'forecasting', status:'Finalizado', metrics:{mape:'9.5%',rmse:'$310M',r2:'0.83'}, trained:'25/02/2026', dashUrl:'../dashboard_unificado.html#forecasting'},
  { name:'TimesFM', folder:'aprobaciones_TimesFM_2026', type:'forecasting', status:'Finalizado', metrics:{mape:'6.8%',rmse:'$185M',r2:'0.93'}, trained:'25/02/2026', dashUrl:'../dashboard_unificado.html#forecasting'},
  { name:'K-Means', folder:'aprobaciones_kmeans_2026', type:'clustering', status:'Finalizado', metrics:{silhouette:'0.42',clusters:'4',inertia:'2.3e6'}, trained:'24/02/2026', dashUrl:'../dashboard_unificado.html#clustering'},
  { name:'K-Medoids', folder:'aprobaciones_kmedoids_2026', type:'clustering', status:'Finalizado', metrics:{silhouette:'0.39',clusters:'4',inertia:'2.5e6'}, trained:'24/02/2026', dashUrl:'../dashboard_unificado.html#clustering'},
  { name:'DBSCAN', folder:'aprobaciones_dbscan_2026', type:'clustering', status:'Finalizado', metrics:{silhouette:'0.35',clusters:'3',noise:'12%'}, trained:'24/02/2026', dashUrl:'../dashboard_unificado.html#clustering'},
  { name:'HDBSCAN', folder:'aprobaciones_hdbscan_2026', type:'clustering', status:'Finalizado', metrics:{silhouette:'0.41',clusters:'5',noise:'8%'}, trained:'24/02/2026', dashUrl:'../dashboard_unificado.html#clustering'},
  { name:'GMM', folder:'aprobaciones_gmm_2026', type:'clustering', status:'Finalizado', metrics:{silhouette:'0.44',clusters:'4',bic:'1.2e4'}, trained:'24/02/2026', dashUrl:'../dashboard_unificado.html#clustering'},
  { name:'Hierarchical', folder:'aprobaciones_hierarchical_2026', type:'clustering', status:'Finalizado', metrics:{silhouette:'0.38',clusters:'4',linkage:'ward'}, trained:'24/02/2026', dashUrl:'../dashboard_unificado.html#clustering'},
  { name:'Mixed Clustering', folder:'aprobaciones_mixed_2026', type:'clustering', status:'Finalizado', metrics:{silhouette:'0.45',clusters:'4',method:'ensemble'}, trained:'24/02/2026', dashUrl:'../dashboard_unificado.html#clustering'},
  { name:'EDA Exploratorio', folder:'aprobaciones_eda_2026', type:'eda', status:'Finalizado', metrics:{variables:'12',correlations:'66',outliers:'23'}, trained:'23/02/2026', dashUrl:'../dashboard_unificado.html'},
];
const DASHBOARDS = [
  // ── Unificado ──
  { name:'Dashboard Ejecutivo Unificado', url:'../dashboard_unificado.html', status:'online', views:47, lastAccess:'02/03/2026 11:20', type:'unificado', sections:['Inicio','Forecasting','Clustering','Comparativa','Cross-Validation','Particiones']},
  // ── Forecasting Labs ──
  { name:'Prophet — Ejecutivo', url:'../labs/prophet/dashboard_ejecutivo.html', status:'online', views:23, lastAccess:'25/02/2026 20:30', type:'forecasting', sections:['Predicciones','KPIs','Tabla Detalle']},
  { name:'Prophet — Estratégico', url:'../labs/prophet/dashboard_estrategico.html', status:'online', views:18, lastAccess:'25/02/2026 20:30', type:'forecasting', sections:['Escenarios','Filtros','Proyección']},
  { name:'NeuralProphet — Ejecutivo', url:'../labs/neuralprophet/dashboard_ejecutivo.html', status:'online', views:19, lastAccess:'25/02/2026 19:15', type:'forecasting', sections:['Forecast','Tendencia','Métricas']},
  { name:'NeuralProphet — Estratégico', url:'../labs/neuralprophet/dashboard_estrategico.html', status:'online', views:14, lastAccess:'25/02/2026 19:15', type:'forecasting', sections:['Escenarios','Filtros','Proyección']},
  { name:'StatsForecast — Ejecutivo', url:'../labs/statsforecast/dashboard_ejecutivo.html', status:'online', views:21, lastAccess:'02/03/2026 11:22', type:'forecasting', sections:['AutoARIMA','KPIs','Tabla']},
  { name:'StatsForecast — Estratégico', url:'../labs/statsforecast/dashboard_estrategico.html', status:'online', views:16, lastAccess:'02/03/2026 11:22', type:'forecasting', sections:['Ensemble','Escenarios','Filtros']},
  { name:'TimesFM — Ejecutivo', url:'../labs/timesfm/dashboard_ejecutivo.html', status:'online', views:35, lastAccess:'02/03/2026 10:55', type:'forecasting', sections:['GPU','Predicciones','KPIs']},
  { name:'TimesFM — Proyecciones', url:'../labs/timesfm/dashboard_proyecciones.html', status:'online', views:28, lastAccess:'02/03/2026 10:55', type:'forecasting', sections:['2026-2030','Escenarios','País']},
  // ── Clustering Labs ──
  { name:'DBSCAN — Dashboard', url:'../labs/dbscan/dashboard_dbscan.html', status:'online', views:12, lastAccess:'24/02/2026 16:40', type:'clustering', sections:['Clusters','Noise','DBSCAN']},
  { name:'HDBSCAN — Dashboard', url:'../labs/hdbscan/dashboard_hdbscan.html', status:'online', views:14, lastAccess:'24/02/2026 16:40', type:'clustering', sections:['Clusters','Jerárquico','Noise']},
  { name:'GMM — Dashboard', url:'../labs/gmm/dashboard_gmm.html', status:'online', views:11, lastAccess:'24/02/2026 16:40', type:'clustering', sections:['Gaussian','BIC','Clusters']},
  { name:'K-Means — Dashboard', url:'../labs/kmeans/dashboard_kmeans.html', status:'online', views:13, lastAccess:'24/02/2026 16:40', type:'clustering', sections:['Elbow','Silhouette','Clusters']},
  { name:'K-Medoids — Dashboard', url:'../labs/kmedoids/dashboard_kmedoids.html', status:'online', views:10, lastAccess:'24/02/2026 16:40', type:'clustering', sections:['PAM','Medoids','Clusters']},
  { name:'Hierarchical — Dashboard', url:'../labs/hierarchical/dashboard_hierarchical.html', status:'online', views:9, lastAccess:'24/02/2026 16:40', type:'clustering', sections:['Dendrograma','Ward','Clusters']},
  { name:'Mixed Clustering — Dashboard', url:'../labs/mixed/dashboard_mixed.html', status:'online', views:8, lastAccess:'24/02/2026 16:40', type:'clustering', sections:['Ensemble','Comparativa','Clusters']},
  // ── EDA ──
  { name:'EDA — Dashboard Exploratorio', url:'../labs/eda/dashboard_eda.html', status:'online', views:31, lastAccess:'23/02/2026 14:20', type:'eda', sections:['Distribución','Correlaciones','Outliers']},
  { name:'EDA — Reporte Completo', url:'../labs/eda/dashboard_eda_report.html', status:'online', views:22, lastAccess:'23/02/2026 14:20', type:'eda', sections:['Variables','Estadísticos','Reporte']},
];
// Audit log: dinámico desde localStorage (registrado por auth.js)
const AUDIT_LOG = (() => {
  const stored = JSON.parse(localStorage.getItem('bcie_audit_log'));
  if (stored && stored.length > 0) return stored;
  // Fallback: datos demo iniciales
  return [
    { ts:'2026-02-26T19:49:00', level:'success', event:'Login exitoso', user:'waguilar', details:'Rol: Administrador' },
    { ts:'2026-02-26T18:10:12', level:'success', event:'Login exitoso', user:'admin', details:'Rol: Administrador' },
    { ts:'2026-02-26T18:05:44', level:'success', event:'Login exitoso', user:'bcie', details:'Redirigido a Dashboard Unificado' },
    { ts:'2026-02-26T17:58:01', level:'info', event:'Sistema inicializado', user:'system', details:'5 usuarios cargados' },
    { ts:'2026-02-26T17:55:30', level:'info', event:'CSRF token generado', user:'system', details:'Token: a3f2b8c1d4e5...' },
    { ts:'2026-02-26T14:26:00', level:'info', event:'Pipeline ETL completado', user:'system', details:'Bronze > Silver > Gold' },
    { ts:'2026-02-26T14:25:00', level:'info', event:'Datos actualizados', user:'system', details:'3,139 registros procesados' },
    { ts:'2026-02-25T20:30:00', level:'success', event:'Modelo entrenado', user:'admin', details:'NeuralProphet - MAPE: 7.1%' },
    { ts:'2026-02-25T19:15:00', level:'success', event:'Modelo entrenado', user:'admin', details:'Prophet - MAPE: 8.2%' },
    { ts:'2026-02-25T16:00:00', level:'warn', event:'Intento de login fallido', user:'unknown', details:'Usuario no encontrado' },
    { ts:'2026-02-24T16:40:00', level:'success', event:'Dashboard generado', user:'admin', details:'Dashboard Unificado actualizado' },
    { ts:'2026-02-24T15:00:00', level:'info', event:'Modelos clustering completados', user:'admin', details:'7 modelos entrenados' },
    { ts:'2026-02-23T14:20:00', level:'info', event:'EDA completado', user:'admin', details:'12 variables, 23 outliers' },
  ];
})();
const NOTIFICATIONS = [
  { id:1, type:'warn', text:'Intento de login fallido detectado', time:'Hace 2h', read:false },
  { id:2, type:'success', text:'Pipeline ETL completado exitosamente', time:'Hace 4h', read:false },
  { id:3, type:'info', text:'Nuevo usuario waguilar creado', time:'Hace 1h', read:false },
];
// Sesiones activas: dinámicas desde localStorage (registradas por auth.js)
const SESSIONS = (() => {
  const stored = JSON.parse(localStorage.getItem('bcie_active_sessions'));
  if (stored && stored.length > 0) {
    // Calcular duración para sesiones online
    return stored.map(s => {
      if (s.online && s.loginTime) {
        const elapsed = Date.now() - new Date(s.loginTime).getTime();
        const mins = Math.floor(elapsed / 60000);
        s.duration = mins < 60 ? `${mins}m` : `${Math.floor(mins/60)}h ${mins%60}m`;
      }
      return s;
    });
  }
  // Fallback: datos demo iniciales
  return [
    { user:'Norman Sabillon', username:'admin', role:'Administrador', ip:'192.168.1.10', started:'18:10', duration:'1h 44m', browser:'Chrome 122', online:true },
    { user:'Willson Aguilar', username:'waguilar', role:'Administrador', ip:'192.168.1.22', started:'19:49', duration:'5m', browser:'Firefox 124', online:true },
    { user:'Analista BCIE', username:'bcie', role:'Analista BCIE', ip:'10.0.0.45', started:'18:05', duration:'Sesión cerrada', browser:'Edge 122', online:false },
  ];
})();
const HEALTH = [
  { name:'API Datos Abiertos', status:'healthy', latency:'42ms', uptime:'99.97%', icon:'globe' },
  { name:'Auth Service', status:'healthy', latency:'12ms', uptime:'100%', icon:'lock' },
  { name:'ML Pipeline', status:'healthy', latency:'— ', uptime:'99.8%', icon:'cpu' },
  { name:'Session Store', status:'healthy', latency:'3ms', uptime:'100%', icon:'database' },
  { name:'Audit Logger', status:'healthy', latency:'8ms', uptime:'100%', icon:'file' },
  { name:'CSRF Protection', status:'healthy', latency:'1ms', uptime:'100%', icon:'shield' },
];
const ALERT_RULES = [
  { id:1, name:'MAPE > 10%', desc:'Alertar si algún modelo forecasting supera 10% MAPE', threshold:'10%', metric:'mape', enabled:true, triggered:false },
  { id:2, name:'Silhouette < 0.3', desc:'Alertar si algún modelo clustering baja de 0.3', threshold:'0.3', metric:'silhouette', enabled:true, triggered:false },
  { id:3, name:'Login fallido x3', desc:'Alertar después de 3 intentos fallidos consecutivos', threshold:'3', metric:'failed_logins', enabled:true, triggered:true },
  { id:4, name:'Uptime < 99%', desc:'Alertar si uptime de cualquier servicio baja del 99%', threshold:'99%', metric:'uptime', enabled:true, triggered:false },
  { id:5, name:'Sesión > 8hrs', desc:'Alertar si una sesión supera las 8 horas', threshold:'8h', metric:'session_duration', enabled:false, triggered:false },
];
const ALERT_HISTORY = [
  { ts:'2026-02-25T16:00:00', rule:'Login fallido x3', severity:'warn', details:'3 intentos fallidos desde IP 10.0.0.99', resolved:true },
  { ts:'2026-02-24T09:30:00', rule:'ML Pipeline', severity:'info', details:'Latencia elevada temporalmente (250ms)', resolved:true },
  { ts:'2026-02-23T22:15:00', rule:'Uptime < 99%', severity:'warn', details:'API Datos Abiertos — 98.7% por mantenimiento', resolved:true },
];

// ============================================
// Autenticación y cierre de sesión
// ============================================
(function checkAuth() {
  const auth = typeof SESSION_GUARD !== 'undefined' ? SESSION_GUARD.getAuthData() : null;
  if (!auth) {
    window.location.href = 'index.html';
    return;
  }
  // Guardia de rol: solo Administrador accede al panel
  if (auth.user.role !== 'Administrador') {
    alert('Acceso denegado. Solo usuarios con rol Administrador pueden acceder al Panel de Administración.');
    window.location.href = '../dashboard_unificado.html';
    return;
  }
  document.getElementById('navUserName').textContent = auth.user.displayName;
  // Inicializar guardia de sesión (timeout, rastreo inactividad)
  if (typeof SESSION_GUARD !== 'undefined') SESSION_GUARD.init();
})();
function handleLogout() {
  if (typeof SESSION_GUARD !== 'undefined') {
    SESSION_GUARD.forceLogout('user_logout');
  } else {
    sessionStorage.removeItem('bcie_auth');
    sessionStorage.removeItem('bcie_session');
    window.location.href = 'index.html';
  }
}

// ============================================
// Navegación por pestañas / Barra lateral
// ============================================
function showTab(id, btn) {
  document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.sidebar-item').forEach(b => b.classList.remove('active'));
  document.getElementById('tab-' + id).classList.add('active');
  if (btn) btn.classList.add('active');
  else document.querySelector(`[data-tab="${id}"]`)?.classList.add('active');
  document.getElementById('bcCurrent').textContent = t('tab.' + id) || id;
  document.getElementById('sidebar').classList.remove('open');
  document.getElementById('sidebarOverlay').classList.remove('visible');
  if (id === 'overview') renderCharts();
  if (id === 'health') renderUptimeChart();
  if (id === 'models') { renderComparison(); renderClusteringComp(); }
}
function toggleSidebar() {
  document.getElementById('sidebar').classList.toggle('open');
  document.getElementById('sidebarOverlay').classList.toggle('visible');
}
// ============================================
// Colapso de barra lateral
// ============================================
function toggleSidebarCollapse() {
  const sb = document.getElementById('sidebar');
  sb.classList.toggle('collapsed');
  const bc = document.getElementById('breadcrumbs');
  const collapsed = sb.classList.contains('collapsed');
  bc.style.paddingLeft = collapsed ? 'calc(58px + 1.5rem)' : '';
  localStorage.setItem('bcie-sidebar-collapsed', collapsed ? '1' : '0');
}
(function loadSidebarState(){
  if(localStorage.getItem('bcie-sidebar-collapsed')==='1'){
    const sb=document.getElementById('sidebar');
    if(sb){sb.classList.add('collapsed');document.getElementById('breadcrumbs').style.paddingLeft='calc(58px + 1.5rem)';}
  }
})();

// ============================================
// Alternador de tema claro/oscuro
// ============================================
function toggleTheme() {
  const html = document.documentElement;
  const current = html.getAttribute('data-theme');
  const next = current === 'dark' ? 'light' : 'dark';
  html.setAttribute('data-theme', next);
  localStorage.setItem('bcie-theme', next);
  document.querySelector('.theme-icon-dark').style.display = next === 'dark' ? 'block' : 'none';
  document.querySelector('.theme-icon-light').style.display = next === 'light' ? 'block' : 'none';
  renderCharts();
}
(function loadTheme() {
  const saved = localStorage.getItem('bcie-theme') || 'light';
  document.documentElement.setAttribute('data-theme', saved);
  if (saved === 'light') { document.querySelector('.theme-icon-dark').style.display='none'; document.querySelector('.theme-icon-light').style.display='block'; }
  else { document.querySelector('.theme-icon-dark').style.display='block'; document.querySelector('.theme-icon-light').style.display='none'; }
})();

// ============================================
// Búsqueda global
// ============================================
function handleSearch(q) {
  const box = document.getElementById('searchResults');
  if (!q || q.length < 2) { box.classList.remove('visible'); return; }
  const ql = q.toLowerCase();
  let results = [];
  USERS.forEach(u => { if (u.username.includes(ql) || u.displayName.toLowerCase().includes(ql)) results.push({ type:'user', label:u.displayName, sub:u.username, tab:'users' }); });
  MODELS.forEach(m => { if (m.name.toLowerCase().includes(ql) || m.type.includes(ql)) results.push({ type:'model', label:m.name, sub:m.type, tab:'models' }); });
  AUDIT_LOG.forEach(e => { if (e.event.toLowerCase().includes(ql) || e.details.toLowerCase().includes(ql)) results.push({ type:'event', label:e.event, sub:e.details.slice(0,40), tab:'audit' }); });
  if (results.length === 0) { box.innerHTML = `<div class="sr-item" style="color:var(--text-dim)">${t('search.noresults')}</div>`; } else {
    box.innerHTML = results.slice(0,8).map(r => `<div class="sr-item" onclick="showTab('${r.tab}');document.getElementById('searchResults').classList.remove('visible');document.getElementById('globalSearch').value=''"><span class="sr-type ${r.type}">${r.type}</span><span>${r.label}</span><span style="color:var(--text-dim);font-size:.7rem;margin-left:auto">${r.sub}</span></div>`).join('');
  }
  box.classList.add('visible');
}
document.addEventListener('click', e => { if (!e.target.closest('.search-bar')) document.getElementById('searchResults').classList.remove('visible'); });

// ============================================
// Notificaciones
// ============================================
function toggleNotifications() { document.getElementById('notifDropdown').classList.toggle('visible'); }
function renderNotifications() {
  const dd = document.getElementById('notifDropdown');
  const colors = { warn:'#f59e0b', success:'#22c55e', info:'#3b82f6', error:'#ef4444' };
  dd.innerHTML = `<div class="notif-header">${t('notif.title')}</div>` + NOTIFICATIONS.map(n =>
    `<div class="notif-item"><div class="notif-dot" style="background:${colors[n.type]||'#64748b'}"></div><div class="notif-text"><div>${n.text}</div><div class="notif-time">${n.time}</div></div></div>`
  ).join('');
}
document.addEventListener('click', e => { if (!e.target.closest('.notif-wrapper')) document.getElementById('notifDropdown').classList.remove('visible'); });

// ============================================
// Carga esquelética (animación placeholder)
// ============================================
function showSkeleton() {
  const sk = document.getElementById('skeletonOverview');
  const oc = document.getElementById('overviewContent');
  if (sk && oc) { sk.style.display = 'block'; oc.style.display = 'none'; }
}
function hideSkeleton() {
  const sk = document.getElementById('skeletonOverview');
  const oc = document.getElementById('overviewContent');
  if (sk && oc) { sk.style.display = 'none'; oc.style.display = 'block'; }
}

// ============================================
// Renderizado: Resumen general
// ============================================
function renderOverview() {
  const el = document.getElementById('recentActivity');
  el.innerHTML = AUDIT_LOG.slice(0,6).map(e => {
    const d = new Date(e.ts); const ti = d.toLocaleTimeString('es-HN',{hour12:false,hour:'2-digit',minute:'2-digit'}); const day=d.toLocaleDateString('es-HN',{day:'2-digit',month:'2-digit'});
    return `<div class="activity-item ${e.level}"><span class="activity-time">${day} ${ti}</span><span>${e.event}</span></div>`;
  }).join('');
}

// ============================================
// Gráficos (Chart.js)
// ============================================
let loginsChartInst, modelsChartInst;
function renderCharts() {
  const isDark = document.documentElement.getAttribute('data-theme') !== 'light';
  const gridColor = isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.06)';
  const textColor = isDark ? '#94a3b8' : '#64748b';
  const ctx1 = document.getElementById('loginsChart');
  if (loginsChartInst) loginsChartInst.destroy();
  loginsChartInst = new Chart(ctx1, { type:'bar', data:{ labels:['20/02','21/02','22/02','23/02','24/02','25/02','26/02'], datasets:[{ label:'Logins', data:[2,1,3,2,4,5,6], backgroundColor:'rgba(6,182,212,0.5)', borderColor:'#06b6d4', borderWidth:1, borderRadius:4 }] }, options:{ responsive:true, maintainAspectRatio:false, plugins:{legend:{display:false}}, scales:{ y:{grid:{color:gridColor},ticks:{color:textColor,font:{size:10}}}, x:{grid:{display:false},ticks:{color:textColor,font:{size:10}}} } } });
  const ctx2 = document.getElementById('modelsTypeChart');
  if (modelsChartInst) modelsChartInst.destroy();
  modelsChartInst = new Chart(ctx2, { type:'doughnut', data:{ labels:['Forecasting','Clustering','EDA'], datasets:[{ data:[4,7,1], backgroundColor:['#06b6d4','#a855f7','#f59e0b'], borderWidth:0 }] }, options:{ responsive:true, maintainAspectRatio:false, plugins:{ legend:{ position:'bottom', labels:{ color:textColor, font:{size:11}, padding:12 } } } } });
}

// ============================================
// Renderizado: Usuarios + Historial
// ============================================
function renderUsers() {
  const iconEdit = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>';
  const iconTrash = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/><line x1="10" y1="11" x2="10" y2="17"/><line x1="14" y1="11" x2="14" y2="17"/></svg>';
  const iconKey = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16" stroke-linecap="round" stroke-linejoin="round"><path d="M21 2l-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.778 7.778 5.5 5.5 0 0 1 7.777-7.777zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3m-3.5 3.5L19 4"/></svg>';
  const iconHistory = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>';
  const iconToggle = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16" stroke-linecap="round" stroke-linejoin="round"><path d="M18.36 6.64a9 9 0 1 1-12.73 0"/><line x1="12" y1="2" x2="12" y2="12"/></svg>';
  const btnStyle = 'display:inline-flex;align-items:center;justify-content:center;width:34px;height:34px;border-radius:8px;border:1px solid;cursor:pointer;transition:all .2s;';
  document.querySelector('#usersTable tbody').innerHTML = USERS.map(u => `<tr>
    <td class="text-accent" style="font-weight:600">${u.username}</td>
    <td>${u.displayName}</td>
    <td><span style="font-size:.78rem;padding:2px 8px;border-radius:4px;background:${u.role==='Administrador'?'rgba(168,85,247,.15)':'rgba(6,182,212,.15)'};color:${u.role==='Administrador'?'#a855f7':'#06b6d4'}">${u.role}</span></td>
    <td><span class="status-badge ${u.status==='active'?'ok':'inactive'}">${u.status==='active'?t('users.active'):t('users.inactive')}</span></td>
    <td style="font-size:.78rem;color:var(--text-muted)">${u.lastAccess}</td>
    <td>
      <div style="display:flex;gap:6px;align-items:center">
        <button onclick="editUser(${u.id})" title="${t('users.edit')}" style="${btnStyle}background:rgba(59,130,246,.1);border-color:rgba(59,130,246,.3);color:#3b82f6">${iconEdit}</button>
        <button onclick="resetPassword(${u.id})" title="${t('users.reset')}" style="${btnStyle}background:rgba(245,158,11,.1);border-color:rgba(245,158,11,.3);color:#f59e0b">${iconKey}</button>
        <button onclick="showUserHistory('${u.username}')" title="${t('users.viewhistory')}" style="${btnStyle}background:rgba(6,182,212,.1);border-color:rgba(6,182,212,.3);color:#06b6d4">${iconHistory}</button>
        <button onclick="deleteUser(${u.id})" title="${t('modal.deleteuser')}" style="${btnStyle}background:rgba(239,68,68,.1);border-color:rgba(239,68,68,.3);color:#ef4444">${iconTrash}</button>
        <button onclick="toggleUser(${u.id})" title="${u.status==='active'?t('users.deactivate'):t('users.activate')}" style="${btnStyle}background:${u.status==='active'?'rgba(34,197,94,.1)':'rgba(156,163,175,.1)'};border-color:${u.status==='active'?'rgba(34,197,94,.3)':'rgba(156,163,175,.3)'};color:${u.status==='active'?'#22c55e':'#9ca3af'}">${iconToggle}</button>
      </div>
    </td>
  </tr>`).join('');
}
function showUserHistory(username) {
  const card = document.getElementById('userHistoryCard');
  const content = document.getElementById('userHistoryContent');
  const events = AUDIT_LOG.filter(e => e.user === username);
  if (events.length === 0) {
    content.innerHTML = `<div style="padding:.5rem;color:var(--text-dim);font-size:.78rem">${t('search.noresults')}</div>`;
  } else {
    const m = {success:'ok',info:'info',warn:'warn',error:'error'};
    content.innerHTML = `<table class="data-table"><thead><tr><th>Timestamp</th><th>${t('audit.level')}</th><th>${t('audit.event')}</th><th>${t('modal.details')}</th></tr></thead><tbody>` +
      events.map(e => {
        const dt=new Date(e.ts); const ts=dt.toLocaleDateString('es-HN')+' '+dt.toLocaleTimeString('es-HN',{hour12:false});
        return `<tr><td style="white-space:nowrap;font-family:monospace;font-size:.72rem">${ts}</td><td><span class="status-badge ${m[e.level]||'info'}">${e.level.toUpperCase()}</span></td><td>${e.event}</td><td style="color:var(--text-muted);font-size:.75rem">${e.details}</td></tr>`;
      }).join('') + '</tbody></table>';
  }
  card.style.display = 'block';
  card.scrollIntoView({ behavior:'smooth', block:'start' });
}

// ============================================
// Renderizado: Modelos ML con tooltips
// ============================================
const METRIC_TOOLTIPS = { mape:'tooltip.mape', rmse:'tooltip.rmse', r2:'tooltip.r2', silhouette:'tooltip.silhouette', clusters:'tooltip.clusters', inertia:'tooltip.inertia' };
function renderModels(filter='all') {
  const grid = document.getElementById('modelsGrid');
  const filtered = filter==='all' ? MODELS : MODELS.filter(m=>m.type===filter);
  const typeColors = {forecasting:'#06b6d4',clustering:'#a855f7',eda:'#f59e0b'};
  grid.innerHTML = filtered.map((m,i) => {
    const c = typeColors[m.type]||'#64748b';
    const metricsHtml = Object.entries(m.metrics).map(([k,v])=>{
      const tip = METRIC_TOOLTIPS[k] ? ` class="tooltip-trigger" data-tooltip="${t(METRIC_TOOLTIPS[k])}"` : '';
      return `<div class="metric-row"><span${tip}>${k}</span><span>${v}</span></div>`;
    }).join('');
    return `<div class="model-card"><div class="model-name">${m.name}</div><div class="model-type" style="color:${c}">${m.type}</div><div class="model-metrics">${metricsHtml}</div><div class="model-footer"><span class="status-badge ok">${m.status}</span><div style="display:flex;gap:5px"><button class="btn-sm" onclick="event.stopPropagation();openModelDetail(${MODELS.indexOf(m)})">${t('models.detail')}</button><button class="btn-sm" onclick="event.stopPropagation();window.open('${m.dashUrl}','_blank')" style="border-color:var(--accent);color:var(--accent)">${t('models.viewdash')}</button></div></div></div>`;
  }).join('');
}
function filterModels() { renderModels(document.getElementById('modelTypeFilter').value); }

function openModelDetail(idx) {
  const m = MODELS[idx];
  const typeColors = {forecasting:'#06b6d4',clustering:'#a855f7',eda:'#f59e0b'};
  const c = typeColors[m.type] || '#64748b';
  document.getElementById('modalTitle').textContent = m.name;
  document.getElementById('modalBody').innerHTML = `
    <div style="margin-bottom:.8rem"><span class="status-badge" style="background:${c}22;color:${c};border:1px solid ${c}44">${m.type.toUpperCase()}</span> <span class="status-badge ok">${m.status}</span></div>
    <h4 style="font-size:.8rem;color:var(--text-muted);margin-bottom:.5rem">${t('modal.metrics')}</h4>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:.5rem;margin-bottom:1rem">${Object.entries(m.metrics).map(([k,v])=>`<div style="background:var(--bg-input);padding:.5rem;border-radius:6px;text-align:center"><div style="font-size:.65rem;color:var(--text-muted);text-transform:uppercase">${k}</div><div style="font-size:1.1rem;font-weight:800;color:var(--text)">${v}</div></div>`).join('')}</div>
    <h4 style="font-size:.8rem;color:var(--text-muted);margin-bottom:.5rem">${t('modal.details')}</h4>
    <div style="font-size:.78rem"><div class="data-row"><span>${t('modal.folder')}</span><span>${m.folder}</span></div><div class="data-row"><span>${t('modal.trained')}</span><span>${m.trained}</span></div><div class="data-row"><span>${t('modal.dataset')}</span><span>3,139 aprobaciones BCIE</span></div></div>
    <div style="margin-top:1rem;display:flex;justify-content:flex-end"><button class="btn-primary" onclick="window.open('${m.dashUrl}','_blank')">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
      ${t('models.viewdash')}</button></div>`;
  document.getElementById('modalOverlay').classList.add('visible');
}

// ============================================
// Gráfico comparativo de modelos
// ============================================
let comparisonChartInst;
function renderComparison() {
  const type = document.getElementById('comparisonTypeFilter')?.value || 'forecasting';
  const filtered = MODELS.filter(m => m.type === type);
  const ctx = document.getElementById('comparisonChart');
  if (!ctx) return;
  const isDark = document.documentElement.getAttribute('data-theme') !== 'light';
  const textColor = isDark ? '#94a3b8' : '#64748b';
  const gridColor = isDark ? 'rgba(255,255,255,.06)' : 'rgba(0,0,0,.06)';
  if (comparisonChartInst) comparisonChartInst.destroy();

  if (type === 'forecasting') {
    const labels = filtered.map(m => m.name);
    const mapeData = filtered.map(m => parseFloat(m.metrics.mape));
    const r2Data = filtered.map(m => parseFloat(m.metrics.r2) * 100);
    comparisonChartInst = new Chart(ctx, { type:'bar', data:{ labels,
      datasets:[
        { label:'MAPE %', data:mapeData, backgroundColor:'rgba(239,68,68,.5)', borderColor:'#ef4444', borderWidth:1, borderRadius:4, yAxisID:'y' },
        { label:'R² (×100)', data:r2Data, backgroundColor:'rgba(34,197,94,.5)', borderColor:'#22c55e', borderWidth:1, borderRadius:4, yAxisID:'y1' }
      ] }, options:{ responsive:true, maintainAspectRatio:false, plugins:{legend:{labels:{color:textColor,font:{size:11}}}},
        scales:{ y:{position:'left',grid:{color:gridColor},ticks:{color:textColor,font:{size:10},callback:v=>v+'%'},title:{display:true,text:'MAPE %',color:textColor}},
                 y1:{position:'right',grid:{display:false},ticks:{color:textColor,font:{size:10}},title:{display:true,text:'R² ×100',color:textColor}},
                 x:{grid:{display:false},ticks:{color:textColor,font:{size:10}}} } } });
  } else {
    const labels = filtered.map(m => m.name);
    const silData = filtered.map(m => parseFloat(m.metrics.silhouette));
    comparisonChartInst = new Chart(ctx, { type:'bar', data:{ labels,
      datasets:[{ label:'Silhouette', data:silData, backgroundColor:filtered.map((_,i)=>`hsla(${270+i*15},60%,60%,.5)`), borderColor:filtered.map((_,i)=>`hsl(${270+i*15},60%,50%)`), borderWidth:1, borderRadius:4 }]
    }, options:{ responsive:true, maintainAspectRatio:false, indexAxis:'y',
        plugins:{legend:{display:false}},
        scales:{ x:{grid:{color:gridColor},ticks:{color:textColor,font:{size:10}},min:0,max:0.6}, y:{grid:{display:false},ticks:{color:textColor,font:{size:10}}} } } });
  }
}

// ============================================
// Gráfico comparativo de clustering (Silhouette)
// ============================================
let clusteringCompInst;
function renderClusteringComp() {
  const ctx = document.getElementById('clusteringCompChart');
  if (!ctx) return;
  const isDark = document.documentElement.getAttribute('data-theme') !== 'light';
  const textColor = isDark ? '#94a3b8' : '#64748b';
  const gridColor = isDark ? 'rgba(255,255,255,.06)' : 'rgba(0,0,0,.06)';
  if (clusteringCompInst) clusteringCompInst.destroy();
  const clustering = MODELS.filter(m => m.type === 'clustering').sort((a,b) => parseFloat(b.metrics.silhouette) - parseFloat(a.metrics.silhouette));
  const labels = clustering.map(m => m.name);
  const silData = clustering.map(m => parseFloat(m.metrics.silhouette));
  clusteringCompInst = new Chart(ctx, { type:'bar', data:{ labels,
    datasets:[{ label:'Silhouette', data:silData, backgroundColor:clustering.map((_,i)=>`hsla(${270+i*15},60%,60%,.5)`), borderColor:clustering.map((_,i)=>`hsl(${270+i*15},60%,50%)`), borderWidth:1, borderRadius:4 }]
  }, options:{ responsive:true, maintainAspectRatio:false, indexAxis:'y',
      plugins:{legend:{display:false}},
      scales:{ x:{grid:{color:gridColor},ticks:{color:textColor,font:{size:10}},min:0,max:0.6}, y:{grid:{display:false},ticks:{color:textColor,font:{size:10}}} } } });
}

// ============================================
// Renderizado: Dashboards
// ============================================
function renderDashboards() {
  const typeColors = {unificado:'#f59e0b',forecasting:'#06b6d4',clustering:'#a855f7',eda:'#22c55e'};
  document.getElementById('dashboardsGrid').innerHTML = DASHBOARDS.map(d => {
    const c = typeColors[d.type] || '#64748b';
    return `<div class="dash-card ${d.status}">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">
      <div class="dash-name" style="font-size:.85rem">${d.name}</div>
      <span style="padding:2px 7px;background:${c}22;color:${c};border:1px solid ${c}44;border-radius:4px;font-size:.6rem;font-weight:700;text-transform:uppercase">${d.type||'—'}</span>
    </div>
    <div class="dash-meta">
    <div class="dash-meta-row"><span>Estado</span><span class="status-badge ${d.status==='online'?'ok':'error'}">${d.status==='online'?'Online':'Offline'}</span></div>
    <div class="dash-meta-row"><span>Vistas</span><span>${d.views}</span></div>
    <div class="dash-meta-row"><span>Último acceso</span><span>${d.lastAccess}</span></div></div>
    <div style="margin-top:.6rem;display:flex;flex-wrap:wrap;gap:3px">${d.sections.map(s=>`<span style="padding:2px 6px;background:${c}11;border:1px solid ${c}22;border-radius:3px;font-size:.63rem;color:${c}">${s}</span>`).join('')}</div>
    <div style="margin-top:.6rem;text-align:right"><button class="btn-sm" onclick="window.open('${d.url}','_blank')" style="border-color:${c};color:${c}">Abrir ↗</button></div>
  </div>`}).join('');
}

// ============================================
// Renderizado: Auditoría
// ============================================
function renderAudit(filter='all') {
  const filtered = filter==='all' ? AUDIT_LOG : AUDIT_LOG.filter(e=>e.level===filter);
  const m = {success:'ok',info:'info',warn:'warn',error:'error'};
  document.querySelector('#auditTable tbody').innerHTML = filtered.map(e => {
    const dt=new Date(e.ts); const ts=dt.toLocaleDateString('es-HN')+' '+dt.toLocaleTimeString('es-HN',{hour12:false});
    return `<tr><td style="white-space:nowrap;font-family:monospace;font-size:.72rem">${ts}</td><td><span class="status-badge ${m[e.level]||'info'}">${e.level.toUpperCase()}</span></td><td>${e.event}</td><td class="text-accent">${e.user}</td><td style="color:var(--text-muted);font-size:.75rem">${e.details}</td></tr>`;
  }).join('');
}
function filterAudit() { renderAudit(document.getElementById('auditLevelFilter').value); }
function exportAuditLog() {
  const csv='Timestamp,Nivel,Evento,Usuario,Detalles\n'+AUDIT_LOG.map(e=>`"${e.ts}","${e.level}","${e.event}","${e.user}","${e.details}"`).join('\n');
  const a=document.createElement('a'); a.href=URL.createObjectURL(new Blob([csv],{type:'text/csv'})); a.download=`bcie_audit_log_${new Date().toISOString().slice(0,10)}.csv`; a.click();
}

// ============================================
// Renderizado: Sesiones activas
// ============================================
function renderSessions() {
  document.getElementById('sessionsGrid').innerHTML = SESSIONS.map(s => `
    <div class="session-card ${s.online?'online':''}">
      <div class="session-avatar">${s.user.charAt(0)}</div>
      <div class="session-info"><div class="session-name">${s.user}</div><div class="session-details">
        <span>@${s.username} - ${s.role}</span><span>IP: ${s.ip} | ${s.browser}</span>
        <span>${t('sessions.start')}: ${s.started} | ${t('sessions.duration')}: ${s.duration}</span></div></div>
      ${s.online ? '<div class="session-pulse"></div>' : `<span class="status-badge inactive">${t('sessions.offline')}</span>`}
    </div>`).join('');
}

// ============================================
// Renderizado: Salud del sistema
// ============================================
const HEALTH_ICONS = {
  globe:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="22" height="22" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>',
  lock:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="22" height="22" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>',
  cpu:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="22" height="22" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2" ry="2"/><rect x="9" y="9" width="6" height="6"/><line x1="9" y1="1" x2="9" y2="4"/><line x1="15" y1="1" x2="15" y2="4"/><line x1="9" y1="20" x2="9" y2="23"/><line x1="15" y1="20" x2="15" y2="23"/><line x1="20" y1="9" x2="23" y2="9"/><line x1="20" y1="14" x2="23" y2="14"/><line x1="1" y1="9" x2="4" y2="9"/><line x1="1" y1="14" x2="4" y2="14"/></svg>',
  database:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="22" height="22" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg>',
  file:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="22" height="22" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>',
  shield:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="22" height="22" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>'
};
function renderHealth() {
  const statusLabel = {healthy:t('health.healthy'),degraded:t('health.degraded'),down:t('health.down')};
  document.getElementById('healthGrid').innerHTML = HEALTH.map(h => `
    <div class="health-card ${h.status}"><div class="health-icon">${HEALTH_ICONS[h.icon]||''}</div>
    <div class="health-name">${h.name}</div>
    <div class="health-status" style="color:${h.status==='healthy'?'#22c55e':h.status==='degraded'?'#f59e0b':'#ef4444'}">${statusLabel[h.status]}</div>
    <div class="health-meta">${t('health.latency')}: ${h.latency} | ${t('health.uptimepct')}: ${h.uptime}</div></div>`).join('');
}
let uptimeChartInst;
function renderUptimeChart() {
  const ctx = document.getElementById('uptimeChart');
  if (!ctx) return;
  const isDark = document.documentElement.getAttribute('data-theme') !== 'light';
  if (uptimeChartInst) uptimeChartInst.destroy();
  uptimeChartInst = new Chart(ctx, { type:'line', data:{ labels:['Lun','Mar','Mié','Jue','Vie','Sáb','Dom'], datasets:[{ label:'Uptime %', data:[99.9,100,99.8,100,100,99.97,100], borderColor:'#22c55e', backgroundColor:'rgba(34,197,94,0.1)', fill:true, tension:0.3, pointRadius:4, pointBackgroundColor:'#22c55e' }] }, options:{ responsive:true, maintainAspectRatio:false, plugins:{legend:{display:false}}, scales:{ y:{min:99,max:100.1,grid:{color: isDark?'rgba(255,255,255,.06)':'rgba(0,0,0,.06)'},ticks:{color: isDark?'#94a3b8':'#64748b',font:{size:10},callback:v=>v+'%'}}, x:{grid:{display:false},ticks:{color: isDark?'#94a3b8':'#64748b',font:{size:10}}} } } });
}

// ============================================
// Alertas programables
// ============================================
function renderAlerts() {
  const rulesEl = document.getElementById('alertRules');
  const histEl = document.getElementById('alertHistory');
  rulesEl.innerHTML = ALERT_RULES.map(r => `
    <div class="alert-rule">
      <div class="ar-dot ${r.enabled?'on':'off'}"></div>
      <div class="ar-name">${r.name} ${r.triggered?'<span class="status-badge warn">'+t('alerts.triggered')+'</span>':''}</div>
      <div class="ar-thresh">${t('alerts.thresh')}: ${r.threshold}</div>
      <div style="display:flex;gap:4px">
        <button class="btn-sm" onclick="toggleAlertRule(${r.id})">${r.enabled?t('alerts.enabled'):t('alerts.disabled')}</button>
      </div>
    </div>`).join('');

  const m = {warn:'warn',info:'info',error:'error'};
  histEl.innerHTML = `<table class="data-table"><thead><tr><th>Timestamp</th><th>Regla</th><th>${t('audit.level')}</th><th>${t('modal.details')}</th><th>Estado</th></tr></thead><tbody>` +
    ALERT_HISTORY.map(a => {
      const dt=new Date(a.ts); const ts=dt.toLocaleDateString('es-HN')+' '+dt.toLocaleTimeString('es-HN',{hour12:false});
      return `<tr><td style="white-space:nowrap;font-family:monospace;font-size:.72rem">${ts}</td><td class="text-accent">${a.rule}</td><td><span class="status-badge ${m[a.severity]||'info'}">${a.severity.toUpperCase()}</span></td><td style="color:var(--text-muted);font-size:.75rem">${a.details}</td><td><span class="status-badge ok">Resuelto</span></td></tr>`;
    }).join('') + '</tbody></table>';
}
function toggleAlertRule(id) {
  const rule = ALERT_RULES.find(r=>r.id===id);
  if(rule) { rule.enabled = !rule.enabled; renderAlerts(); }
}

// ============================================
// Exportar reporte del sistema
// ============================================
function exportSystemReport() {
  const now = new Date().toISOString().slice(0,19).replace('T',' ');
  let report = `BCIE ML Lab - Reporte del Sistema\nGenerado: ${now}\n${'='.repeat(50)}\n\n`;
  report += `USUARIOS (${USERS.length})\n${'-'.repeat(30)}\n`;
  USERS.forEach(u => report += `  ${u.username.padEnd(12)} ${u.displayName.padEnd(20)} ${u.role.padEnd(16)} ${u.status}\n`);
  report += `\nMODELOS ML (${MODELS.length})\n${'-'.repeat(30)}\n`;
  MODELS.forEach(m => report += `  ${m.name.padEnd(18)} ${m.type.padEnd(14)} ${m.status}\n`);
  report += `\nDASHBOARDS (${DASHBOARDS.length})\n${'-'.repeat(30)}\n`;
  DASHBOARDS.forEach(d => report += `  ${d.name.padEnd(35)} ${d.status}\n`);
  report += `\nHEALTH CHECK\n${'-'.repeat(30)}\n`;
  HEALTH.forEach(h => report += `  ${h.name.padEnd(20)} ${h.status.padEnd(10)} Latencia: ${h.latency}\n`);
  report += `\nALERT RULES (${ALERT_RULES.length})\n${'-'.repeat(30)}\n`;
  ALERT_RULES.forEach(r => report += `  ${r.name.padEnd(20)} ${r.enabled?'ON':'OFF'}  Threshold: ${r.threshold}\n`);
  report += `\nAUDIT LOG (últimos ${AUDIT_LOG.length} eventos)\n${'-'.repeat(30)}\n`;
  AUDIT_LOG.forEach(e => report += `  ${e.ts}  [${e.level.toUpperCase().padEnd(7)}] ${e.event} - ${e.user}\n`);
  const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([report],{type:'text/plain'})); a.download = `bcie_system_report_${new Date().toISOString().slice(0,10)}.txt`; a.click();
}

// ============================================
// Modal (CRUD de usuarios)
// ============================================
function openModal(type) {
  const body = document.getElementById('modalBody'); const title = document.getElementById('modalTitle');
  if (type === 'addUser') {
    title.textContent = t('modal.adduser');
    body.innerHTML = `<div class="form-field"><label>${t('modal.username')}</label><input type="text" id="newUsername" placeholder="ej: analista01"></div>
    <div class="form-field"><label>${t('modal.fullname')}</label><input type="text" id="newDisplayName" placeholder="ej: Juan Pérez"></div>
    <div class="form-field"><label>${t('modal.role')}</label><select id="newRole"><option>Analista BCIE</option><option>Administrador</option><option>Viewer</option></select></div>
    <div class="form-field"><label>${t('modal.password')}</label><input type="password" id="newPassword" placeholder="Mínimo 6 caracteres"></div>
    <div style="display:flex;gap:6px;justify-content:flex-end;margin-top:.8rem"><button class="btn-secondary" onclick="closeModal()">${t('modal.cancel')}</button><button class="btn-primary" onclick="addUser()">${t('modal.create')}</button></div>`;
  }
  if (type === 'addAlert') {
    title.textContent = t('alerts.add');
    body.innerHTML = `<div class="form-field"><label>Nombre de la regla</label><input type="text" id="newAlertName" placeholder="ej: MAPE > 15%"></div>
    <div class="form-field"><label>Métrica</label><select id="newAlertMetric"><option value="mape">MAPE</option><option value="silhouette">Silhouette</option><option value="uptime">Uptime</option><option value="failed_logins">Failed Logins</option></select></div>
    <div class="form-field"><label>Umbral</label><input type="text" id="newAlertThreshold" placeholder="ej: 15%"></div>
    <div class="form-field"><label>Descripción</label><input type="text" id="newAlertDesc" placeholder="Descripción de la alerta"></div>
    <div style="display:flex;gap:6px;justify-content:flex-end;margin-top:.8rem"><button class="btn-secondary" onclick="closeModal()">${t('modal.cancel')}</button><button class="btn-primary" onclick="addAlert()">${t('modal.create')}</button></div>`;
  }
  document.getElementById('modalOverlay').classList.add('visible');
}
function closeModal() { document.getElementById('modalOverlay').classList.remove('visible'); }
async function addUser() {
  const u=document.getElementById('newUsername').value.trim(), n=document.getElementById('newDisplayName').value.trim(), r=document.getElementById('newRole').value;
  const pw=document.getElementById('newPassword').value;
  if (!u||!n||!pw) return alert('Completa todos los campos, incluyendo la contraseña.');
  if (pw.length < 6) return alert('La contraseña debe tener mínimo 6 caracteres.');
  
  USERS.push({id:USERS.length+1,username:u,displayName:n,role:r,status:'active',lastAccess:'—',created:new Date().toLocaleDateString('es-HN')});
  saveUsersData();
  
  const hash = await hashBciePassword(pw);
  let authStore = JSON.parse(localStorage.getItem('bcie_auth_store')) || {};
  authStore[u.toLowerCase()] = { username: u, passwordHash: hash, role: r, displayName: n };
  localStorage.setItem('bcie_auth_store', JSON.stringify(authStore));

  renderUsers(); closeModal(); document.getElementById('kpiUsers').textContent = USERS.filter(x=>x.status==='active').length;
}
function addAlert() {
  const name=document.getElementById('newAlertName').value.trim();
  const metric=document.getElementById('newAlertMetric').value;
  const threshold=document.getElementById('newAlertThreshold').value.trim();
  const desc=document.getElementById('newAlertDesc').value.trim()||name;
  if(!name||!threshold) return alert('Completa nombre y umbral.');
  ALERT_RULES.push({id:ALERT_RULES.length+1,name,desc,threshold,metric,enabled:true,triggered:false});
  renderAlerts(); closeModal();
}
function editUser(id) {
  const u = USERS.find(x => x.id === id);
  if (!u) return;
  const body = document.getElementById('modalBody'); const title = document.getElementById('modalTitle');
  title.textContent = t('modal.edituser') + ': ' + u.username;
  const roles = ['Administrador', 'Analista BCIE', 'Viewer'];
  const statuses = [{val:'active',label:t('users.active')},{val:'inactive',label:t('users.inactive')}];
  body.innerHTML = `
    <div style="display:flex;align-items:center;gap:1rem;margin-bottom:1.2rem;padding-bottom:.8rem;border-bottom:1px solid var(--border)">
      <div style="width:52px;height:52px;border-radius:50%;background:linear-gradient(135deg,var(--accent),#a855f7);display:flex;align-items:center;justify-content:center;color:#fff;font-weight:800;font-size:1.2rem;flex-shrink:0">${u.displayName.charAt(0)}</div>
      <div>
        <div style="font-weight:700;font-size:1rem;color:var(--text)">${u.displayName}</div>
        <div style="font-size:.72rem;color:var(--text-muted)">@${u.username} · ${t('modal.created')}: ${u.created}</div>
        <div style="margin-top:3px"><span class="status-badge ${u.status==='active'?'ok':'inactive'}">${u.status==='active'?t('users.active'):t('users.inactive')}</span></div>
      </div>
    </div>
    <div class="form-field">
      <label>${t('modal.username')}</label>
      <input type="text" id="editUsername" value="${u.username}" maxlength="30">
    </div>
    <div class="form-field">
      <label>${t('modal.fullname')}</label>
      <input type="text" id="editDisplayName" value="${u.displayName}" maxlength="60">
    </div>
    <div class="form-field">
      <label>${t('modal.role')}</label>
      <select id="editRole">
        ${roles.map(r => `<option ${r===u.role?'selected':''}>${r}</option>`).join('')}
      </select>
    </div>
    <div class="form-field">
      <label>${t('users.status')}</label>
      <select id="editStatus">
        ${statuses.map(s => `<option value="${s.val}" ${s.val===u.status?'selected':''}>${s.label}</option>`).join('')}
      </select>
    </div>
    <div style="display:flex;gap:6px;justify-content:space-between;align-items:center;margin-top:1rem;padding-top:.8rem;border-top:1px solid var(--border)">
      <button class="btn-sm danger" onclick="deleteUser(${u.id})" style="color:#ef4444;border-color:rgba(239,68,68,.3)">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
        ${t('modal.deleteuser')}
      </button>
      <div style="display:flex;gap:6px">
        <button class="btn-secondary" onclick="closeModal()">${t('modal.cancel')}</button>
        <button class="btn-primary" onclick="saveUser(${u.id})">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>
          ${t('modal.save')}
        </button>
      </div>
    </div>`;
  document.getElementById('modalOverlay').classList.add('visible');
}

function saveUser(id) {
  const u = USERS.find(x => x.id === id);
  if (!u) return;
  const newUsername = document.getElementById('editUsername').value.trim().replace(/[^a-zA-Z0-9_.]/g, '');
  const newName = document.getElementById('editDisplayName').value.trim().replace(/[<>"'&]/g, '');
  const newRole = document.getElementById('editRole').value;
  const newStatus = document.getElementById('editStatus').value;
  if (!newUsername || !newName) return showToast('Completa todos los campos', 'warn');
  
  const oldUserKey = u.username.toLowerCase();
  
  u.username = newUsername;
  u.displayName = newName;
  u.role = newRole;
  u.status = newStatus;
  saveUsersData();

  let authStore = JSON.parse(localStorage.getItem('bcie_auth_store')) || {};
  if (authStore[oldUserKey] || true) {
    const data = authStore[oldUserKey] || { passwordHash: '' }; // fallback
    delete authStore[oldUserKey];
    data.username = newUsername;
    data.displayName = newName;
    data.role = newRole;
    authStore[newUsername.toLowerCase()] = data;
    localStorage.setItem('bcie_auth_store', JSON.stringify(authStore));
  }

  AUDIT_LOG.unshift({ ts: new Date().toISOString(), level:'info', event:'Usuario editado', user: sessionStorage.getItem('bcie_auth') ? JSON.parse(sessionStorage.getItem('bcie_auth')).user?.username||'admin' : 'admin', details:`${newUsername} → ${newRole} (${newStatus})` });
  renderUsers(); renderAudit(); renderOverview(); closeModal();
  document.getElementById('kpiUsers').textContent = USERS.filter(x=>x.status==='active').length;
  showToast(t('toast.saved'), 'success');
}

function deleteUser(id) {
  if (!confirm(t('modal.deleteconfirm'))) return;
  const idx = USERS.findIndex(x => x.id === id);
  if (idx > -1) {
    const deleted = USERS.splice(idx, 1)[0];
    saveUsersData();
    
    let authStore = JSON.parse(localStorage.getItem('bcie_auth_store')) || {};
    delete authStore[deleted.username.toLowerCase()];
    localStorage.setItem('bcie_auth_store', JSON.stringify(authStore));

    AUDIT_LOG.unshift({ ts: new Date().toISOString(), level:'warn', event:'Usuario eliminado', user:'admin', details: deleted.username });
    renderUsers(); renderAudit(); renderOverview(); closeModal();
    document.getElementById('kpiUsers').textContent = USERS.filter(x=>x.status==='active').length;
    showToast(t('toast.deleted'), 'warn');
  }
}

function resetPassword(id) {
  const u = USERS.find(x => x.id === id);
  if (!u) return;
  const body = document.getElementById('modalBody');
  const title = document.getElementById('modalTitle');
  title.textContent = t('modal.resetpw') + ': @' + u.username;
  body.innerHTML = `
    <div style="margin-bottom:1rem;padding:.6rem;background:rgba(245,158,11,.08);border:1px solid rgba(245,158,11,.2);border-radius:var(--radius-sm);font-size:.78rem;color:#f59e0b;display:flex;gap:.5rem;align-items:center">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
      <span>${t('pw.requirements')}</span>
    </div>
    <div class="form-field">
      <label>${t('modal.newpw')}</label>
      <input type="password" id="resetNewPw" placeholder="••••••••" oninput="updatePwStrength()">
      <div id="pwStrengthBar" style="margin-top:6px;height:4px;border-radius:2px;background:var(--border);overflow:hidden"><div id="pwStrengthFill" style="height:100%;width:0;border-radius:2px;transition:all .3s"></div></div>
      <div id="pwStrengthLabel" style="font-size:.68rem;margin-top:3px;color:var(--text-dim)"></div>
    </div>
    <div class="form-field">
      <label>${t('modal.confirmpw')}</label>
      <input type="password" id="resetConfirmPw" placeholder="••••••••">
      <div id="pwMatchMsg" style="font-size:.68rem;margin-top:3px"></div>
    </div>
    <div style="display:flex;gap:6px;justify-content:flex-end;margin-top:.8rem">
      <button class="btn-secondary" onclick="closeModal()">${t('modal.cancel')}</button>
      <button class="btn-primary" onclick="executeResetPassword(${u.id})">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
        ${t('modal.resetbtn')}
      </button>
    </div>`;
  document.getElementById('modalOverlay').classList.add('visible');
}

function updatePwStrength() {
  const pw = document.getElementById('resetNewPw').value;
  const fill = document.getElementById('pwStrengthFill');
  const label = document.getElementById('pwStrengthLabel');
  let score = 0;
  if (pw.length >= 6) score++;
  if (pw.length >= 10) score++;
  if (/[A-Z]/.test(pw)) score++;
  if (/[0-9]/.test(pw)) score++;
  if (/[^A-Za-z0-9]/.test(pw)) score++;
  const levels = [
    { w:'0%', c:'#64748b', l:'' },
    { w:'20%', c:'#ef4444', l:t('pw.weak') },
    { w:'40%', c:'#f59e0b', l:t('pw.fair') },
    { w:'65%', c:'#f59e0b', l:t('pw.fair') },
    { w:'85%', c:'#22c55e', l:t('pw.good') },
    { w:'100%', c:'#06b6d4', l:t('pw.strong') },
  ];
  const lv = levels[score];
  fill.style.width = lv.w; fill.style.background = lv.c;
  label.textContent = lv.l; label.style.color = lv.c;
}

async function executeResetPassword(id) {
  const pw1 = document.getElementById('resetNewPw').value;
  const pw2 = document.getElementById('resetConfirmPw').value;
  if (pw1.length < 6) return showToast(t('pw.requirements'), 'warn');
  if (pw1 !== pw2) { document.getElementById('pwMatchMsg').textContent = '✗ No coinciden'; document.getElementById('pwMatchMsg').style.color = '#ef4444'; return; }
  
  const u = USERS.find(x => x.id === id);
  if (u) {
    const hash = await hashBciePassword(pw1);
    let authStore = JSON.parse(localStorage.getItem('bcie_auth_store')) || {};
    if (authStore[u.username.toLowerCase()]) {
      authStore[u.username.toLowerCase()].passwordHash = hash;
    } else {
      authStore[u.username.toLowerCase()] = { username: u.username, passwordHash: hash, role: u.role, displayName: u.displayName };
    }
    localStorage.setItem('bcie_auth_store', JSON.stringify(authStore));
  }

  AUDIT_LOG.unshift({ ts: new Date().toISOString(), level:'info', event:'Password restablecido', user:'admin', details:`Usuario: ${u?.username}` });
  renderAudit(); renderOverview(); closeModal();
  showToast(t('toast.pwreset'), 'success');
}

function toggleUser(id) {
  const u = USERS.find(x => x.id === id);
  if (u) {
    u.status = u.status === 'active' ? 'inactive' : 'active';
    saveUsersData();
    AUDIT_LOG.unshift({ ts: new Date().toISOString(), level: u.status==='active'?'success':'warn', event: u.status==='active'?'Usuario activado':'Usuario desactivado', user:'admin', details: u.username });
    renderUsers(); renderAudit(); renderOverview();
    document.getElementById('kpiUsers').textContent = USERS.filter(x => x.status === 'active').length;
    showToast(u.status==='active' ? t('users.active') : t('users.inactive'), u.status==='active'?'success':'warn');
  }
}

// ============================================
// Notificaciones emergentes (Toast)
// ============================================
function showToast(msg, type='info') {
  const colors = { success:'#22c55e', warn:'#f59e0b', error:'#ef4444', info:'#3b82f6' };
  const toast = document.createElement('div');
  toast.style.cssText = `position:fixed;bottom:1.5rem;right:1.5rem;background:var(--bg-card);border:1px solid ${colors[type]||colors.info};color:var(--text);padding:.6rem 1.2rem;border-radius:var(--radius-sm);font-size:.82rem;font-family:var(--font);z-index:2000;display:flex;align-items:center;gap:.5rem;box-shadow:0 8px 24px rgba(0,0,0,.3);animation:fadeIn 250ms ease;max-width:350px`;
  toast.innerHTML = `<span style="width:8px;height:8px;border-radius:50%;background:${colors[type]||colors.info};flex-shrink:0"></span>${msg}`;
  document.body.appendChild(toast);
  setTimeout(() => { toast.style.opacity = '0'; toast.style.transition = 'opacity .3s'; setTimeout(() => toast.remove(), 300); }, 3000);
}

// ============================================
// Renderizado completo
// ============================================
function renderAll() {
  renderOverview(); renderUsers(); renderModels();
  renderDashboards(); renderAudit(); renderNotifications();
  renderSessions(); renderHealth(); renderAlerts();
  renderRBAC(); applyRBAC();
}

// ============================================
// RBAC — Control de acceso basado en roles
// ============================================
const RBAC_PERMISSIONS = {
  'Administrador': { overview:'full', users:'full', models:'full', dashboards:'full', etl:'full', audit:'full', sessions:'full', health:'full', alerts:'full', config:'full' },
  'Analista BCIE': { overview:'full', users:'read', models:'full', dashboards:'full', etl:'read', audit:'read', sessions:'none', health:'read', alerts:'read', config:'none' },
  'Viewer':        { overview:'read', users:'none', models:'read', dashboards:'read', etl:'none', audit:'none', sessions:'none', health:'read', alerts:'none', config:'none' },
};
function renderRBAC() {
  const el = document.getElementById('rbacMatrix');
  if (!el) return;
  const roles = Object.keys(RBAC_PERMISSIONS);
  const sections = Object.keys(RBAC_PERMISSIONS['Administrador']);
  const roleBadge = r => {
    const cls = r === 'Administrador' ? 'admin' : r === 'Analista BCIE' ? 'analyst' : 'viewer';
    return `<span class="rbac-role-badge ${cls}">${r}</span>`;
  };
  const icon = level => {
    if (level === 'full') return `<span class="rbac-check yes"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" width="14" height="14"><polyline points="20 6 9 17 4 12"/></svg></span>`;
    if (level === 'read') return `<span class="rbac-check partial"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><circle cx="12" cy="12" r="1"/><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/></svg></span>`;
    return `<span class="rbac-check no"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg></span>`;
  };
  el.innerHTML = `<table class="rbac-table">
    <thead><tr><th>${t('rbac.section')}</th>${roles.map(r => `<th>${roleBadge(r)}</th>`).join('')}</tr></thead>
    <tbody>${sections.map(s => `<tr><td>${t('tab.' + s)}</td>${roles.map(r => `<td>${icon(RBAC_PERMISSIONS[r][s])}</td>`).join('')}</tr>`).join('')}</tbody>
  </table>`;
}
function getCurrentUserRole() {
  try {
    const d = sessionStorage.getItem('bcie_auth');
    if (d) { const a = JSON.parse(d); return a.user?.role || 'Administrador'; }
  } catch(e) {}
  return 'Administrador';
}
function applyRBAC() {
  const role = getCurrentUserRole();
  const perms = RBAC_PERMISSIONS[role];
  if (!perms) return;
  Object.keys(perms).forEach(section => {
    const sidebarBtn = document.querySelector(`[data-tab="${section}"]`);
    if (sidebarBtn) {
      if (perms[section] === 'none') {
        sidebarBtn.style.display = 'none';
      } else {
        sidebarBtn.style.display = '';
        if (perms[section] === 'read') sidebarBtn.style.opacity = '0.7';
        else sidebarBtn.style.opacity = '';
      }
    }
  });
}

// ============================================
// Advertencia de timeout de sesión
// ============================================
let sessionTimeoutMs = 30 * 60 * 1000; // 30 min default
let sessionWarningMs = 2 * 60 * 1000;  // warn 2 min before
let sessionTimer = null;
let sessionWarningTimer = null;
let countdownInterval = null;
let countdownSeconds = 120;

function resetSessionTimer() {
  clearTimeout(sessionTimer);
  clearTimeout(sessionWarningTimer);
  clearInterval(countdownInterval);
  document.getElementById('timeoutOverlay').classList.remove('visible');

  // Warning fires 2 min before full timeout
  sessionWarningTimer = setTimeout(() => {
    showTimeoutWarning();
  }, sessionTimeoutMs - sessionWarningMs);

  // Full timeout: auto logout
  sessionTimer = setTimeout(() => {
    handleLogout();
  }, sessionTimeoutMs);
}

function showTimeoutWarning() {
  const overlay = document.getElementById('timeoutOverlay');
  const countdown = document.getElementById('timeoutCountdown');
  const bar = document.getElementById('timeoutBarFill');
  const msg = document.getElementById('timeoutMsg');
  msg.textContent = t('timeout.msg');
  overlay.classList.add('visible');

  countdownSeconds = Math.floor(sessionWarningMs / 1000);
  const totalSeconds = countdownSeconds;
  bar.style.width = '100%';

  countdownInterval = setInterval(() => {
    countdownSeconds--;
    if (countdownSeconds <= 0) {
      clearInterval(countdownInterval);
      handleLogout();
      return;
    }
    const min = Math.floor(countdownSeconds / 60);
    const sec = countdownSeconds % 60;
    countdown.textContent = `${String(min).padStart(2,'0')}:${String(sec).padStart(2,'0')}`;
    bar.style.width = `${(countdownSeconds / totalSeconds) * 100}%`;
  }, 1000);
}

function extendSession() {
  resetSessionTimer();
  showToast(t('timeout.extend') + ' ✓', 'success');
  AUDIT_LOG.unshift({ ts: new Date().toISOString(), level:'info', event:'Sesión extendida', user:'admin', details: 'Timeout reiniciado' });
}

// Escuchar actividad del usuario para reiniciar timer
['click', 'keydown', 'mousemove', 'scroll'].forEach(evt => {
  document.addEventListener(evt, () => {
    // Solo reiniciar si la advertencia NO está visible
    if (!document.getElementById('timeoutOverlay').classList.contains('visible')) {
      clearTimeout(sessionTimer);
      clearTimeout(sessionWarningTimer);
      // Establecer nuevos temporizadores
      sessionWarningTimer = setTimeout(() => showTimeoutWarning(), sessionTimeoutMs - sessionWarningMs);
      sessionTimer = setTimeout(() => handleLogout(), sessionTimeoutMs);
    }
  }, { passive: true });
});

// ============================================
// Exportación PDF
// ============================================
function exportPDF() {
  // Generar reporte limpio en nueva ventana y disparar impresión -> Guardar como PDF
  const now = new Date();
  const dateStr = now.toLocaleDateString('es-HN', { year:'numeric', month:'long', day:'numeric' });
  const timeStr = now.toLocaleTimeString('es-HN', { hour12:false });

  const userRows = USERS.map(u =>
    `<tr><td>${u.username}</td><td>${u.displayName}</td><td>${u.role}</td><td><span style="color:${u.status==='active'?'#22c55e':'#94a3b8'}">● ${u.status}</span></td><td>${u.lastAccess}</td></tr>`
  ).join('');

  const modelRows = MODELS.map(m => {
    const metrics = Object.entries(m.metrics).map(([k,v]) => `${k}: ${v}`).join(' | ');
    return `<tr><td style="font-weight:600">${m.name}</td><td>${m.type}</td><td>${m.status}</td><td style="font-size:.75em;color:#555">${metrics}</td></tr>`;
  }).join('');

  const healthRows = HEALTH.map(h =>
    `<tr><td>${h.name}</td><td><span style="color:${h.status==='healthy'?'#22c55e':h.status==='degraded'?'#f59e0b':'#ef4444'}">● ${h.status}</span></td><td>${h.latency}</td><td>${h.uptime}</td></tr>`
  ).join('');

  const alertRows = ALERT_RULES.map(r =>
    `<tr><td>${r.name}</td><td>${r.threshold}</td><td>${r.enabled?'✅ Activa':'⚫ Inactiva'}</td><td>${r.triggered?'⚠️ Sí':'No'}</td></tr>`
  ).join('');

  const auditRows = AUDIT_LOG.slice(0,15).map(e => {
    const dt = new Date(e.ts);
    return `<tr><td style="font-family:monospace;font-size:.75em">${dt.toLocaleDateString('es-HN')} ${dt.toLocaleTimeString('es-HN',{hour12:false})}</td><td>${e.user}</td><td>${e.event}</td><td style="color:#555;font-size:.8em">${e.details||''}</td></tr>`;
  }).join('');

  const html = `<!DOCTYPE html><html><head><meta charset="UTF-8"><title>BCIE ML Lab — ${t('pdf.title')}</title>
  <style>
    *{margin:0;padding:0;box-sizing:border-box}body{font-family:'Segoe UI',Tahoma,sans-serif;font-size:11px;color:#222;padding:1cm;background:#fff}
    h1{font-size:18px;color:#0891b2;margin-bottom:2px}h2{font-size:13px;color:#333;margin:14px 0 6px;padding-bottom:3px;border-bottom:2px solid #06b6d4}
    .header{display:flex;justify-content:space-between;align-items:center;padding-bottom:10px;border-bottom:3px solid #06b6d4;margin-bottom:14px}
    .header-meta{font-size:10px;color:#666;text-align:right}
    table{width:100%;border-collapse:collapse;margin-bottom:12px;font-size:10.5px}
    th{background:#f1f5f9;color:#475569;padding:5px 8px;text-align:left;font-weight:600;font-size:10px;text-transform:uppercase;border-bottom:2px solid #ddd}
    td{padding:4px 8px;border-bottom:1px solid #e5e7eb}tr:nth-child(even){background:#f9fafb}
    .kpi-bar{display:flex;gap:12px;margin:8px 0 14px}
    .kpi{flex:1;border:1px solid #ddd;border-radius:6px;padding:10px;text-align:center}
    .kpi-val{font-size:22px;font-weight:800;color:#0891b2}.kpi-lbl{font-size:9px;color:#666;text-transform:uppercase;margin-top:2px}
    .footer{margin-top:20px;padding-top:8px;border-top:1px solid #ddd;font-size:9px;color:#888;text-align:center}
    @page{size:A4;margin:1cm}
  </style></head><body>
  <div class="header">
    <div><h1>BCIE ML Lab</h1><div style="font-size:10px;color:#666">${t('pdf.title')}</div></div>
    <div class="header-meta">Generado: ${dateStr}<br>${timeStr}<br>ISO 27001:2022</div>
  </div>
  <div class="kpi-bar">
    <div class="kpi"><div class="kpi-val">${USERS.filter(u=>u.status==='active').length}</div><div class="kpi-lbl">Usuarios Activos</div></div>
    <div class="kpi"><div class="kpi-val">${MODELS.length}</div><div class="kpi-lbl">Modelos ML</div></div>
    <div class="kpi"><div class="kpi-val">${DASHBOARDS.length}</div><div class="kpi-lbl">Dashboards</div></div>
    <div class="kpi"><div class="kpi-val">${HEALTH.filter(h=>h.status==='healthy').length}/${HEALTH.length}</div><div class="kpi-lbl">Servicios OK</div></div>
  </div>
  <h2>👥 Usuarios</h2>
  <table><thead><tr><th>Username</th><th>Nombre</th><th>Rol</th><th>Estado</th><th>Último Acceso</th></tr></thead><tbody>${userRows}</tbody></table>
  <h2>🧠 Modelos ML</h2>
  <table><thead><tr><th>Modelo</th><th>Tipo</th><th>Estado</th><th>Métricas</th></tr></thead><tbody>${modelRows}</tbody></table>
  <h2>🟢 Health Check</h2>
  <table><thead><tr><th>Servicio</th><th>Estado</th><th>Latencia</th><th>Uptime</th></tr></thead><tbody>${healthRows}</tbody></table>
  <h2>🔔 Reglas de Alerta</h2>
  <table><thead><tr><th>Regla</th><th>Umbral</th><th>Estado</th><th>Disparada</th></tr></thead><tbody>${alertRows}</tbody></table>
  <h2>📋 Audit Log (Recientes)</h2>
  <table><thead><tr><th>Timestamp</th><th>Usuario</th><th>Evento</th><th>Detalles</th></tr></thead><tbody>${auditRows}</tbody></table>
  <div class="footer">BCIE ML Lab · Panel de Administración · ${dateStr} · Documento generado automáticamente · Confidencial</div>
  </body></html>`;

  const w = window.open('', '_blank', 'width=800,height=1000');
  w.document.write(html);
  w.document.close();
  setTimeout(() => w.print(), 400);
}

// ============================================
// Botón flotante de acción rápida (FAB)
// ============================================
function toggleFab() {
  document.getElementById('fabContainer').classList.toggle('open');
}
function updateFabLabels() {
  document.querySelectorAll('.fab-action').forEach(a => {
    const label = a.getAttribute(`data-label-${currentLang}`);
    if (label) {
      a.style.setProperty('--fab-label', `"${label}"`);
      // Update the CSS content via data attribute
      a.setAttribute('data-label', label);
    }
  });
}
// Cerrar FAB al hacer clic fuera
document.addEventListener('click', e => {
  const fab = document.getElementById('fabContainer');
  if (fab && fab.classList.contains('open') && !fab.contains(e.target)) {
    fab.classList.remove('open');
  }
});
// Vincular toggle al botón principal
document.addEventListener('DOMContentLoaded', () => {
  const fabMain = document.getElementById('fabMain');
  if (fabMain) fabMain.addEventListener('click', toggleFab);
});

// ============================================
// Inicialización con carga esquelética
// ============================================
document.addEventListener('DOMContentLoaded', () => {
  showSkeleton();
  setTimeout(() => {
    hideSkeleton();
    applyI18n();
    renderCharts();
    renderComparison();
    renderRBAC();
    applyRBAC();
    resetSessionTimer();
    updateFabLabels();
  }, 600);
});
