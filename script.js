let db = JSON.parse(localStorage.getItem('fcpro_db')) || {
  users: [],
  groups: [],
  tasks: [],
  submissions: []
};

function saveData() {
  localStorage.setItem('fcpro_db', JSON.stringify(db));
}

let currentUser = null;
let selectedGroupId = null;
let selectedTaskId = null;

function togglePassword(inputId) {
  const inp = document.getElementById(inputId);
  inp.type = inp.type === "password" ? "text" : "password";
}

function login() {
  const l = document.getElementById("login-input").value.trim();
  const p = document.getElementById("pass-input").value.trim();

  if (l === "ega1234" && p === "parol1234") {
    currentUser = { role: "owner", name: "Ega", surname: "Admin" };
  } else {
    const u = db.users.find(u => u.login === l && u.pass === p);
    if (u) {
      currentUser = { role: "user", ...u };
    } else {
      alert("Login yoki parol noto'g'ri!"); 
      return;
    }
  }

  document.getElementById("login-screen").style.display = "none";
  document.getElementById("dashboard").style.display = "flex";
  
  document.getElementById("welcome-user").innerText = `Salom, ${currentUser.surname} ${currentUser.name}! 👋`;
  document.getElementById("user-role").innerText = currentUser.role === "owner" ? "Tizim Egasi" : "O'quvchi Kabineti";

  if (currentUser.role === "owner") {
    document.getElementById("btn-add-task-owner").classList.remove("hidden");
    document.getElementById("btn-add-group-owner").classList.remove("hidden");
    document.getElementById("menu-check").classList.remove("hidden");
  }

  renderAll();
}

function logout() { location.reload(); }

function switchTab(tab) {
  document.querySelectorAll(".menu-item").forEach(i => i.classList.remove("active"));
  document.getElementById("section-tasks").classList.add("hidden");
  document.getElementById("section-groups").classList.add("hidden");
  document.getElementById("section-check").classList.add("hidden");

  if (tab === 'tasks') {
    document.getElementById("menu-tasks").classList.add("active");
    document.getElementById("section-tasks").classList.remove("hidden");
  } else if (tab === 'groups') {
    document.getElementById("menu-groups").classList.add("active");
    document.getElementById("section-groups").classList.remove("hidden");
  } else if (tab === 'check') {
    document.getElementById("menu-check").classList.add("active");
    document.getElementById("section-check").classList.remove("hidden");
  }
}

/* GURUHLAR */
function createGroup() {
  const name = document.getElementById("group-name-inp").value.trim();
  if (!name) return;
  db.groups.push({ id: Date.now(), name, members: [] });
  saveData(); closeModals(); renderGroups();
  document.getElementById("group-name-inp").value = "";
}

function openAddUserModal(groupId) {
  selectedGroupId = groupId;
  openModal('modal-add-user');
}

function addUserToGroup() {
  const fn = document.getElementById("u-fname").value.trim();
  const ln = document.getElementById("u-lname").value.trim();
  const code = document.getElementById("u-code").value.trim();

  if (!fn || !ln || code.length !== 4 || isNaN(code)) {
    alert("Ism, familiya va 4 ta raqam shaklida kiriting!"); return;
  }

  const generatedLogin = "odam" + code;
  const generatedPass = "parol" + code;

  const newUser = { id: Date.now(), name: fn, surname: ln, login: generatedLogin, pass: generatedPass };
  db.users.push(newUser);

  const g = db.groups.find(g => g.id === selectedGroupId);
  if (g) g.members.push(newUser);

  saveData();
  alert(`Odam saqlandi!\nLogin: ${generatedLogin}\nParol: ${generatedPass}`);
  closeModals(); renderGroups();

  document.getElementById("u-fname").value = "";
  document.getElementById("u-lname").value = "";
  document.getElementById("u-code").value = "";
}

function renderGroups() {
  const container = document.getElementById("groups-container");
  container.innerHTML = "";

  if (db.groups.length === 0) {
    container.innerHTML = "<p style='color:#94a3b8;'>Hozircha guruhlar yo'q.</p>";
    return;
  }


  db.groups.forEach(g => {
    let html = `<div style="background:#0f172a; padding:15px; border-radius:8px; margin-bottom:15px;">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <h4>Guruh: ${g.name}</h4>
        ${currentUser.role === 'owner' ? `<button class="action-btn-sm btn-green" onclick="openAddUserModal(${g.id})">+ Odam qo'shish</button>` : ''}
      </div>
      <table>
        <thead><tr><th>#</th><th>F.I.SH</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th></tr></thead>
        <tbody>`;
    
    if (g.members.length === 0) {
      html += `<tr><td colspan="7" style="color:#94a3b8;">Hali odamlar qo'shilmagan</td></tr>`;
    } else {
      g.members.forEach((m, idx) => {
        html += `<tr>
          <td>${idx+1}</td>
          <td style="text-align:left;">${m.name} ${m.surname}</td>
          <td>✓</td><td>✕</td><td>✓</td><td>-</td><td>-</td>
        </tr>`;
      });
    }
    html += `</tbody></table></div>`;
    container.innerHTML += html;
  });
}

/* TOPSHIRIQLAR */
function createTask() {
  const title = document.getElementById("t-title").value.trim();
  if (!title) return;
  db.tasks.push({ id: Date.now(), title });
  saveData(); closeModals(); renderTasks();
  document.getElementById("t-title").value = "";
}

function openSubmitModal(taskId) {
  selectedTaskId = taskId;
  openModal('modal-submit-task');
}

