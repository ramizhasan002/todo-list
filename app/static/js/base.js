// ── Dropdown ───────────────────────────────────────────
function toggleDD(id) {
    var dd = document.getElementById(id);
    var isOpen = dd.classList.contains('open');
    document.querySelectorAll('.dd.open').forEach(function (d) { d.classList.remove('open'); });
    if (!isOpen) dd.classList.add('open');
}
document.addEventListener('click', function (e) {
    if (!e.target.closest('.dd')) {
        document.querySelectorAll('.dd.open').forEach(function (d) { d.classList.remove('open'); });
    }
});


// ── Flash messages ─────────────────────────────────────
setTimeout(function () {
    document.querySelectorAll('.flash').forEach(function (f) {
        f.style.transition = 'opacity 0.4s';
        f.style.opacity = '0';
        setTimeout(function () { f.remove(); }, 400);
    });
}, 3500);

// ── Description toggle ─────────────────────────────────
function toggleDesc() {
    var area = document.getElementById('desc-area');
    var btn  = document.getElementById('desc-btn');
    var open = area.classList.toggle('open');
    btn.classList.toggle('on', open);
    if (open) document.getElementById('desc-input').focus();
}

// ── Description Height ─────────────────────────────────
const descInput = document.getElementById("desc-input");

descInput.addEventListener("input", autoResize);

function autoResize() {

    descInput.style.height = "18px";

    descInput.style.height = descInput.scrollHeight + "px";
}

// ── Date / time picker ─────────────────────────────────
// No openPicker() needed — the transparent .dt-input sits directly
// on top of the clock button and receives clicks natively.

function formatDT(val) {
    if (!val) return '';
    var d    = new Date(val);
    var mo   = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    var h    = d.getHours();
    var m    = d.getMinutes().toString().padStart(2, '0');
    var ampm = h >= 12 ? 'PM' : 'AM';
    h = h % 12 || 12;
    return d.getDate() + ' ' + mo[d.getMonth()] + ', ' + h + ':' + m + ' ' + ampm;
}

var dtInput = document.getElementById('time_date');
if (dtInput) {
    dtInput.addEventListener('change', function () {
        var pill     = document.getElementById('date-pill');
        var label    = document.getElementById('date-label');
        var clockBtn = document.getElementById('clock-btn');
        if (this.value) {
            label.textContent = formatDT(this.value);
            pill.classList.add('show');
            clockBtn.classList.add('on');
        } else {
            clearDate();
        }
    });
}

function clearDate() {
    var dtInput  = document.getElementById('time_date');
    var pill     = document.getElementById('date-pill');
    var label    = document.getElementById('date-label');
    var clockBtn = document.getElementById('clock-btn');
    if (dtInput)  dtInput.value = '';
    if (pill)     pill.classList.remove('show');
    if (label)    label.textContent = '';
    if (clockBtn) clockBtn.classList.remove('on');
}

// ── Accordion ──────────────────────────────────────────
function toggleAcc() {
    var btn  = document.getElementById('acc-btn');
    var body = document.getElementById('acc-body');
    if (btn && body) {
        btn.classList.toggle('open');
        body.classList.toggle('open');
    }
}

// Open accordion automatically after redirect
window.addEventListener("DOMContentLoaded", function () {
    const params = new URLSearchParams(window.location.search);

    if (params.get("section") === "completed") {

        var btn  = document.getElementById('acc-btn');
        var body = document.getElementById('acc-body');

        if (btn && body) {
            btn.classList.add('open');
            body.classList.add('open');
        }
    }
});


