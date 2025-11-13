// 3D Hero Animation for ActiScore Landing Page

// Scene setup
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });

const canvasContainer = document.getElementById('hero-canvas');
if (canvasContainer) {
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setClearColor(0x000000, 0);
    canvasContainer.appendChild(renderer.domElement);
    
    // Create floating brain-like structure
    const geometry = new THREE.SphereGeometry(2, 32, 32);
    const material = new THREE.MeshPhongMaterial({
        color: 0x4f46e5,
        transparent: true,
        opacity: 0.6,
        wireframe: true
    });
    
    const brain = new THREE.Mesh(geometry, material);
    scene.add(brain);
    
    // Create smaller floating spheres (neurons)
    const neurons = [];
    const neuronGeometry = new THREE.SphereGeometry(0.1, 8, 8);
    const neuronMaterial = new THREE.MeshPhongMaterial({
        color: 0x06b6d4,
        transparent: true,
        opacity: 0.8
    });
    
    for (let i = 0; i < 50; i++) {
        const neuron = new THREE.Mesh(neuronGeometry, neuronMaterial);
        neuron.position.set(
            (Math.random() - 0.5) * 20,
            (Math.random() - 0.5) * 20,
            (Math.random() - 0.5) * 20
        );
        neurons.push(neuron);
        scene.add(neuron);
    }
    
    // Create wave-like structures
    const waveGeometry = new THREE.PlaneGeometry(10, 10, 32, 32);
    const waveMaterial = new THREE.MeshPhongMaterial({
        color: 0x8b5cf6,
        transparent: true,
        opacity: 0.3,
        side: THREE.DoubleSide,
        wireframe: true
    });
    
    const waves = [];
    for (let i = 0; i < 5; i++) {
        const wave = new THREE.Mesh(waveGeometry, waveMaterial.clone());
        wave.position.set(0, i * 2 - 5, 0);
        wave.rotation.x = Math.PI / 2;
        waves.push(wave);
        scene.add(wave);
    }
    
    // Add lighting
    const ambientLight = new THREE.AmbientLight(0x404040, 0.4);
    scene.add(ambientLight);
    
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(5, 5, 5);
    scene.add(directionalLight);
    
    const pointLight = new THREE.PointLight(0x4f46e5, 1, 100);
    pointLight.position.set(0, 0, 10);
    scene.add(pointLight);
    
    // Position camera
    camera.position.z = 10;
    
    // Mouse interaction
    let mouseX = 0;
    let mouseY = 0;
    
    document.addEventListener('mousemove', (event) => {
        mouseX = (event.clientX / window.innerWidth) * 2 - 1;
        mouseY = -(event.clientY / window.innerHeight) * 2 + 1;
    });
    
    // Animation loop
    function animate() {
        requestAnimationFrame(animate);
        
        // Rotate brain
        brain.rotation.x += 0.005;
        brain.rotation.y += 0.01;
        
        // Animate neurons
        neurons.forEach((neuron, index) => {
            neuron.position.y += Math.sin(Date.now() * 0.001 + index) * 0.01;
            neuron.rotation.x += 0.02;
            neuron.rotation.y += 0.02;
        });
        
        // Animate waves
        waves.forEach((wave, index) => {
            const time = Date.now() * 0.001;
            wave.position.z = Math.sin(time + index * 0.5) * 2;
            wave.rotation.z += 0.005;
        });
        
        // Camera movement based on mouse
        camera.position.x += (mouseX * 2 - camera.position.x) * 0.05;
        camera.position.y += (mouseY * 2 - camera.position.y) * 0.05;
        camera.lookAt(scene.position);
        
        renderer.render(scene, camera);
    }
    
    // Handle window resize
    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });
    
    // Start animation
    animate();
    
    // Performance optimization - reduce animation on mobile
    if (window.innerWidth < 768) {
        // Simplified animation for mobile
        function simpleAnimate() {
            requestAnimationFrame(simpleAnimate);
            brain.rotation.y += 0.01;
            renderer.render(scene, camera);
        }
        simpleAnimate();
    }
}

// Fallback for reduced motion preference
if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    // Don't initialize complex animations
    console.log('Reduced motion preference detected - 3D animation disabled');
} else {
    // Initialize animation when page loads
    window.addEventListener('load', () => {
        setTimeout(() => {
            if (document.getElementById('hero-canvas')) {
                // Animation code is already above
            }
        }, 100);
    });
}