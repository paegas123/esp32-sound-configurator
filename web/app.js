const TIER_COLORS = {
  red: ["var(--tier-red-bg)", "var(--tier-red-text)"],
  yellow: ["var(--tier-yellow-bg)", "var(--tier-yellow-text)"],
  green: ["var(--tier-green-bg)", "var(--tier-green-text)"],
};
const NEUTRAL_CATEGORY_COLOR = ["var(--surface-neutral, #F1EDE3)", "var(--text-main)"];

let uploadJobId = null;
let uploadPollTimer = null;
let monitorJobId = null;
let monitorPollTimer = null;
let currentFilter = "green";
let currentTab = "vehicle";
let debugMode = false;
let allTabs = [];
let currentLanguage = "cs";

const HEADER_TEXTS = {
  cs: { subtitle: "Nastavení zvukového modulu bez ručního úpravování kódu", credit: "Postaveno nad projektem" },
  en: { subtitle: "Configure your sound module without editing any code by hand", credit: "Built on top of the project" },
  de: { subtitle: "Konfiguriere dein Soundmodul, ohne Code von Hand zu bearbeiten", credit: "Aufgebaut auf dem Projekt" },
};

function applyHeaderLanguage(lang) {
  const texts = HEADER_TEXTS[lang] || HEADER_TEXTS.cs;
  const subtitleEl = document.getElementById("app-subtitle");
  const creditEl = document.getElementById("app-credit-label");
  if (subtitleEl) subtitleEl.textContent = texts.subtitle;
  if (creditEl) creditEl.textContent = texts.credit;
}

async function apiGet(path) {
  const res = await fetch(path);
  return res.json();
}
async function apiPost(path, body) {
  const res = await fetch(path, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body || {}),
  });
  return res.json();
}

async function init() {
  const boot = await apiGet("/api/bootstrap");

  document.querySelectorAll("#language-overlay button[data-lang]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      await apiPost("/api/language", { lang: btn.dataset.lang });
      currentLanguage = btn.dataset.lang;
      applyHeaderLanguage(currentLanguage);
      document.getElementById("language-overlay").classList.add("hidden");
      afterLanguageReady();
    });
  });
  const closeBtn = document.getElementById("language-overlay-close");
  if (closeBtn) {
    closeBtn.addEventListener("click", () => {
      document.getElementById("language-overlay").classList.add("hidden");
    });
  }

  if (!boot.language) {
    document.getElementById("language-overlay").classList.remove("hidden");
  } else {
    currentLanguage = boot.language;
    applyHeaderLanguage(currentLanguage);
    afterLanguageReady();
  }
}

async function afterLanguageReady() {
  await checkForUpdate();
  await loadVehicleList();
  await setupTierFilter();
  await setupTabs();
  setupToolbarEvents();
  setupBottomBar();
  setupMonitorOverlay();
  setupDebugMode();
}

function setupDebugMode() {
  const toggleBtn = document.getElementById("debug-toggle");
  const bar = document.getElementById("debug-bar");

  toggleBtn.addEventListener("click", () => {
    debugMode = !debugMode;
    document.body.classList.toggle("debug-mode", debugMode);
    bar.classList.toggle("hidden", !debugMode);
  });

  document.getElementById("debug-export").addEventListener("click", () => {
    window.location.href = "/api/debug/export";
  });

  document.getElementById("debug-reset").addEventListener("click", async () => {
    if (!confirm("Opravdu vymazat všechny ruční úpravy barev z ladicího režimu?")) return;
    await apiPost("/api/debug/clear");
    await refreshCurrentView();
  });
}

let saveFlashTimer = null;
function flashSaved() {
  const el = document.getElementById("save-flash");
  if (!el) return;
  el.textContent = "✓ Uloženo";
  el.classList.add("visible");
  clearTimeout(saveFlashTimer);
  saveFlashTimer = setTimeout(() => el.classList.remove("visible"), 1200);
}

function makeTierDots(tierKey, onAfterChange) {
  const wrap = document.createElement("span");
  wrap.className = "tier-dots";
  ["green", "yellow", "red"].forEach((tier) => {
    const dot = document.createElement("button");
    dot.type = "button";
    dot.className = `tier-dot dot-${tier}`;
    dot.title = tier;
    dot.addEventListener("click", async (e) => {
      e.stopPropagation();
      await apiPost("/api/debug/set-tier", { name: tierKey, tier });
      flashSaved();
      onAfterChange(tier);
    });
    wrap.appendChild(dot);
  });
  return wrap;
}