function submitTaskLink() {
  const link = document.getElementById("yt-link").value.trim();
  
  if (!link.includes("youtube.com") && !link.includes("youtu.be")) {
    alert("Xatolik yuz berdi: Iltimos, faqat YouTube video havolasini (link) kiriting!");
    return;
  }

  let subIndex = db.submissions.findIndex(s => s.taskId === selectedTaskId && s.userId === currentUser.id);

  if (subIndex !== -1) {
    db.submissions[subIndex].link = link;
    db.submissions[subIndex].status = "kutilmoqda";
    db.submissions[subIndex].score = null;
  } else {
    db.submissions.push({
      id: Date.now(),
      taskId: selectedTaskId,
      userId: currentUser.id,
      userName: `${currentUser.surname} ${currentUser.name}`,
      link: link,
      status: "kutilmoqda",
      score: null
    });
  }

  saveData();
  alert("Topshiriq yuborildi!");
  closeModals(); renderTasks();
  document.getElementById("yt-link").value = "";
}

function renderTasks() {
  const tbody = document.getElementById("task-list-body");
  tbody.innerHTML = "";

  let total = db.tasks.length;
  let done = 0, pending = 0, left = 0;

  db.tasks.forEach((t, i) => {
    let sub = db.submissions.find(s => s.taskId === t.id && s.userId === (currentUser ? currentUser.id : null));
    let statusHtml = "<span style='color:#ef4444;'>Topshirilmagan</span>";
    let actionBtn = currentUser.role === 'owner' 
      ? "<span style='color:#94a3b8;'>Tekshiruvchi</span>" 
      : `<button class="action-btn-sm btn-blue" onclick="openSubmitModal(${t.id})">Topshirish</button>`;

    if (sub) {
      if (sub.status === "kutilmoqda") {
        statusHtml = "<span style='color:#eab308;'>Kutilmoqda</span>";
        if (currentUser.role !== 'owner') actionBtn = "<span style='color:#94a3b8;'>Tekshirilmoqda</span>";
        pending++;
      } else if (sub.status === "bajarilgan") {
        if (sub.score === 20) statusHtml = "<span class='badge badge-green'>✓ 20 ball</span>";
        else if (sub.score === 10) statusHtml = "<span class='badge badge-blue'>✓ 10 ball</span>";
        else statusHtml = "<span class='badge badge-red'>✕ 0 ball</span>";
        
        if (currentUser.role !== 'owner') actionBtn = "✅ Qabul qilindi";
        done++;
      } else if (sub.status === "qayta") {
        statusHtml = "<span class='badge badge-orange'>Qayta topshirish</span>";
        if (currentUser.role !== 'owner') {
          actionBtn = `<button class="action-btn-sm btn-retry" onclick="openSubmitModal(${t.id})">Qayta</button>`;
        }
        left++;
      }
    } else {
      left++;
    }


    tbody.innerHTML += `<tr>
      <td>#${i+1}</td>
      <td style="text-align:left;">${t.title}</td>
      <td>${statusHtml}</td>
      <td>${actionBtn}</td>
    </tr>`;
  });

  document.getElementById("st-total").innerText = total;
  document.getElementById("st-done").innerText = done;
  document.getElementById("st-pending").innerText = pending;
  document.getElementById("st-left").innerText = left;
}

/* TEKSHIRISH BO'LIMI (EGA UCHUN) */
function renderCheckList() {
  const tbody = document.getElementById("check-list-body");
  tbody.innerHTML = "";

  const pendingSubmissions = db.submissions.filter(s => s.status === "kutilmoqda");

  if (pendingSubmissions.length === 0) {
    tbody.innerHTML = `<tr><td colspan="4" style="color:#94a3b8;">Tekshirilishi kerak bo'lgan topshiriqlar yo'q.</td></tr>`;
    return;
  }

  pendingSubmissions.forEach(s => {
    const t = db.tasks.find(task => task.id === s.taskId);
    tbody.innerHTML += `<tr>
      <td>${s.userName}</td>
      <td>${t ? t.title : 'Topshiriq'}</td>
      <td>
        <a href="${s.link}" target="_blank" class="action-btn-sm btn-blue" style="text-decoration:none;">▶️ Topshiriqni tomosha qilish</a>
      </td>
      <td>
        <button class="action-btn-sm btn-green" onclick="evaluateSub(${s.id}, 20)">20 Ball (Yashil)</button>
        <button class="action-btn-sm btn-blue" onclick="evaluateSub(${s.id}, 10)">10 Ball (Ko'k)</button>
        <button class="action-btn-sm btn-red" onclick="evaluateSub(${s.id}, 0)">0 Ball (Qizil)</button>
        <button class="action-btn-sm btn-retry" onclick="rejectSub(${s.id})">Qayta</button>
      </td>
    </tr>`;
  });
}

// BAHOLASH FUNKSIYASI (20, 10, 0 ball)
function evaluateSub(subId, score) {
  const sub = db.submissions.find(s => s.id === subId);
  if (sub) {
    sub.status = "bajarilgan";
    sub.score = score;
    saveData();
    renderAll();
  }
}

// QAYTA TOPSHIRISHGA YUBORISH
function rejectSub(subId) {
  const sub = db.submissions.find(s => s.id === subId);
  if (sub) {
    sub.status = "qayta";
    sub.score = null;
    saveData();
    renderAll();
  }
}

function renderAll() {
  renderTasks();
  renderGroups();
  renderCheckList();
}

function openModal(id) { document.getElementById(id).classList.remove("hidden"); }
function closeModals() { document.querySelectorAll(".modal").forEach(m => m.classList.add("hidden")); }
