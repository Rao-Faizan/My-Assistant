// Canvas Particle System
var sphereRad = 140;
var radius_sp = 1;

var Debugger = function () {};
Debugger.log = function (message) {
  try { console.log(message); } catch (exception) {}
};

function canvasSupport() {
  return !!document.createElement("canvas").getContext;
}

function canvasApp() {
  if (!canvasSupport()) return;

  var theCanvas = document.getElementById("canvasOne");
  var context = theCanvas.getContext("2d");
  var displayWidth = theCanvas.width;
  var displayHeight = theCanvas.height;
  var timer, wait = 1, count = 0, numToAddEachFrame = 8;
  var particleAlpha = 1, r = 0, g = 200, b = 255;
  var rgbString = `rgba(${r},${g},${b},`;
  var fLen = 320, projCenterX = displayWidth / 2, projCenterY = displayHeight / 2;
  var zMax = fLen - 2, particleList = {}, recycleBin = {};
  var randAccelX = 0.1, randAccelY = 0.1, randAccelZ = 0.1, gravity = 0;
  var particleRad = 1.8, sphereCenterX = 0, sphereCenterY = 0, sphereCenterZ = -3 - sphereRad;
  var zeroAlphaDepth = -750, turnSpeed = 2 * Math.PI / 1200, turnAngle = 0;

  function init() {
    timer = setInterval(onTimer, 1000 / 24);
  }

  function onTimer() {
    count++;
    if (count >= wait) {
      count = 0;
      for (let i = 0; i < numToAddEachFrame; i++) {
        let theta = Math.random() * 2 * Math.PI;
        let phi = Math.acos(Math.random() * 2 - 1);
        let x0 = sphereRad * Math.sin(phi) * Math.cos(theta);
        let y0 = sphereRad * Math.sin(phi) * Math.sin(theta);
        let z0 = sphereRad * Math.cos(phi);
        let p = addParticle(x0, sphereCenterY + y0, sphereCenterZ + z0, 0.002 * x0, 0.002 * y0, 0.002 * z0);
        p.attack = 50; p.hold = 50; p.decay = 100; p.initValue = 0;
        p.holdValue = particleAlpha; p.lastValue = 0; p.stuckTime = 90 + Math.random() * 20;
        p.accelX = 0; p.accelY = gravity; p.accelZ = 0;
      }
    }

    turnAngle = (turnAngle + turnSpeed) % (2 * Math.PI);
    let sinAngle = Math.sin(turnAngle), cosAngle = Math.cos(turnAngle);
    context.fillStyle = "#000000";
    context.fillRect(0, 0, displayWidth, displayHeight);

    let p = particleList.first;
    while (p) {
      let nextParticle = p.next;
      p.age++;
      if (p.age > p.stuckTime) {
        p.velX += p.accelX + randAccelX * (Math.random() * 2 - 1);
        p.velY += p.accelY + randAccelY * (Math.random() * 2 - 1);
        p.velZ += p.accelZ + randAccelZ * (Math.random() * 2 - 1);
        p.x += p.velX; p.y += p.velY; p.z += p.velZ;
      }

      let rotX = cosAngle * p.x + sinAngle * (p.z - sphereCenterZ);
      let rotZ = -sinAngle * p.x + cosAngle * (p.z - sphereCenterZ) + sphereCenterZ;
      let m = radius_sp * fLen / (fLen - rotZ);
      p.projX = rotX * m + projCenterX;
      p.projY = p.y * m + projCenterY;

      if (p.age < p.attack + p.hold + p.decay) {
        if (p.age < p.attack) p.alpha = (p.holdValue - p.initValue) / p.attack * p.age + p.initValue;
        else if (p.age < p.attack + p.hold) p.alpha = p.holdValue;
        else p.alpha = (p.lastValue - p.holdValue) / p.decay * (p.age - p.attack - p.hold) + p.holdValue;
      } else p.dead = true;

      let outsideTest = (p.projX > displayWidth || p.projX < 0 || p.projY < 0 || p.projY > displayHeight || rotZ > zMax);
      if (outsideTest || p.dead) recycle(p);
      else {
        let depthAlphaFactor = Math.max(0, Math.min(1, 1 - rotZ / zeroAlphaDepth));
        context.fillStyle = rgbString + depthAlphaFactor * p.alpha + ")";
        context.beginPath();
        context.arc(p.projX, p.projY, m * particleRad, 0, 2 * Math.PI, false);
        context.closePath();
        context.fill();
      }
      p = nextParticle;
    }
  }

  function addParticle(x0, y0, z0, vx0, vy0, vz0) {
    let newParticle = recycleBin.first || {};
    if (recycleBin.first) {
      recycleBin.first = newParticle.next;
      if (newParticle.next) newParticle.next.prev = null;
    }
    if (!particleList.first) {
      particleList.first = newParticle;
      newParticle.prev = null; newParticle.next = null;
    } else {
      newParticle.next = particleList.first;
      particleList.first.prev = newParticle;
      particleList.first = newParticle;
      newParticle.prev = null;
    }
    newParticle.x = x0; newParticle.y = y0; newParticle.z = z0;
    newParticle.velX = vx0; newParticle.velY = vy0; newParticle.velZ = vz0;
    newParticle.age = 0; newParticle.dead = false;
    newParticle.right = Math.random() < 0.5;
    return newParticle;
  }

  function recycle(p) {
    if (particleList.first === p) {
      particleList.first = p.next;
      if (p.next) p.next.prev = null;
    } else {
      if (!p.next) p.prev.next = null;
      else { p.prev.next = p.next; p.next.prev = p.prev; }
    }
    if (!recycleBin.first) {
      recycleBin.first = p; p.prev = null; p.next = null;
    } else {
      p.next = recycleBin.first; recycleBin.first.prev = p; recycleBin.first = p; p.prev = null;
    }
  }

  window.addEventListener("load", () => {
    canvasApp();
    init();
  });

  // Chat and Eel Integration
  function safeEelCall(fnName, ...args) {
    if (typeof eel !== "undefined" && eel && typeof eel[fnName] === "function") {
      try { return eel[fnName](...args); } catch (e) { console.warn(`eel call failed: ${fnName}`, e); }
    }
    return null;
  }

  function updateTime() {
    const now = new Date();
    document.getElementById("timeDisplay").textContent = now.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", hour12: true });
  }
  setInterval(updateTime, 1000);
  updateTime();

  function appendMessage(isUser, msg) {
    if (!msg || !msg.trim()) return;
    const container = document.getElementById("chatMessages");
    const div = document.createElement("div");
    div.className = `chat-message ${isUser ? "user-message" : "jarvis-message"}`;
    div.textContent = msg;
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
  }

  if (typeof eel !== "undefined") {
    eel.expose(receiverText); function receiverText(message) { appendMessage(false, message); }
    eel.expose(senderText); function senderText(message) { appendMessage(true, message); }
    eel.expose(DisplayMessage); function DisplayMessage(message) { document.getElementById("statusLine").textContent = message; }
    eel.expose(ShowHome); function ShowHome() { document.getElementById("statusLine").textContent = "Ready"; document.getElementById("chatbox").value = ""; }
  } else {
    let tries = 0;
    const iv = setInterval(() => {
      tries++;
      if (typeof eel !== "undefined") {
        eel.expose(receiverText); eel.expose(senderText); eel.expose(DisplayMessage); eel.expose(ShowHome);
        clearInterval(iv);
      }
      if (tries > 20) clearInterval(iv);
    }, 250);
  }

  document.addEventListener("DOMContentLoaded", () => {
    const chatbox = document.getElementById("chatbox");
    const sendBtn = document.getElementById("SendBtn");
    const micBtn = document.getElementById("mic-btn");
    const status = document.getElementById("statusLine");

    sendBtn.addEventListener("click", () => {
      const msg = chatbox.value.trim();
      if (!msg) return;
      appendMessage(true, msg);
      chatbox.value = "";
      safeEelCall("allCommands", msg);
      status.textContent = "Processing...";
    });

    chatbox.addEventListener("keypress", (e) => {
      if (e.key === "Enter") { e.preventDefault(); sendBtn.click(); }
    });

    micBtn.addEventListener("click", () => {
      status.textContent = "Listening...";
      safeEelCall("allCommands");
    });

    document.getElementById("open-notepad")?.addEventListener("click", () => safeEelCall("allCommands", "open notepad"));
    document.getElementById("open-youtube")?.addEventListener("click", () => safeEelCall("allCommands", "open youtube"));
  });
}