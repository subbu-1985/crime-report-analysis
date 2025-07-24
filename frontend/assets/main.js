// Map initialization
const map = L.map('map').setView([15.9129, 79.7400], 7);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

let currentMarkers = [];

// Load district data
async function loadDistrictData() {
    try {
        const response = await fetch('data/ap_districts.json');
        return await response.json();
    } catch (error) {
        console.error('Error loading district data:', error);
        return { districts: [] };
    }
}

// Initialize the application
async function initializeApp() {
    const districtData = await loadDistrictData();
    const districtSelect = document.getElementById('district-select');
    
    // Add markers for all districts
    districtData.districts.forEach(district => {
        // Create option for dropdown
        const option = document.createElement('option');
        option.value = district.name;
        option.textContent = district.name;
        districtSelect.appendChild(option);

        // Add marker to map
        const crimeLevel = district.crime_rate > 25 ? 'high' : district.crime_rate > 20 ? 'medium' : 'low';
        const markerColor = crimeLevel === 'high' ? 'red' : crimeLevel === 'medium' ? 'orange' : 'green';
        
        const marker = L.marker([district.lat, district.lng]).addTo(map)
            .bindPopup(`
                <div style="text-align: center;">
                    <h3>${district.name}</h3>
                    <p><strong>Crime Rate:</strong> ${district.crime_rate}/100k</p>
                    <p><strong>Hotspots:</strong> ${district.hotspots}</p>
                    <p><strong>Safety Score:</strong> ${district.safety_score}/10</p>
                </div>
            `);
        
        currentMarkers.push(marker);
    });

    // District selection handler
    districtSelect.addEventListener('change', (e) => {
        const selectedDistrict = districtData.districts.find(d => d.name === e.target.value);
        if (selectedDistrict) {
            map.setView([selectedDistrict.lat, selectedDistrict.lng], 10);
            updateDistrictStats(selectedDistrict);
        } else {
            map.setView([15.9129, 79.7400], 7);
            document.getElementById('stats-container').innerHTML = '<div class="loading">Select a district to view crime statistics</div>';
        }
    });
}

// Update district statistics
function updateDistrictStats(district) {
    const statsContainer = document.getElementById('stats-container');
    const crimeLevel = district.crime_rate > 25 ? 'high-crime' : district.crime_rate > 20 ? 'medium-crime' : 'low-crime';
    
    statsContainer.innerHTML = `
        <div class="stat-item">
            <span class="stat-label">📍 District</span>
            <span class="stat-value">${district.name}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">🔢 Crime Rate</span>
            <span class="stat-value ${crimeLevel}">${district.crime_rate}/100k</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">🚨 Hotspots</span>
            <span class="stat-value">${district.hotspots}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">🛡️ Safety Score</span>
            <span class="stat-value">${district.safety_score}/10</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">👥 Population</span>
            <span class="stat-value">${district.population.toLocaleString()}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">📅 Last Updated</span>
            <span class="stat-value">${district.last_updated}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">⚠️ Major Crimes</span>
            <span class="stat-value">${district.major_crimes.join(', ')}</span>
        </div>
    `;
}

// Chatbot functionality
const chatbotMessages = document.getElementById('chatbot-messages');
const chatbotInput = document.getElementById('chatbot-input');
const sendBtn = document.getElementById('send-btn');

function addChatMessage(sender, message, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    messageDiv.innerHTML = `<strong>${sender}:</strong> ${message}`;
    chatbotMessages.appendChild(messageDiv);
    chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
}

// Enhanced chatbot responses
const chatbotResponses = {
    greetings: [
        "Hello! I'm here to help with crime-related queries in Andhra Pradesh.",
        "Hi there! How can I assist you with AP crime information today?",
        "Welcome! I can help you with crime statistics, safety tips, and reporting procedures."
    ],
    report: [
        "🚨 To report a crime: Call 100 (Emergency) or 1077 (Women Helpline). You can also visit the nearest police station or use the AP Police app.",
        "For immediate emergencies, dial 100. For non-emergency reporting, visit your local police station with proper documentation.",
        "You can file complaints online through the AP Police portal or use the Hawk Eye app for quick reporting."
    ],
    fir: [
        "📋 For FIR status updates, you can check online at https://cctnsap.ap.gov.in or call the station where you filed the FIR.",
        "To track your FIR, use your complaint number on the AP Police website or visit the concerned police station.",
        "FIR tracking is available 24/7 through the CCTNS AP portal. You'll need your complaint number."
    ],
    safety: [
        "🛡️ Safety tips: Avoid isolated areas at night, keep emergency contacts handy, stay aware of surroundings, and trust your instincts.",
        "For personal safety: Share your location with family, avoid displaying valuables, use well-lit paths, and keep your phone charged.",
        "Safety measures include: staying in groups when possible, avoiding poorly lit areas, keeping doors locked, and being cautious with strangers."
    ],
    hotspots: [
        "🗺️ Crime hotspots are areas with higher incident rates. Check the map for current hotspot locations in your selected district.",
        "Hotspots change based on recent crime patterns. Select a district to view current high-risk areas and take extra precautions there.",
        "The dashboard shows current crime hotspots. These areas require additional vigilance and police patrolling."
    ],
    statistics: [
        "📊 Select any district from the dropdown to view detailed crime statistics, including rates, hotspots, and recent trends.",
        "Crime statistics are updated regularly. Choose a district to see crime rates per 100k population and safety scores.",
        "Our data includes crime rates, hotspot counts, major crime types, and safety scores for each district in AP."
    ]
};

function getBotResponse(message) {
    const msg = message.toLowerCase();
    
    if (msg.includes('hello') || msg.includes('hi') || msg.includes('hey')) {
        return chatbotResponses.greetings[Math.floor(Math.random() * chatbotResponses.greetings.length)];
    }
    if (msg.includes('report') || msg.includes('complaint') || msg.includes('file')) {
        return chatbotResponses.report[Math.floor(Math.random() * chatbotResponses.report.length)];
    }
    if (msg.includes('fir') || msg.includes('status') || msg.includes('track')) {
        return chatbotResponses.fir[Math.floor(Math.random() * chatbotResponses.fir.length)];
    }
    if (msg.includes('safety') || msg.includes('safe') || msg.includes('protect')) {
        return chatbotResponses.safety[Math.floor(Math.random() * chatbotResponses.safety.length)];
    }
    if (msg.includes('hotspot') || msg.includes('dangerous') || msg.includes('area')) {
        return chatbotResponses.hotspots[Math.floor(Math.random() * chatbotResponses.hotspots.length)];
    }
    if (msg.includes('stats') || msg.includes('data') || msg.includes('numbers')) {
        return chatbotResponses.statistics[Math.floor(Math.random() * chatbotResponses.statistics.length)];
    }
    
    return "I can help with crime reporting (dial 100), FIR tracking, safety tips, hotspot information, and district statistics. What would you like to know?";
}

function sendMessage() {
    const message = chatbotInput.value.trim();
    if (!message) return;
    
    addChatMessage("You", message, true);
    chatbotInput.value = '';
    
    // Show typing indicator
    setTimeout(() => {
        const response = getBotResponse(message);
        addChatMessage("AP Assistant", response);
    }, 800);
}

sendBtn.addEventListener('click', sendMessage);

chatbotInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Initialize the app
initializeApp();

// Welcome message
setTimeout(() => {
    addChatMessage("AP Assistant", "🙏 Welcome to AP Crime Analytics! I can help you with crime reporting, safety tips, FIR tracking, and district statistics. How can I assist you?");
}, 1000);