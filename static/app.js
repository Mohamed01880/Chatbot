/**
 * PORTAIL D'INTÉGRATION — USINE FAISCEAUX DE CÂBLES AUTOMOBILE
 * Logique Frontend & Interaction (Phase 3)
 */

(function () {
  'use strict';

  // --- ÉTAT GLOBAL DE L'APPLICATION ---
  const state = {
    user: null, // { name, matricule, role, lang }
    currentView: 'login',
    history: [],
    theme: localStorage.getItem('auto_harness_theme') || 'dark',
    lang: localStorage.getItem('auto_harness_lang') || 'fr',
    showSources: false,
    backendStatus: { provider: 'gemini', llm: false, model: '' },
    isRecording: false,
    speechRecognition: null,
    modules: []
  };

  // -------------------------------------------------------------------
  // Internationalisation (i18n) – Dictionnaire Arabe Intégral (0 mot en français)
  // -------------------------------------------------------------------
  const I18N_AR = {
    // Navigation & En-tête
    "Câblage Auto": "أحزمة الأسلاك للسيارات",
    "Portail d'Intégration": "بوابة الإدماج والتكوين المهني",
    "Accueil": "الرئيسية",
    "Assistant IA": "المدرب الذكي",
    "Changer de thème": "تغيير المظهر",
    "Déconnexion": "تسجيل الخروج",
    "Session active": "جلسة نشطة",
    "Bonjour,": "مرحبًا،",
    "Bonjour ,": "مرحبًا ،",
    "Collègue": "زميلنا",
    "Affectation : Usine Faisceaux de Câbles Automobiles.": "التعيين : مصنع أحزمة الأسلاك الكهربائية للسيارات.",
    "Ouvrir l'Assistant Formateur IA": "فتح المدرب الذكي الافتراضي",
    "Consulter les Fiches Métier": "الاطلاع على بطاقات التكوين",

    // Suivi du Parcours (Tracker)
    "Votre Parcours d'Intégration": "مسار إدماجك وتكوينك المهني",
    "65% complété": "65% مكتمل",
    "35% complété": "35% مكتمل",
    "50% complété": "50% مكتمل",
    "Phase 1": "المرحلة 1",
    "Accueil RH & Histoire": "استقبال الموارد البشرية والتعريف بالمصنع",
    "Phase 2": "المرحلة 2",
    "Sécurité & 5S": "السلامة العامة ومنهجية 5S",
    "Phase 3 (En cours)": "المرحلة 3 (قيد الإنجاز)",
    "Phase 3": "المرحلة 3",
    "Formation Production": "التدريب على محطات الإنتاج",
    "Phase 4": "المرحلة 4",
    "Évaluation & Validation": "التقييم والتأهيل النهائي",

    // Boîte de Recherche Rapide
    "Posez une question au formateur (ex: Comment faire un sertissage ? Quels EPI ?)…": "اطرح سؤالاً على المدرب (مثال: كيف يتم السرتيساج؟ ما هي معدات الوقاية؟)...",
    "Demander au Formateur": "اسأل المدرب",

    // Titres de Sections & Modules
    "Zones de l'Usine & Fiches de Formation": "مناطق المصنع وبطاقات التدريب المهني",
    "Explorez les postes de travail et posez des questions ciblées au formateur.": "اكتشف محطات العمل واطرح أسئلة موجهة ومباشرة على المدرب الذكي.",
    "Priorité 1": "أولوية 1",
    "Sécurité Générale & EPI": "السلامة العامة ومعدات الوقاية (EPI)",
    "Équipements de protection obligatoire, arrêt d'urgence coup-de-poing, gestes de secours en cas d'accident ou de coupure.": "معدات الحماية الفردية الإلزامية، زر التوقف الاستعجالي، وإسعافات الطوارئ عند حدوث أي إصابة أو جرح.",
    "9 fiches disponibles": "9 بطاقات تدريبية متاحة",
    "Interroger le formateur ➔": "استشر المدرب ➔",
    "Interroger le formateur →": "استشر المدرب ➔",
    "Interroger le formateur": "استشر المدرب",

    "Poste P1": "محطة P1",
    "Zone Coupe & Dénudage": "منطقة القطع وتعرية الأسلاك",
    "Machines automatiques Komax, déroulage des bobines, coupe à longueur exacte, dénudage des extrémités et règles de sécurité.": "آلات كوماكس الأوتوماتيكية، سحب اللفائف، القطع بدقة متناهية، تعرية الأطراف وقواعد السلامة المتبعة.",
    "Machines Komax": "آلات كوماكس",

    "Poste P2": "محطة P2",
    "Zone Préparation & Sertissage": "منطقة التحضير والضغط (السرتيساج)",
    "Sertissage mécanique des cosses, gaines thermorétractables au pistolet chauffant, soudure par ultrasons et test d'arrachement.": "الضغط الميكانيكي للموصلات، العوازل الحرارية بالمسدس الحراري، اللحام بالموجات فوق الصوتية واختبار قوة الشد.",
    "Sertissage & Cosses": "الضغط والموصلات",

    "Poste P3": "محطة P3",
    "Zone Assemblage & Câblage": "منطقة التجميع وتركيب الأسلاك",
    "Planches de pose rotatives avec gabarits colorés, encliquetage des connecteurs, pose du ruban adhésif et clips de fixation.": "طاولات التركيب الدوارة بالألوان والمقاييس، تثبيت المقابس والموصلات، لف الشريط اللاصق ومثبتات الكابلات.",
    "Planches rotatives": "طاولات التركيب الدوارة",

    "Contrôle": "مراقبة الجودة",
    "Contrôle Qualité & Test Électrique": "مراقبة الجودة والفحص الكهربائي",
    "Test de continuité sur tables électroniques, détection des inversions de fils et contrôle visuel de l'étanchéité.": "اختبار التوصيل الكهربائي على الطاولات الإلكترونية، كشف الأخطاء وعكس الأسلاك والفحص البصري للعزل المائي.",
    "Continuité & Sécurité": "التوصيل والسلامة",

    "Méthode": "المنهجية",
    "Glossaire Technique & 5S": "المصطلحات التقنية ومنهجية 5S",
    "Lexique complet bilingue français / arabe / darija (sertissage, toron, cosse) et les 5 piliers du rangement de l'atelier.": "دليل شامل ومبسط للمصطلحات التقنية والمبادئ الخمسة لتنظيم ورشة العمل ونظافتها.",
    "Lexique Bilingue": "دليل المصطلحات",

    // Section FAQ (Questions Fréquentes)
    "Questions fréquentes des nouveaux employés": "الأسئلة الشائعة للملتحقين الجدد",
    "Cliquez pour obtenir immédiatement l'explication du formateur.": "انقر للحصول على إجابة فورية وشرح مبسط من المدرب.",
    "Quels sont les EPI obligatoires ?": "ما هي معدات الوقاية الفردية الإلزامية؟",
    "Différence entre les postes P1, P2 et P3 ?": "ما الفرق بين المحطات P1 و P2 و P3؟",
    "Comment réussir un bon sertissage ?": "كيف أحقق ضغطاً وسرتيساجاً ناجحاً؟",
    "Que faire en cas de blessure ou accident ?": "ماذا أفعل فوراً عند وقوع حادث أو جرح؟",
    "C'est quoi la méthode 5S ?": "ما هي خطوات منهجية 5S لتنظيم الورشة؟",
    "Quelles sont les 4 phases de ma formation ?": "ما هي المراحل الأربع لتدريبي وإدماجي؟",
    "Quels sont les EPI obligatoires dès que j'entre dans l'usine ?": "ما هي معدات الوقاية الإلزامية بمجرد دخولي المصنع؟",
    "C'est quoi la différence entre le poste P1, P2 et P3 ?": "ما الفرق بين محطة P1 ومحطة P2 ومحطة P3؟",
    "Comment savoir si un sertissage est bien réalisé ?": "كيف أتأكد أن عملية الضغط (السرتيساج) تمت بنجاح؟",
    "Que dois-je faire immédiatement en cas de blessure ou accident ?": "ماذا أفعل فوراً عند حدوث إصابة أو حادث في الورشة؟",
    "Explique-moi les étapes de la méthode 5S en usine.": "اشرح لي مراحل تطبيق منهجية 5S في المصنع.",
    "Quelles sont les 4 phases de mon parcours d'intégration ?": "ما هي المراحل الأربع لمسار إدماجي وتكويني؟",

    // Connexion & Inscription
    "Portail Intégration Usine": "بوابة إدماج المصنع",
    "Connexion Opérateur": "تسجيل دخول المشغّل",
    "Inscription Collaborateur": "تسجيل موظف أو عميل جديد",
    "Connexion": "تسجيل الدخول",
    "Inscription": "إنشاء حساب",
    "Matricule Employé": "رقم الموظف",
    "Matricule Employé / Identifiant": "رقم الموظف / المعرّف الخاص",
    "Mot de passe": "كلمة المرور",
    "Accéder au Portail": "الدخول إلى البوابة",
    "Nouveau collaborateur ou client ?": "هل أنت موظف أو عميل جديد؟",
    "Créer un compte": "إنشاء حساب جديد",
    "Connexion rapide démo (PostgreSQL) :": "دخول سريع تجريبي (قاعدة البيانات) :",
    "Nom et Prénom": "الاسم واللقب",
    "Email": "البريد الإلكتروني",
    "Poste d'affectation": "محطة العمل المخصصة",
    "Langue": "اللغة",
    "Créer mon compte dans PostgreSQL": "تسجيل حسابي في قاعدة البيانات",
    "Vous avez déjà un compte ?": "هل لديك حساب بالفعل؟",
    "Se connecter": "تسجيل الدخول",
    "Zone Coupe (Poste P1)": "منطقة القطع (محطة P1)",
    "Zone Préparation & Sertissage (Poste P2)": "منطقة التحضير والضغط (محطة P2)",
    "Zone Assemblage & Planches (Poste P3)": "منطقة التجميع واللوحات (محطة P3)",
    "Contrôle Qualité & Test Électrique": "مراقبة الجودة والفحص الكهربائي",
    "Nouvel Arrivant (Tronc Commun)": "ملتحق جديد (التدريب المشترك)",
    "Français": "الفرنسية",
    "Arabe / Darija (الدارجة)": "العربية / الدارجة",
    "Arabe / Darija": "العربية / الدارجة",

    // Vue Chat
    "Assistant Formateur Virtuel": "المدرب الافتراضي الذكي",
    "Formateur Virtuel d'Usine": "المدرب الافتراضي للمصنع",
    "Usine Faisceaux Automobile": "مصنع أحزمة أسلاك السيارات",
    "Effacer l'historique": "مسح المحادثة",
    "Afficher les sources techniques": "إظهار المصادر التقنية",
    "Afficher sources": "إظهار المصادر",
    "Posez votre question au formateur… (ex: c'est quoi le sertissage ?)": "اطرح سؤالك على المدرب... (مثال: ما هو السرتيساج وكيف يتم؟)",
    "Posez votre question au formateur...": "اطرح سؤالك على المدرب...",
    "Retour à l'accueil": "العودة إلى الرئيسية",
    "Poser une question à la voix": "اطرح سؤالاً بالصوت",
    "Envoyer": "إرسال",
    "Écouter": "استماع",
    "Arrêter": "إيقاف",
    "Copier": "نسخ",
    "🔊 Écouter": "🔊 استماع",
    "📋 Copier": "📋 نسخ"
  };

  function isArabicActive() {
    const userLang = state.user?.lang ? state.user.lang.toLowerCase() : '';
    const appLang = state.lang ? state.lang.toLowerCase() : '';
    return appLang.includes('ar') || userLang.includes('ar');
  }

  function translateRole(role) {
    if (!role) return '';
    if (!isArabicActive()) return role;
    if (role.includes('P1') || role.toLowerCase().includes('coupe')) return 'منطقة القطع وتعرية الأسلاك (محطة P1)';
    if (role.includes('P2') || role.toLowerCase().includes('sertissage')) return 'منطقة التحضير والضغط (محطة P2)';
    if (role.includes('P3') || role.toLowerCase().includes('assemblage')) return 'منطقة التجميع واللوحات (محطة P3)';
    if (role.toLowerCase().includes('qualité') || role.toLowerCase().includes('test')) return 'مراقبة الجودة والفحص الكهربائي';
    if (role.toLowerCase().includes('tronc') || role.toLowerCase().includes('nouvel')) return 'ملتحق جديد (التدريب المشترك)';
    return role;
  }

  function applyTranslations() {
    const isAr = isArabicActive();

    // 1. Activer la direction RTL et la langue HTML
    document.documentElement.lang = isAr ? 'ar' : 'fr';
    document.documentElement.dir = isAr ? 'rtl' : 'ltr';
    if (isAr) {
      document.body.classList.add('rtl-mode');
    } else {
      document.body.classList.remove('rtl-mode');
    }

    // 2. Parcourir tous les nœuds de texte
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null);
    let node;
    while ((node = walker.nextNode())) {
      if (node.parentElement && (node.parentElement.tagName === 'SCRIPT' || node.parentElement.tagName === 'STYLE')) {
        continue;
      }

      // Stocker le texte original en français au premier passage
      if (node._origFr === undefined) {
        node._origFr = node.nodeValue;
      }

      if (isAr) {
        const trimmed = node._origFr.trim();
        if (I18N_AR[trimmed]) {
          node.nodeValue = node._origFr.replace(trimmed, I18N_AR[trimmed]);
        }
      } else {
        node.nodeValue = node._origFr;
      }
    }

    // 3. Mettre à jour les placeholders et titres
    document.querySelectorAll('input, textarea, button, a').forEach(el => {
      if (el.placeholder) {
        if (el._origPlaceholder === undefined) el._origPlaceholder = el.placeholder;
        if (isAr) {
          const trimmedP = el._origPlaceholder.trim();
          if (I18N_AR[trimmedP]) el.placeholder = I18N_AR[trimmedP];
        } else {
          el.placeholder = el._origPlaceholder;
        }
      }

      if (el.title) {
        if (el._origTitle === undefined) el._origTitle = el.title;
        if (isAr) {
          const trimmedT = el._origTitle.trim();
          if (I18N_AR[trimmedT]) el.title = I18N_AR[trimmedT];
        } else {
          el.title = el._origTitle;
        }
      }
    });

    // 4. Mettre à jour l'affichage utilisateur et les suggestions
    updateUserUI();
  }

  // Profils démo rapides
  const DEMO_PROFILES = {
    amine: { name: 'Amine El Mansouri', matricule: 'OP-2026-104', role: 'P1 - Coupe & Dénudage', lang: 'ar' },
    fatima: { name: 'Fatima Zahra Bennani', matricule: 'OP-2026-218', role: 'P2 - Préparation & Sertissage', lang: 'ar' },
    youssef: { name: 'Youssef Alami', matricule: 'OP-2026-309', role: 'P3 - Assemblage & Câblage', lang: 'ar' },
    sara: { name: 'Sara Chaoui', matricule: 'OP-2026-015', role: 'Nouvel Arrivant (Tronc Commun)', lang: 'ar' }
  };

  // Suggestions par rôle (Français)
  const ROLE_SUGGESTIONS = {
    'P1 - Coupe & Dénudage': [
      'Quels sont les EPI obligatoires en zone coupe ?',
      'Comment fonctionne la machine de coupe Komax ?',
      'Quelles sont les règles de sécurité avec les lames ?',
      'Comment vérifier la longueur d’un fil coupé ?'
    ],
    'P2 - Préparation & Sertissage': [
      'C’est quoi un sertissage réussi ?',
      'Comment réaliser un test d’arrachement ?',
      'À quoi sert la gaine thermorétractable ?',
      'Quelles sont les anomalies fréquentes de sertissage ?'
    ],
    'P3 - Assemblage & Câblage': [
      'Comment lire une planche de pose rotative ?',
      'C’est quoi l’encliquetage d’un connecteur ?',
      'Comment bien poser le ruban adhésif sur un toron ?',
      'Que faire si un fil est mal repéré sur la table ?'
    ],
    'default': [
      'Quelles sont les 4 phases de mon intégration ?',
      'Quels sont les EPI obligatoires dès l’entrée ?',
      'Que faire en cas d’accident ou de coupure ?',
      'Explique-moi les 5S simplement.'
    ]
  };

  // Suggestions par rôle (Arabe intégral)
  const ROLE_SUGGESTIONS_AR = {
    'P1 - Coupe & Dénudage': [
      'ما هي معدات الوقاية الإلزامية في منطقة القطع؟',
      'كيف تعمل آلة القطع الأوتوماتيكية كوماكس؟',
      'ما هي قواعد السلامة عند التعامل مع الشفرات؟',
      'كيف أتحقق من الطول الدقيق للسلك المقطوع؟'
    ],
    'P2 - Préparation & Sertissage': [
      'ما هي شروط الضغط والسرتيساج الناجح؟',
      'كيف أقوم باختبار قوة الشد والتماسك؟',
      'ما فائدة العازل الحراري بالمسدس الحراري؟',
      'ما هي العيوب الشائعة في عملية الضغط؟'
    ],
    'P3 - Assemblage & Câblage': [
      'كيف أقرأ لوحة التجميع الدوارة بدقة؟',
      'ما المقصود بتثبيت وإقفال الموصلات؟',
      'كيف أضع الشريط اللاصق بإتقان على الحزمة؟',
      'ماذا أفعل إذا كان السلك غير واضح الترقيم؟'
    ],
    'default': [
      'ما هي المراحل الأربع لمسار إدماجي في المصنع؟',
      'ما هي معدات الوقاية الإلزامية منذ الدخول؟',
      'ماذا أفعل فوراً في حالة وقوع حادث أو جرح؟',
      'اشرح لي خطوات منهجية 5S ببساطة.'
    ]
  };

  // --- INITIALISATION ---
  window.addEventListener('DOMContentLoaded', () => {
    initTheme();
    loadSavedUser();
    initSpeechRecognition();
    fetchBackendHealth();
    fetchDatabaseStatus();
    fetchModules();
    setupEventListeners();
    handleHashRouting();
    // Apply translations on initial load
    applyTranslations();
  });

  // --- GESTION DU THÈME ---
  function initTheme() {
    if (state.theme === 'light') {
      document.body.classList.add('light-theme');
    } else {
      document.body.classList.remove('light-theme');
    }
    updateThemeIcon();
  }

  function toggleTheme() {
    state.theme = state.theme === 'dark' ? 'light' : 'dark';
    localStorage.setItem('auto_harness_theme', state.theme);
    initTheme();
    showToast(`Thème ${state.theme === 'dark' ? 'Sombre' : 'Clair'} activé`);
  }

  function updateThemeIcon() {
    const icon = document.getElementById('theme-icon');
    if (icon) {
      icon.textContent = state.theme === 'dark' ? '☀️' : '🌙';
    }
  }

  // --- SESSION UTILISATEUR & BADGE ---
  function loadSavedUser() {
    const saved = localStorage.getItem('auto_harness_user');
    if (saved) {
      try {
        state.user = JSON.parse(saved);
        if (state.user && state.user.lang) {
          state.lang = state.user.lang;
        }
        applyTranslations();
        updateUserUI();
        if (!window.location.hash || window.location.hash === '#login') {
          navigateTo('home');
        }
      } catch (e) {
        state.user = null;
      }
    }
    if (!state.user) {
      applyTranslations();
      navigateTo('login');
    }
  }

  function saveUser(userObj) {
    state.user = userObj;
    if (userObj && userObj.lang) {
      state.lang = userObj.lang;
      localStorage.setItem('auto_harness_lang', userObj.lang);
    }
    localStorage.setItem('auto_harness_user', JSON.stringify(userObj));
    applyTranslations();
    updateUserUI();
  }

  function logout() {
    state.user = null;
    localStorage.removeItem('auto_harness_user');
    // Toujours remettre la langue en français à la déconnexion
    state.lang = 'fr';
    localStorage.setItem('auto_harness_lang', 'fr');
    state.history = [];
    resetChatUI();
    applyTranslations();
    updateUserUI();
    navigateTo('login');
    showToast('Vous avez été déconnecté.');
  }

  function updateUserUI() {
    const userPill = document.getElementById('user-pill');
    const navLinks = document.getElementById('nav-links');
    const heroName = document.getElementById('hero-user-name');
    const heroRole = document.getElementById('hero-user-role');

    if (state.user) {
      if (userPill) userPill.style.display = 'flex';
      if (navLinks) navLinks.style.display = 'flex';

      const initials = getInitials(state.user.name);
      const pillAvatar = document.getElementById('user-pill-avatar');
      const pillName = document.getElementById('user-pill-name');
      const pillRole = document.getElementById('user-pill-role');

      if (pillAvatar) pillAvatar.textContent = initials;
      if (pillName) pillName.textContent = state.user.name;
      if (pillRole) pillRole.textContent = isArabicActive() ? translateRole(state.user.role) : state.user.role;

      const heroTitle = document.querySelector('.hero-title');
      if (heroTitle) {
        if (isArabicActive()) {
          heroTitle.innerHTML = `مرحبًا، <span class="highlight" id="hero-user-name">${escapeHtml(state.user.name)}</span> !`;
        } else {
          heroTitle.innerHTML = `Bonjour, <span class="highlight" id="hero-user-name">${escapeHtml(state.user.name)}</span> !`;
        }
      }

      if (heroRole) {
        if (isArabicActive()) {
          heroRole.textContent = `المنطقة : ${translateRole(state.user.role)} | رقم الموظف : ${state.user.matricule}`;
        } else {
          heroRole.textContent = `Zone : ${state.user.role} | Matricule : ${state.user.matricule}`;
        }
      }

      updateTrackerProgress();
      renderChatSuggestions();
    } else {
      if (userPill) userPill.style.display = 'none';
      if (navLinks) navLinks.style.display = 'none';
    }
  }

  function getInitials(name) {
    if (!name) return 'OP';
    const parts = name.trim().split(/\s+/);
    if (parts.length >= 2) {
      return (parts[0][0] + parts[1][0]).toUpperCase();
    }
    return name.slice(0, 2).toUpperCase();
  }

  // --- ROUTAGE INTERNE PAR HASH ---
  function navigateTo(viewId) {
    window.location.hash = '#' + viewId;
  }

  function handleHashRouting() {
    const hash = (window.location.hash || '#').slice(1);
    const validViews = ['login', 'home', 'chat'];
    let target = validViews.includes(hash) ? hash : (state.user ? 'home' : 'login');

    if (!state.user && target !== 'login') {
      target = 'login';
    }

    state.currentView = target;
    // Re‑apply translations whenever the view changes
    applyTranslations();

    // Masquer toutes les vues
    document.querySelectorAll('.app-view').forEach(v => {
      v.classList.remove('active');
    });

    // Activer la vue courante
    const viewEl = document.getElementById(`view-${target}`);
    if (viewEl) {
      viewEl.classList.add('active');
    }

    // Activer le lien dans la navbar
    document.querySelectorAll('.nav-item').forEach(btn => {
      btn.classList.toggle('active', btn.getAttribute('data-view') === target);
    });

    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  window.addEventListener('hashchange', handleHashRouting);

  // --- SANTÉ DU BACKEND & MODULES ---
  async function fetchBackendHealth() {
    try {
      const res = await fetch('/health');
      if (res.ok) {
        const data = await res.json();
        state.backendStatus = data;
        const statusEl = document.getElementById('chat-status-text');
        const providerTag = document.getElementById('provider-tag');
        if (statusEl) {
          statusEl.textContent = `En ligne (${data.provider} : ${data.model || 'actif'})`;
        }
        if (providerTag) {
          providerTag.textContent = `${data.provider.toUpperCase()} IA`;
        }
      }
    } catch (e) {
      const statusEl = document.getElementById('chat-status-text');
      if (statusEl) statusEl.textContent = 'Serveur local (hors ligne ou chargement)';
    }
  }

  async function fetchModules() {
    try {
      const res = await fetch('/api/modules');
      if (res.ok) {
        const data = await res.json();
        state.modules = data.modules || [];
        renderDynamicModules();
      }
    } catch (e) {
      console.log('Modules statiques conservés.');
    }
  }

  // --- STATUT BASE DE DONNÉES POSTGRESQL ---
  async function fetchDatabaseStatus() {
    const pill = document.getElementById('db-status-pill');
    const textEl = document.getElementById('db-status-text');
    if (!pill || !textEl) return;
    try {
      const res = await fetch('/api/auth/status');
      if (res.ok) {
        const data = await res.json();
        if (data.connected) {
          pill.classList.remove('disconnected');
          textEl.textContent = 'PostgreSQL actif';
          pill.title = `Connecté à PostgreSQL (${data.database} @ ${data.host}:${data.port})`;
        } else {
          pill.classList.add('disconnected');
          textEl.textContent = 'PostgreSQL à configurer';
          pill.title = data.message || 'Non connecté';
        }
      }
    } catch (e) {
      pill.classList.add('disconnected');
      textEl.textContent = 'PostgreSQL hors ligne';
    }
  }

  // --- MISE À JOUR DU BADGE INTERACTIF SUR LOGIN & SIGNUP ---
  function updateBadgePreview() {
    const isSignup = document.getElementById('signup-form')?.classList.contains('active');

    let name = '';
    let matricule = '';
    let role = '';

    if (isSignup) {
      name = document.getElementById('signup-name')?.value.trim();
      matricule = document.getElementById('signup-matricule')?.value.trim();
      role = document.getElementById('signup-role')?.value;
    } else {
      matricule = document.getElementById('login-matricule')?.value.trim();
      // Si c'est un profil démo connu
      for (const k in DEMO_PROFILES) {
        if (DEMO_PROFILES[k].matricule.toLowerCase() === matricule?.toLowerCase()) {
          name = DEMO_PROFILES[k].name;
          role = DEMO_PROFILES[k].role;
          break;
        }
      }
    }

    const badgeName = document.getElementById('badge-name-preview');
    const badgeRole = document.getElementById('badge-role-preview');
    const badgeId = document.getElementById('badge-id-preview');
    const badgeAvatar = document.getElementById('badge-avatar-preview');

    const finalName = name || state.user?.name || 'Nouvel Opérateur';
    const finalMatricule = matricule || state.user?.matricule || 'OP-2026-000';
    const finalRole = role || state.user?.role || 'P1 - Coupe & Dénudage';

    if (badgeName) badgeName.textContent = finalName;
    if (badgeRole) badgeRole.textContent = finalRole;
    if (badgeId) badgeId.textContent = `ID: ${finalMatricule}`;
    if (badgeAvatar) badgeAvatar.textContent = getInitials(finalName);
  }

  // --- CHANGEMENT D'ONGLET AUTH (CONNEXION / INSCRIPTION) ---
  function switchAuthTab(targetTab) {
    const tabLogin = document.getElementById('tab-login');
    const tabSignup = document.getElementById('tab-signup');
    const formLogin = document.getElementById('login-form');
    const formSignup = document.getElementById('signup-form');
    const title = document.getElementById('auth-title');
    const desc = document.getElementById('auth-desc');

    if (targetTab === 'signup') {
      tabLogin?.classList.remove('active');
      tabSignup?.classList.add('active');
      formLogin?.classList.remove('active');
      formSignup?.classList.add('active');
      if (title) title.textContent = "Inscription Collaborateur";
      if (desc) desc.textContent = "Créez votre compte opérateur dans la base PostgreSQL.";
    } else {
      tabSignup?.classList.remove('active');
      tabLogin?.classList.add('active');
      formSignup?.classList.remove('active');
      formLogin?.classList.add('active');
      if (title) title.textContent = "Connexion Opérateur";
      if (desc) desc.textContent = "Authentifiez-vous avec votre matricule ou vos identifiants PostgreSQL.";
    }
    updateBadgePreview();
  }

  // --- PROGRESSION DE FORMATION ---
  function updateTrackerProgress() {
    const role = state.user?.role || '';
    const barFill = document.getElementById('tracker-bar-fill');
    const percentBadge = document.getElementById('tracker-percent');

    let percent = 50;
    if (role.includes('P1') || role.includes('P2') || role.includes('P3')) {
      percent = 65; // Phase 3 en cours
    } else {
      percent = 35; // Tronc commun
    }

    if (barFill) barFill.style.width = percent + '%';
    if (percentBadge) percentBadge.textContent = isArabicActive() ? `${percent}% مكتمل` : `${percent}% complété`;
  }

  // --- ÉVÉNEMENTS & FORMULAIRES ---
  function setupEventListeners() {
    // Navigation Brand
    const brand = document.getElementById('nav-brand');
    if (brand) {
      brand.addEventListener('click', (e) => {
        e.preventDefault();
        navigateTo(state.user ? 'home' : 'login');
      });
    }

    // Nav Items
    document.querySelectorAll('.nav-item').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        const view = btn.getAttribute('data-view');
        if (view) navigateTo(view);
      });
    });

    // Theme Toggle
    const themeBtn = document.getElementById('btn-toggle-theme');
    if (themeBtn) themeBtn.addEventListener('click', toggleTheme);

    // Logout
    const logoutBtn = document.getElementById('btn-logout');
    if (logoutBtn) logoutBtn.addEventListener('click', logout);

    // Onglets Auth
    document.getElementById('tab-login')?.addEventListener('click', () => switchAuthTab('login'));
    document.getElementById('tab-signup')?.addEventListener('click', () => switchAuthTab('signup'));
    document.getElementById('btn-goto-signup')?.addEventListener('click', () => switchAuthTab('signup'));
    document.getElementById('btn-goto-login')?.addEventListener('click', () => switchAuthTab('login'));

    // Toggle Afficher/Masquer Mot de passe
    document.querySelectorAll('.btn-toggle-pwd').forEach(btn => {
      btn.addEventListener('click', () => {
        const targetId = btn.getAttribute('data-target');
        const input = document.getElementById(targetId);
        if (input) {
          const isPwd = input.type === 'password';
          input.type = isPwd ? 'text' : 'password';
          btn.textContent = isPwd ? '🙈' : '👁️';
        }
      });
    });

    // Formulaire Connexion (PostgreSQL)
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
      loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const matricule = document.getElementById('login-matricule')?.value.trim();
        const password = document.getElementById('login-password')?.value;
        const submitBtn = document.getElementById('btn-submit-login');

        if (!matricule || !password) {
          showToast('Veuillez saisir votre matricule et mot de passe', 'warning');
          return;
        }

        if (submitBtn) {
          submitBtn.disabled = true;
          submitBtn.innerHTML = '<span>Connexion à PostgreSQL...</span>';
        }

        try {
          const res = await fetch('/api/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ matricule, password })
          });
          const data = await res.json();

          if (!res.ok) {
            showToast(data.detail || 'Identifiants invalides', 'warning');
            return;
          }

          saveUser(data.user);
          if (data.user.lang) {
            state.lang = data.user.lang;
            localStorage.setItem('auto_harness_lang', state.lang);
            applyTranslations();
          }
          showToast(`Bienvenue ${data.user.name} !`);
          navigateTo('home');
        } catch (err) {
          showToast('Erreur serveur de connexion : ' + err.message, 'warning');
        } finally {
          if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<span>Accéder au Portail</span> <span>➔</span>';
          }
        }
      });
    }

    // Formulaire Inscription (PostgreSQL)
    const signupForm = document.getElementById('signup-form');
    if (signupForm) {
      signupForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const name = document.getElementById('signup-name')?.value.trim();
        const matricule = document.getElementById('signup-matricule')?.value.trim();
        const email = document.getElementById('signup-email')?.value.trim();
        const password = document.getElementById('signup-password')?.value;
        const role = document.getElementById('signup-role')?.value;
        const lang = document.getElementById('signup-lang')?.value;
        const submitBtn = document.getElementById('btn-submit-signup');

        if (!name || !matricule || !password) {
          showToast('Veuillez remplir le nom, matricule et mot de passe', 'warning');
          return;
        }

        if (password.length < 4) {
          showToast('Le mot de passe doit comporter au moins 4 caractères', 'warning');
          return;
        }

        if (submitBtn) {
          submitBtn.disabled = true;
          submitBtn.innerHTML = '<span>Enregistrement dans PostgreSQL...</span>';
        }

        try {
          const res = await fetch('/api/auth/signup', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, matricule, email: email || null, password, role, lang })
          });
          const data = await res.json();

          if (!res.ok) {
            showToast(data.detail || 'Erreur lors de l’inscription', 'warning');
            return;
          }

          saveUser(data.user);
          state.lang = data.user.lang || lang;
          localStorage.setItem('auto_harness_lang', state.lang);
          applyTranslations();
          showToast(`Compte enregistré avec succès dans PostgreSQL ! Bienvenue ${data.user.name}`);
          navigateTo('home');
        } catch (err) {
          showToast("Erreur PostgreSQL : " + err.message, 'warning');
        } finally {
          if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<span>Créer mon compte dans PostgreSQL</span> <span>➔</span>';
          }
        }
      });
    }

    // Synchronisation en direct du badge
    ['login-matricule', 'signup-name', 'signup-matricule', 'signup-role'].forEach(id => {
      const el = document.getElementById(id);
      if (el) {
        el.addEventListener('input', updateBadgePreview);
        el.addEventListener('change', updateBadgePreview);
      }
    });

    // Boutons de démo rapide
    document.querySelectorAll('.btn-quick-profile').forEach(btn => {
      btn.addEventListener('click', () => {
        const key = btn.getAttribute('data-profile');
        const p = DEMO_PROFILES[key];
        if (p) {
          switchAuthTab('login');
          const matInput = document.getElementById('login-matricule');
          const pwdInput = document.getElementById('login-password');
          if (matInput) matInput.value = p.matricule;
          if (pwdInput) pwdInput.value = 'pass123';
          updateBadgePreview();
          showToast(`Profil ${p.name} pré-rempli (mot de passe: pass123)`);
        }
      });
    });

    // Recherche Rapide sur la page d'accueil
    const homeSearchForm = document.getElementById('home-search-form');
    if (homeSearchForm) {
      homeSearchForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const input = document.getElementById('home-search-input');
        const q = input.value.trim();
        if (q) {
          navigateTo('chat');
          sendChatMessage(q);
          input.value = '';
        }
      });
    }

    // Raccourcis FAQ
    document.querySelectorAll('.faq-chip').forEach(chip => {
      chip.addEventListener('click', () => {
        const question = chip.getAttribute('data-question') || chip.textContent.trim();
        navigateTo('chat');
        sendChatMessage(question);
      });
    });

    // Formulaire Chat
    const chatForm = document.getElementById('chat-form');
    if (chatForm) {
      chatForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const input = document.getElementById('chat-input');
        const q = input.value.trim();
        if (q) {
          sendChatMessage(q);
          input.value = '';
        }
      });
    }

    // Clear Chat
    const clearBtn = document.getElementById('btn-clear-chat');
    if (clearBtn) {
      clearBtn.addEventListener('click', () => {
        if (confirm('Voulez-vous effacer l’historique de conversation ?')) {
          state.history = [];
          resetChatUI();
          showToast('Historique effacé.');
        }
      });
    }

    // Toggle Sources
    const sourcesToggle = document.getElementById('toggle-sources');
    if (sourcesToggle) {
      sourcesToggle.addEventListener('change', (e) => {
        state.showSources = e.target.checked;
        showToast(state.showSources ? 'Affichage des sources activé' : 'Sources masquées');
      });
    }

    // Microphone Vocal (STT)
    const micBtn = document.getElementById('btn-mic');
    if (micBtn) {
      micBtn.addEventListener('click', toggleSpeechRecognition);
    }
  }

  // --- RECONNAISSANCE VOCALE (STT) ---
  function initSpeechRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      const r = new SpeechRecognition();
      r.continuous = false;
      r.interimResults = false;
      r.lang = state.lang === 'ar' ? 'ar-MA' : 'fr-FR';

      r.onstart = () => {
        state.isRecording = true;
        const micBtn = document.getElementById('btn-mic');
        if (micBtn) micBtn.classList.add('recording');
        showToast('Parlez maintenant, le formateur écoute...', 'info');
      };

      r.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        const input = document.getElementById('chat-input');
        if (input) {
          input.value = transcript;
          sendChatMessage(transcript);
        }
      };

      r.onerror = (e) => {
        console.error('Erreur reconnaissance vocale:', e);
        showToast('Impossible de capter votre voix. Essayez au clavier.', 'warning');
      };

      r.onend = () => {
        state.isRecording = false;
        const micBtn = document.getElementById('btn-mic');
        if (micBtn) micBtn.classList.remove('recording');
      };

      state.speechRecognition = r;
    } else {
      const micBtn = document.getElementById('btn-mic');
      if (micBtn) {
        micBtn.title = 'Reconnaissance vocale non supportée sur ce navigateur';
      }
    }
  }

  function toggleSpeechRecognition() {
    if (!state.speechRecognition) {
      showToast('Votre navigateur ne supporte pas la reconnaissance vocale.', 'warning');
      return;
    }
    if (state.isRecording) {
      state.speechRecognition.stop();
    } else {
      // Use selected UI language for STT
      state.speechRecognition.lang = state.lang === 'ar' ? 'ar-MA' : 'fr-FR';
      state.speechRecognition.start();
    }
  }

  // --- SYNTHÈSE VOCALE (TTS) ---
  let availableVoices = [];

  function loadAvailableVoices() {
    if ('speechSynthesis' in window) {
      availableVoices = window.speechSynthesis.getVoices();
    }
  }

  if ('speechSynthesis' in window) {
    loadAvailableVoices();
    window.speechSynthesis.onvoiceschanged = loadAvailableVoices;
  }

  let activeSpeakBtn = null;

  function stopSpeaking() {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
    }
    if (activeSpeakBtn) {
      activeSpeakBtn.innerHTML = '🔊 Écouter';
      activeSpeakBtn.classList.remove('playing');
      activeSpeakBtn = null;
    }
  }

  function speakText(text, btnElement = null) {
    if (!('speechSynthesis' in window)) {
      showToast('Synthèse vocale non supportée par votre navigateur', 'warning');
      return;
    }

    // Toggle arrêt si on reclique sur le bouton actif
    if (btnElement && btnElement === activeSpeakBtn && (window.speechSynthesis.speaking || window.speechSynthesis.pending)) {
      stopSpeaking();
      showToast('Lecture arrêtée.');
      return;
    }

    stopSpeaking();

    // Nettoyer le markdown et le texte technique
    let clean = text
      .replace(/\[\[INCONNU\]\]/gi, '')
      .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
      .replace(/[*#_`>~]/g, ' ')
      .replace(/\s+/g, ' ')
      .trim();

    if (!clean) return;

    const isArabic = hasArabic(clean);
    const targetPrefix = isArabic ? 'ar' : 'fr';

    if (!availableVoices || availableVoices.length === 0) {
      availableVoices = window.speechSynthesis.getVoices();
    }

    // Sélection de la voix appropriée
    let voice = availableVoices.find(v => v.lang && v.lang.toLowerCase().startsWith(targetPrefix));
    if (!voice) {
      voice = availableVoices.find(v => v.lang && v.lang.toLowerCase().includes(targetPrefix));
    }

    // Découpage en segments courts (< 160 caractères) pour éviter le blocage silencieux de Chrome/Edge
    const segments = [];
    const rawSentences = clean.split(/(?<=[.!?:;\n])\s+/);
    for (const s of rawSentences) {
      const trimmed = s.trim();
      if (!trimmed) continue;
      if (trimmed.length <= 160) {
        segments.push(trimmed);
      } else {
        const subParts = trimmed.split(/(?<=[,])\s+/);
        for (const p of subParts) {
          const pt = p.trim();
          if (pt) segments.push(pt);
        }
      }
    }

    if (segments.length === 0) segments.push(clean);

    activeSpeakBtn = btnElement;
    if (btnElement) {
      btnElement.innerHTML = '⏹️ Arrêter';
      btnElement.classList.add('playing');
    }

    showToast('Lecture audio en cours...');

    // Débloquer le moteur de synthèse Chrome si en pause
    if (window.speechSynthesis.paused) {
      window.speechSynthesis.resume();
    }

    let currentIndex = 0;

    function speakNext() {
      if (currentIndex >= segments.length) {
        stopSpeaking();
        return;
      }

      const segmentText = segments[currentIndex];
      currentIndex++;

      const utterance = new SpeechSynthesisUtterance(segmentText);
      if (voice) {
        utterance.voice = voice;
      }
      utterance.lang = voice ? voice.lang : (isArabic ? 'ar-SA' : 'fr-FR');
      utterance.rate = 1.0;
      utterance.pitch = 1.0;
      utterance.volume = 1.0;

      utterance.onend = () => {
        speakNext();
      };

      utterance.onerror = (evt) => {
        console.warn('[Synthèse vocale]:', evt);
        if (evt.error !== 'interrupted' && evt.error !== 'canceled') {
          showToast(`Erreur audio (${evt.error}). Vérifiez le volume de votre système.`, 'warning');
        }
        stopSpeaking();
      };

      window.speechSynthesis.speak(utterance);
    }

    // Délai nécessaire après .cancel() pour les navigateurs Chromium
    setTimeout(() => {
      speakNext();
    }, 60);
  }

  function hasArabic(text) {
    return /[\u0600-\u06FF]/.test(text);
  }

  // --- LOGIQUE DE CHATBOT (RAG) ---
  async function sendChatMessage(question) {
    if (!question || !question.trim()) return;

    // 1. Ajouter le message de l'utilisateur
    appendMessage(question, 'user');

    // 2. Désactiver le bouton d'envoi et afficher l'indicateur de frappe
    const sendBtn = document.getElementById('btn-send');
    const input = document.getElementById('chat-input');
    if (sendBtn) sendBtn.disabled = true;
    if (input) input.disabled = true;

    const typingIndicator = showTypingIndicator();

    try {
      const res = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question: question,
          history: state.history,
          show_sources: state.showSources,
          user_matricule: state.user?.matricule || null
        })
      });

      if (!res.ok) throw new Error(`Erreur HTTP: ${res.status}`);

      const data = await res.json();
      removeTypingIndicator(typingIndicator);

      // Ajouter la réponse assistant
      appendMessage(data.answer, 'assistant', data.sources);

      // Mettre à jour l'historique de conversation
      state.history.push(
        { role: 'user', content: question },
        { role: 'assistant', content: data.answer }
      );

    } catch (err) {
      removeTypingIndicator(typingIndicator);
      appendMessage(`⚠️ Désolé, une erreur de communication est survenue (${err.message}). Veuillez réessayer.`, 'assistant');
    } finally {
      if (sendBtn) sendBtn.disabled = false;
      if (input) {
        input.disabled = false;
        input.focus();
      }
    }
  }

  function appendMessage(text, role, sources = []) {
    const container = document.getElementById('chat-messages');
    if (!container) return;

    const row = document.createElement('div');
    row.className = `msg-row ${role}`;

    const avatar = document.createElement('div');
    avatar.className = 'msg-avatar';
    if (role === 'user') {
      avatar.textContent = getInitials(state.user?.name || 'MOI');
    } else {
      avatar.textContent = '🤖';
    }

    const bubbleWrap = document.createElement('div');
    bubbleWrap.className = 'msg-bubble-wrap';

    const bubble = document.createElement('div');
    bubble.className = 'msg-bubble';
    bubble.innerHTML = formatMarkdown(text);
    bubbleWrap.appendChild(bubble);

    // Si assistant : boutons Copier et Écouter
    if (role === 'assistant') {
      const actions = document.createElement('div');
      actions.className = 'msg-actions';

      const btnSpeak = document.createElement('button');
      btnSpeak.className = 'btn-msg-action';
      btnSpeak.innerHTML = '🔊 Écouter';
      btnSpeak.addEventListener('click', () => speakText(text, btnSpeak));
      actions.appendChild(btnSpeak);

      const btnCopy = document.createElement('button');
      btnCopy.className = 'btn-msg-action';
      btnCopy.innerHTML = '📋 Copier';
      btnCopy.addEventListener('click', () => {
        navigator.clipboard.writeText(text);
        showToast('Réponse copiée !');
      });
      actions.appendChild(btnCopy);

      bubbleWrap.appendChild(actions);

      // Affichage des sources
      if (sources && sources.length > 0) {
        const sourcesDiv = document.createElement('div');
        sourcesDiv.className = 'msg-sources';
        sourcesDiv.innerHTML = '<strong>📚 Sources :</strong> ' + sources.map(s => `<span class="source-badge">${escapeHtml(s.fiche)} > ${escapeHtml(s.section)}</span>`).join(' ');
        bubbleWrap.appendChild(sourcesDiv);
      }
    }

    row.appendChild(avatar);
    row.appendChild(bubbleWrap);

    container.appendChild(row);
    container.scrollTop = container.scrollHeight;
  }

  function showTypingIndicator() {
    const container = document.getElementById('chat-messages');
    if (!container) return null;

    const row = document.createElement('div');
    row.className = 'msg-row assistant';
    row.id = 'active-typing-indicator';

    const avatar = document.createElement('div');
    avatar.className = 'msg-avatar';
    avatar.textContent = '🤖';

    const typing = document.createElement('div');
    typing.className = 'typing-indicator';
    typing.innerHTML = '<span class="typing-dot"></span><span class="typing-dot"></span><span class="typing-dot"></span>';

    row.appendChild(avatar);
    row.appendChild(typing);
    container.appendChild(row);
    container.scrollTop = container.scrollHeight;
    return row;
  }

  function removeTypingIndicator(el) {
    if (el && el.parentNode) {
      el.parentNode.removeChild(el);
    }
  }

  function resetChatUI() {
    const container = document.getElementById('chat-messages');
    if (container) {
      const userName = escapeHtml(state.user?.name || 'Collègue');
      let welcomeHtml;
      if (isArabicActive()) {
        welcomeHtml = `
          <div class="msg-row assistant">
            <div class="msg-avatar">🤖</div>
            <div class="msg-bubble-wrap">
              <div class="msg-bubble">
                مرحبًا <strong>${userName}</strong> ! 👋<br>
                أنا <strong>المدرب الافتراضي</strong> الخاص بمصنع أحزمة الأسلاك الكهربائية للسيارات.<br>
                اطرح عليّ أسئلتك حول محطة عملك، قواعد السلامة، السرتيساج، التجميع أو منهجية 5S.
              </div>
            </div>
          </div>
        `;
      } else {
        welcomeHtml = `
          <div class="msg-row assistant">
            <div class="msg-avatar">🤖</div>
            <div class="msg-bubble-wrap">
              <div class="msg-bubble">
                Bonjour <strong>${userName}</strong> ! 👋<br>
                Je suis votre <strong>Formateur Virtuel</strong> pour l'usine de faisceaux de câbles automobiles.<br>
                Posez-moi vos questions sur votre poste de travail, les consignes de sécurité, le sertissage, l'assemblage ou les 5S.
              </div>
            </div>
          </div>
        `;
      }
      container.innerHTML = welcomeHtml;
    }
    renderChatSuggestions();
  }

  function renderChatSuggestions() {
    const container = document.getElementById('chat-suggestions');
    if (!container) return;

    const userRole = state.user?.role || 'default';
    const suggestionsDict = isArabicActive() ? ROLE_SUGGESTIONS_AR : ROLE_SUGGESTIONS;
    const suggestions = suggestionsDict[userRole] || suggestionsDict['default'];

    container.innerHTML = '';
    suggestions.forEach(text => {
      const pill = document.createElement('button');
      pill.className = 'suggestion-pill';
      pill.textContent = text;
      pill.addEventListener('click', () => {
        sendChatMessage(text);
      });
      container.appendChild(pill);
    });
  }

  // --- MODULES DE L'ACCUEIL ---
  function renderDynamicModules() {
    // Rend les cartes de modules cliquables pour ouvrir le chat directement
    document.querySelectorAll('.module-card').forEach(card => {
      card.addEventListener('click', () => {
        const query = card.getAttribute('data-query');
        if (query) {
          navigateTo('chat');
          sendChatMessage(query);
        }
      });
    });
  }

  // --- UTILITAIRES DE RENDU ---
  function formatMarkdown(text) {
    let esc = escapeHtml(text);

    // Gras
    esc = esc.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    // Italique
    esc = esc.replace(/\*([^*]+)\*/g, '<em>$1</em>');

    // Listes à puces
    esc = esc.replace(/^[\*\-] (.+)$/gm, '<li>$1</li>');
    esc = esc.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');

    // Étapes numérotées (1., 2., 3.)
    esc = esc.replace(/^(\d+)\. (.+)$/gm, '<div class="step-line"><strong style="color:var(--cyan)">$1.</strong> $2</div>');

    // Retours à la ligne
    esc = esc.replace(/\n\n/g, '<br><br>');

    return esc;
  }

  function escapeHtml(str) {
    if (!str) return '';
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  function showToast(message, type = 'success') {
    let container = document.getElementById('toast-container');
    if (!container) {
      container = document.createElement('div');
      container.id = 'toast-container';
      container.className = 'toast-container';
      document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    const icon = type === 'warning' ? '⚠️' : (type === 'info' ? 'ℹ️' : '✅');
    toast.innerHTML = `<span>${icon}</span> <span>${escapeHtml(message)}</span>`;

    container.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(10px)';
      toast.style.transition = 'all 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, 3200);
  }

})();