function makeNoteInput(scope, key, currentNote) {
  const input = document.createElement("input");
  input.type = "text";
  input.className = "debug-note-input";
  input.placeholder = "Poznámka pro Claude (proč/na co změnit)...";
  input.value = currentNote || "";
  input.addEventListener("click", (e) => e.stopPropagation());
  input.addEventListener("change", async () => {
    await apiPost("/api/debug/set-note", { scope, key, note: input.value });
    flashSaved();
  });
  return input;
}

async function setupTabs() {
  const { tabs } = await apiGet("/api/tabs");
  allTabs = tabs;
  renderTabButtons();
  applyTabFilter(currentFilter);
}

function renderTabButtons() {
  const container = document.getElementById("tabs");
  container.innerHTML = "";

  allTabs.forEach((tab) => {
    const wrap = document.createElement("span");
    wrap.className = "tab-button-wrap";
    wrap.dataset.tier = tab.tier;

    const btn = document.createElement("button");
    btn.className = `tab-button tab-tier-${tab.tier}` + (tab.key === currentTab ? " active" : "");
    btn.textContent = tab.label;
    btn.addEventListener("click", () => switchTab(tab.key));
    btn.dataset.key = tab.key;
    wrap.appendChild(btn);

    const dots = document.createElement("span");
    dots.className = "tier-dots";
    ["green", "yellow", "red"].forEach((tier) => {
      const dot = document.createElement("button");
      dot.type = "button";
      dot.className = `tier-dot dot-${tier}${tab.tier === tier ? " selected" : ""}`;
      dot.title = `Nastavit barvu karty na ${tier}`;
      dot.addEventListener("click", async (e) => {
        e.stopPropagation();
        await apiPost("/api/debug/set-tab-tier", { key: tab.key, tier });
        flashSaved();
        await setupTabs();
      });
      dots.appendChild(dot);
    });
    wrap.appendChild(dots);

    const tabNoteInput = makeNoteInput("tab", tab.key, tab.note);
    wrap.appendChild(tabNoteInput);

    container.appendChild(wrap);
  });
}

function updateActiveTabButton() {
  document.querySelectorAll(".tab-button").forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.key === currentTab);
  });
}

function applyTabFilter(mode) {
  const visibleTiers = LEVEL_INCLUDES[mode] || LEVEL_INCLUDES.red;
  let currentStillVisible = false;

  document.querySelectorAll(".tab-button-wrap").forEach((wrap) => {
    const visible = visibleTiers.includes(wrap.dataset.tier);
    wrap.classList.toggle("hidden", !visible);
    if (visible && wrap.querySelector(".tab-button").dataset.key === currentTab) {
      currentStillVisible = true;
    }
  });

  if (!currentStillVisible) {
    const firstVisible = [...document.querySelectorAll(".tab-button-wrap")].find(
      (w) => !w.classList.contains("hidden")
    );
    if (firstVisible) {
      switchTab(firstVisible.querySelector(".tab-button").dataset.key);
    }
  }
}

async function renderWebTab() {
  const container = document.getElementById("categories");
  container.innerHTML = "";

  const { choice } = await apiGet("/api/web-interface-choice");

  const box = document.createElement("div");
  box.className = "category";

  const header = document.createElement("div");
  header.className = "category-header";
  header.style.background = "var(--tier-yellow-bg)";
  header.style.color = "var(--tier-yellow-text)";
  header.style.cursor = "default";
  header.innerHTML = "<span>Webové rozhraní modulu</span>";
  box.appendChild(header);

  const body = document.createElement("div");
  body.className = "category-body";
  body.style.padding = "12px 14px";

  const hint = document.createElement("p");
  hint.style.fontSize = "13px";
  hint.style.color = "var(--text-muted)";
  hint.textContent =
    "Modul má svoje vlastní webové rozhraní (na adrese 192.168.4.1), přes které lze některé věci " +
    "nastavovat i za běhu, bez nutnosti nahrávat firmware znovu. Vyber, které chceš používat:";
  body.appendChild(hint);

  const options = [
    { value: "original", label: "Původní web (od autora projektu) - anglicky, jednoduchý vzhled" },
    { value: "new", label: "Nový vylepšený web (připravujeme - zatím není hotový)" },
  ];

  options.forEach((opt) => {
    const row = document.createElement("label");
    row.style.display = "flex";
    row.style.alignItems = "center";
    row.style.gap = "8px";
    row.style.padding = "8px 0";
    row.style.fontSize = "14px";

    const radio = document.createElement("input");
    radio.type = "radio";
    radio.name = "web-interface-choice";
    radio.value = opt.value;
    radio.checked = choice === opt.value;
    radio.disabled = opt.value === "new";
    radio.addEventListener("change", async () => {
      await apiPost("/api/web-interface-choice", { choice: opt.value });
    });

    row.appendChild(radio);
    row.appendChild(document.createTextNode(opt.label));
    body.appendChild(row);
  });

  box.appendChild(body);
  container.appendChild(box);
}

