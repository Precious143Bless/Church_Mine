// Additional JavaScript helpers and utilities

// Show notification (can be enhanced with toast notifications)
function showNotification(message, type = 'info') {
    // Simple alert for now, can be replaced with Bootstrap toast
    alert(message);
}

// Validate email format
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Validate phone number (Philippine format)
function validatePhone(phone) {
    const re = /^(09|\+639)\d{9}$/;
    return re.test(phone);
}

// Get current date in YYYY-MM-DD format
function getCurrentDate() {
    return new Date().toISOString().split('T')[0];
}

// Calculate age from birth date
function calculateAge(birthDate) {
    const today = new Date();
    const birth = new Date(birthDate);
    let age = today.getFullYear() - birth.getFullYear();
    const m = today.getMonth() - birth.getMonth();
    if (m < 0 || (m === 0 && today.getDate() < birth.getDate())) {
        age--;
    }
    return age;
}

// Export to CSV
function exportToCSV(data, filename) {
    const csv = data.map(row => Object.values(row).join(',')).join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${filename}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
}

// Debounce function for search inputs
function debounce(func, delay) {
    let timeoutId;
    return function (...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(this, args), delay);
    };
}

// Local storage helper
const storage = {
    set: (key, value) => {
        localStorage.setItem(key, JSON.stringify(value));
    },
    get: (key) => {
        const value = localStorage.getItem(key);
        return value ? JSON.parse(value) : null;
    },
    remove: (key) => {
        localStorage.removeItem(key);
    },
    clear: () => {
        localStorage.clear();
    }
};

// Session management
const session = {
    setUser: (user) => storage.set('user', user),
    getUser: () => storage.get('user'),
    setToken: (token) => storage.set('auth_token', token),
    getToken: () => storage.get('auth_token'),
    clear: () => {
        storage.remove('user');
        storage.remove('auth_token');
        storage.remove('currentPage');
    },
    isAuthenticated: () => !!storage.get('auth_token')
};

// Initialize page when loaded
document.addEventListener('DOMContentLoaded', () => {
    // Add any global initialization here
    console.log('Church Registry System initialized');
});