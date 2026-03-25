// 🔔 Toast Notification (unchanged)
function showToast(message) {
    const container = document.getElementById("toast-container");

    const toast = document.createElement("div");
    toast.className = "toast";
    toast.innerText = "🔔 " + message;

    container.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 5000);
}

// 🐶 Popup Queue System
let queue = [];
let isShowing = false;

// 🔊 Speak function
function speak(text) {
    window.speechSynthesis.cancel();

    const speech = new SpeechSynthesisUtterance(text);
    speech.lang = "en-US";
    speech.rate = 1;
    speech.pitch = 1;

    window.speechSynthesis.speak(speech);
}

// 🐶 3D variables
let scene, camera, renderer, puppy;

// 🐶 Init 3D puppy
function init3DPuppy() {
    const container = document.getElementById("puppy-3d");

    if (!container) return;

    // clear old canvas
    container.innerHTML = "";

    scene = new THREE.Scene();

    camera = new THREE.PerspectiveCamera(75, 1, 0.1, 1000);
    camera.position.z = 2;

    renderer = new THREE.WebGLRenderer({ alpha: true });
    renderer.setSize(150, 150);

    container.appendChild(renderer.domElement);

    // lighting
    const light = new THREE.AmbientLight(0xffffff, 1);
    scene.add(light);

    // load model
    const loader = new THREE.GLTFLoader();
    loader.load("/static/puppy.glb", function (gltf) {
        puppy = gltf.scene;
        scene.add(puppy);
        animate();
    }, undefined, function (error) {
        console.error("Error loading model:", error);
    });
}

// 🐶 Animation loop
function animate() {
    requestAnimationFrame(animate);

    if (puppy) {
        puppy.rotation.y += 0.02; // rotate
    }

    renderer.render(scene, camera);
}

// 🐶 Show popup
function showPuppyPopup(message) {
    const popup = document.getElementById("puppy-popup");
    const textBox = popup.querySelector(".puppy-text");

    textBox.innerText = "🐶 " + message;

    popup.classList.remove("hidden");

    // 🔥 load 3D puppy
    init3DPuppy();

    // 🔊 speak
    speak(message);

    setTimeout(() => {
        popup.classList.add("hidden");
    }, 6000);
}

// 🔄 Process queue
function processQueue() {
    if (queue.length === 0) {
        isShowing = false;
        return;
    }

    isShowing = true;

    const msg = queue.shift();
    showPuppyPopup(msg);

    setTimeout(processQueue, 7000);
}

// 🔄 Fetch notifications
async function fetchNotifications() {
    const response = await fetch("/get_notifications");
    const data = await response.json();

    data.forEach(n => {
        queue.push(n.name + ": " + n.message);
    });

    if (!isShowing) {
        processQueue();
    }
}

setInterval(fetchNotifications, 5000);

// 🧪 Analyze test user
async function analyze() {
    const days = document.getElementById("days").value;
    const time = document.getElementById("time").value;
    const marks = document.getElementById("marks").value;

    const response = await fetch("/dashboard", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            last_active_days: parseInt(days),
            time_spent: parseInt(time),
            marks: parseInt(marks)
        })
    });

    const data = await response.json();

    document.getElementById("result").innerText =
        "Status: " + data.status + " | Message: " + data.message;
}