async function switchTab(key) {
  currentTab = key;
  updateActiveTabButton();

  const vehicleSelect = document.getElementById("vehicle-select");
  vehicleSelect.style.display = key === "vehicle" ? "" : "none";

  if (key === "vehicle") {
    await selectVehicle(vehicleSelect.value);
  } else if (key === "web") {
    renderChannelMap([]);
    await renderWebTab();
  } else {
    const data = await apiPost("/api/select-settings-file", { key });
    if (data.error) {
      document.getElementById("categories").innerHTML = `<p>${data.error}</p>`;
      return;
    }
    renderCategories(data);
  }
}

async function setupTierFilter() {
  const { mode } = await apiGet("/api/filter");
  currentFilter = mode;

  const radios = {
    red: document.getElementById("filter-red"),
    yellow: document.getElementById("filter-yellow"),
    green: document.getElementById("filter-green"),
  };
  radios[mode].checked = true;

  applyTierFilter(mode);

  Object.entries(radios).forEach(([tier, radio]) => {
    radio.addEventListener("change", async () => {
      if (!radio.checked) return;
      currentFilter = tier;
      await apiPost("/api/filter", { mode: tier });
      applyTierFilter(tier);
      applyTabFilter(tier);
    });
  });
}

// Úrovně jsou kumulativní: začátečník (green) vidí jen zelené, pokročilý
// (yellow) vidí zelené + žluté, expert (red) vidí úplně vše.
const LEVEL_INCLUDES = {
  green: ["green"],
  yellow: ["green", "yellow"],
  red: ["green", "yellow", "red"],
};

function applyTierFilter(mode) {
  const visibleTiers = LEVEL_INCLUDES[mode] || LEVEL_INCLUDES.red;
  document.querySelectorAll(".category").forEach((catDiv) => {
    const visible = visibleTiers.includes(catDiv.dataset.tier);
    catDiv.classList.toggle("category-hidden", !visible);
  });
}

async function checkForUpdate() {
  const result = await apiPost("/api/check-update");
  const banner = document.getElementById("update-banner");
  if (result.status === "no_internet_no_local") {
    banner.textContent = "Není dostupný internet a zatím nemám žádnou lokální kopii originálu. Připoj se k internetu a načti stránku znovu.";
    banner.classList.remove("hidden");
  } else if (result.status === "first_download_needed") {
    banner.textContent = "Stahuji originální projekt poprvé...";
    banner.classList.remove("hidden");
    await apiPost("/api/download-update");
    banner.classList.add("hidden");
  } else if (result.status === "update_available") {
    banner.innerHTML = "Je dostupná novější verze originálu. ";
    const btn = document.createElement("button");
    btn.textContent = "Aktualizovat";
    btn.addEventListener("click", async () => {
      banner.textContent = "Stahuji aktualizaci...";
      await apiPost("/api/download-update");
      banner.classList.add("hidden");
      await loadVehicleList();
    });
    banner.appendChild(btn);
  }
}

async function loadVehicleList() {
  const data = await apiGet("/api/vehicles");
  const select = document.getElementById("vehicle-select");
  select.innerHTML = "";
  if (data.error) {
    select.innerHTML = `<option>${data.error}</option>`;
    return;
  }
  let activeOption = null;
  let currentGroup = null;
  let currentOptgroup = null;

  data.vehicles.forEach((v) => {
    if (v.category !== currentGroup) {
      currentGroup = v.category;
      currentOptgroup = document.createElement("optgroup");
      currentOptgroup.label = v.category;
      select.appendChild(currentOptgroup);
    }
    const opt = document.createElement("option");
    opt.value = v.filename;
    opt.textContent = v.name;
    if (v.active) activeOption = opt;
    currentOptgroup.appendChild(opt);
  });

  if (activeOption) activeOption.selected = true;
  await selectVehicle(select.value);
}

async function selectVehicle(filename) {
  const data = await apiPost("/api/select-vehicle", { filename });
  if (data.error) {
    document.getElementById("categories").innerHTML = `<p>${data.error}</p>`;
    return;
  }
  renderCategories(data);
}

function setupToolbarEvents() {
  document.getElementById("vehicle-select").addEventListener("change", (e) => {
    selectVehicle(e.target.value);
  });
  document.getElementById("language-button").addEventListener("click", () => {
    document.getElementById("language-overlay").classList.remove("hidden");
  });
}

async function refreshCurrentView() {
  if (currentTab === "vehicle") {
    await selectVehicle(document.getElementById("vehicle-select").value);
  } else {
    const data = await apiPost("/api/select-settings-file", { key: currentTab });
    renderCategories(data);
  }
}

function renderInfoTable(entries, title, hint, valueKey) {
  const wrap = document.getElementById("channel-map");
  if (!entries.length) {
    wrap.classList.add("hidden");
    wrap.innerHTML = "";
    return;
  }

  wrap.classList.remove("hidden");
  wrap.innerHTML = "";

  const titleEl = document.createElement("div");
  titleEl.className = "channel-map-title";
  titleEl.textContent = title;
  wrap.appendChild(titleEl);

  const hintEl = document.createElement("div");
  hintEl.className = "channel-map-hint";
  hintEl.textContent = hint;
  wrap.appendChild(hintEl);

  const table = document.createElement("div");
  table.className = "channel-map-table";
  entries.forEach((entry) => {
    const item = document.createElement("div");
    item.className = "channel-map-item" + (entry.unused ? " unused" : "");

    const num = document.createElement("span");
    num.className = "channel-map-number";
    num.textContent = entry.unused ? "-" : entry[valueKey];
    item.appendChild(num);

    const fn = document.createElement("span");
    fn.className = "channel-map-function";
    fn.textContent = entry.unused ? `${entry.function} (nevyužito)` : entry.function;
    item.appendChild(fn);

    table.appendChild(item);
  });
  wrap.appendChild(table);
}

function renderChannelMap(entries) {
  renderInfoTable(
    entries,
    "Zapojení kanálů (vždy vidět, nezávisle na úrovni)",
    "U PWM je číslo kanálu fyzický pin CHx na desce, kam přivedeš daný výstup z přijímače. " +
      "U SBUS/IBUS/SUMD/PPM (jeden datový vodič) je to pořadové číslo kanálu nastavené ve vysílačce.",
    "channel"
  );
}

function renderLightPinMap(entries) {
  renderInfoTable(
    entries,
    "Zapojení světel (vždy vidět, nezávisle na úrovni)",
    "Kam na desce (GPIO pin) připojit každé světlo. Přesné hodnoty se liší podle zvoleného typu desky " +
      "v kartě Obecná nastavení.",
    "pin"
  );
}

function makeAutoZeroBulkOffButton(allParams) {
  const wrap = document.createElement("div");
  wrap.className = "param-row";
  wrap.style.background = "transparent";

  const label = document.createElement("span");
  label.className = "param-label";
  label.textContent = "Automatické vynulování - hromadná akce";
  wrap.appendChild(label);

  const btn = document.createElement("button");
  btn.type = "button";
  btn.className = "secondary-button";
  btn.textContent = "Vypnout pro všechny kanály";
  btn.addEventListener("click", async () => {
    const targets = allParams.filter(
      (p) => p.name && p.name.startsWith("channelAutoZero[") && p.value === "true"
    );
    for (const p of targets) {
      await apiPost("/api/param", { index: p.index, value: "false" });
    }
    markUnsaved();
    await refreshCurrentView();
  });
  wrap.appendChild(btn);

  return wrap;
}

function renderCategories(data) {
  renderChannelMap(data.channelMap || []);
  if (data.lightPinMap) {
    renderLightPinMap(data.lightPinMap);
  }

  const container = document.getElementById("categories");
  container.innerHTML = "";

  data.categories.forEach((cat) => {
    const [bg, text] = TIER_COLORS[cat.tier] || TIER_COLORS.yellow;

    const catDiv = document.createElement("div");
    catDiv.className = "category";
    catDiv.dataset.tier = cat.tier;

    const header = document.createElement("button");
    header.className = "category-header";
    header.style.background = bg;
    header.style.color = text;

    const headerLabel = document.createElement("span");
    headerLabel.textContent = cat.name;
    header.appendChild(headerLabel);

    const headerTools = document.createElement("span");
    headerTools.className = "category-header-tools";
    ["green", "yellow", "red"].forEach((tier) => {
      const dot = document.createElement("button");
      dot.type = "button";
      dot.className = `tier-dot dot-${tier}${cat.tier === tier ? " selected" : ""}`;
      dot.title = `Nastavit barvu celé složky na ${tier}`;
      dot.addEventListener("click", async (e) => {
        e.stopPropagation();
        await apiPost("/api/debug/set-category-tier", { key: cat.categoryKey, tier });
        flashSaved();
        await refreshCurrentView();
      });
      headerTools.appendChild(dot);
    });
    const catNoteInput = makeNoteInput("category", cat.categoryKey, cat.note);
    headerTools.appendChild(catNoteInput);
    header.appendChild(headerTools);

    const chevron = document.createElement("span");
    chevron.className = "chevron";
    chevron.innerHTML = cat.autoExpand ? "&#9662;" : "&#9656;";
    header.appendChild(chevron);

    const body = document.createElement("div");
    body.className = cat.autoExpand ? "category-body" : "category-body collapsed";

    header.addEventListener("click", () => {
      const collapsed = body.classList.toggle("collapsed");
      chevron.innerHTML = collapsed ? "&#9656;" : "&#9662;";
    });

    let autoZeroBulkAdded = false;
    cat.params.forEach((param) => {
      if (param.name && param.name.startsWith("channelAutoZero[") && !autoZeroBulkAdded) {
        autoZeroBulkAdded = true;
        body.appendChild(makeAutoZeroBulkOffButton(cat.params));
      }
      body.appendChild(renderParamRow(param));
    });

    catDiv.appendChild(header);
    catDiv.appendChild(body);
    container.appendChild(catDiv);
  });

  applyTierFilter(currentFilter);
}

function renderParamRow(param) {
  const row = document.createElement("div");
  row.className = `param-row tier-${param.tier || "yellow"}`;
  row.dataset.tier = param.tier || "yellow";

  const labelWrap = document.createElement("div");
  labelWrap.style.flex = "1";
  labelWrap.style.minWidth = "200px";
  const labelEl = document.createElement("span");
  labelEl.className = "param-label";
  labelEl.textContent = param.label;
  labelWrap.appendChild(labelEl);
  if (param.explanation) {
    const expl = document.createElement("span");
    expl.className = "param-explanation";
    expl.textContent = param.explanation;
    labelWrap.appendChild(expl);
  }
  row.appendChild(labelWrap);

  if (param.kind === "flag" || param.kind === "boolean_value") {
    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.checked = param.kind === "flag" ? param.active : param.value === "true";
    checkbox.addEventListener("change", async () => {
      if (param.kind === "flag") {
        await apiPost("/api/param", { index: param.index, active: checkbox.checked });
      } else {
        await apiPost("/api/param", { index: param.index, value: checkbox.checked ? "true" : "false" });
      }
      markUnsaved();
    });
    row.appendChild(checkbox);
  } else if (param.kind === "percentage_slider") {
    const slider = document.createElement("input");
    slider.type = "range";
    slider.min = "0";
    slider.max = "300";
    slider.step = "1";
    slider.value = param.value;
    const readout = document.createElement("span");
    readout.className = "param-value-readout";
    readout.textContent = param.value;
    slider.addEventListener("input", () => { readout.textContent = slider.value; });
    slider.addEventListener("change", async () => {
      await apiPost("/api/param", { index: param.index, value: slider.value });
      markUnsaved();
    });
    row.appendChild(slider);
    row.appendChild(readout);
  } else if (param.kind === "number_input") {
    const input = document.createElement("input");
    input.type = "number";
    input.value = param.value;
    input.style.width = "100px";
    input.addEventListener("change", async () => {
      await apiPost("/api/param", { index: param.index, value: input.value });
      markUnsaved();
    });
    row.appendChild(input);
  } else if (param.kind === "array" || param.kind === "string") {
    const input = document.createElement("input");
    input.type = "text";
    input.value = param.value;
    input.style.width = "260px";
    input.addEventListener("change", async () => {
      await apiPost("/api/param", { index: param.index, value: input.value });
      markUnsaved();
    });
    row.appendChild(input);
  } else if (param.kind === "flag_choice") {
    const select = document.createElement("select");
    select.style.width = "260px";
    param.options.forEach((opt) => {
      const optEl = document.createElement("option");
      optEl.value = opt.name;
      optEl.textContent = opt.description || opt.name;
      if (opt.active) optEl.selected = true;
      select.appendChild(optEl);
    });
    select.addEventListener("change", async () => {
      await apiPost("/api/param", { index: param.index, choice: select.value });
      markUnsaved();
      const refreshed = await apiGet("/api/params");
      renderCategories(refreshed);
    });
    row.appendChild(select);
  } else if (param.kind === "sound_choice") {
    const select = document.createElement("select");
    select.style.width = "220px";
    param.options.forEach((opt) => {
      const optEl = document.createElement("option");
      optEl.value = opt.filename;
      optEl.textContent = opt.description || opt.filename.replace(/\.h$/, "");
      if (opt.active) optEl.selected = true;
      select.appendChild(optEl);
    });
    select.addEventListener("change", async () => {
      await apiPost("/api/param", { index: param.index, filename: select.value });
      markUnsaved();
    });

    const playButton = document.createElement("button");
    playButton.className = "play-button";
    playButton.textContent = "▶ Přehrát";
    playButton.addEventListener("click", () => {
      const player = document.getElementById("sound-player");
      player.src = `/api/sound/${select.value}`;
      player.play();
    });

    row.appendChild(select);
    row.appendChild(playButton);
  }

  if (param.tierKey !== undefined) {
    row.appendChild(
      makeTierDots(param.tierKey, async () => {
        await refreshCurrentView();
      })
    );
    const noteInput = makeNoteInput("param", param.tierKey, param.note);
    row.appendChild(noteInput);
  }

  return row;
}

function markUnsaved() {
  document.getElementById("save-status").textContent = "Neuložené změny";
}

function setupBottomBar() {
  document.getElementById("save-button").addEventListener("click", async () => {
    await apiPost("/api/save");
    document.getElementById("save-status").textContent = "Uloženo";
    setTimeout(() => { document.getElementById("save-status").textContent = ""; }, 2000);
  });

  document.getElementById("upload-button").addEventListener("click", async () => {
    await apiPost("/api/save");
    const logPanel = document.getElementById("upload-log");
    const logContent = document.getElementById("upload-log-content");
    logContent.textContent = "";
    logPanel.classList.remove("hidden");

    const { jobId } = await apiPost("/api/upload");
    uploadJobId = jobId;
    let since = 0;
    if (uploadPollTimer) clearInterval(uploadPollTimer);
    uploadPollTimer = setInterval(async () => {
      const poll = await apiGet(`/api/job/${uploadJobId}?since=${since}`);
      since = poll.total;
      if (poll.lines.length) {
        logContent.textContent += poll.lines.join("\n") + "\n";
        logContent.scrollTop = logContent.scrollHeight;
      }
      if (poll.status !== "running") {
        clearInterval(uploadPollTimer);
      }
    }, 800);
  });
}

function setupMonitorOverlay() {
  const overlay = document.getElementById("monitor-overlay");
  const logContent = document.getElementById("monitor-log-content");

  document.getElementById("monitor-button").addEventListener("click", async () => {
    overlay.classList.remove("hidden");
    logContent.textContent = "";
    const { jobId } = await apiPost("/api/monitor/start");
    monitorJobId = jobId;
    let since = 0;
    if (monitorPollTimer) clearInterval(monitorPollTimer);
    monitorPollTimer = setInterval(async () => {
      const poll = await apiGet(`/api/job/${monitorJobId}?since=${since}`);
      since = poll.total;
      if (poll.lines.length) {
        logContent.textContent += poll.lines.join("\n") + "\n";
        logContent.scrollTop = logContent.scrollHeight;
      }
      if (poll.status !== "running") {
        clearInterval(monitorPollTimer);
      }
    }, 500);
  });

  document.getElementById("monitor-close").addEventListener("click", async () => {
    if (monitorPollTimer) clearInterval(monitorPollTimer);
    if (monitorJobId) {
      await apiPost("/api/monitor/stop", { jobId: monitorJobId });
    }
    overlay.classList.add("hidden");
  });
}

init();
