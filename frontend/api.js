// API Configuration
const API_BASE_URL = 'https://nano-test-platform1.onrender.com/api';

class NanoAPI {
    constructor() {
        this.token = localStorage.getItem('token');
        this.userType = localStorage.getItem('userType');
    }

    setToken(token) {
        this.token = token;
        localStorage.setItem('token', token);
    }

    getAuthHeader() {
        return {
            'Content-Type': 'application/json',
            ...(this.token && { 'Authorization': `Bearer ${this.token}` })
        };
    }

    async request(endpoint, method = 'GET', data = null) {
        const url = `${API_BASE_URL}${endpoint}`;
        const options = {
            method,
            headers: this.getAuthHeader(),
        };

        if (data) {
            options.body = JSON.stringify(data);
        }

        try {
            console.log(`🔵 API Call: ${method} ${url}`, {
                headers: this.getAuthHeader(),
                body: data
            });
            
            const response = await fetch(url, options);
            console.log(`🟢 API Response: ${method} ${endpoint} - Status: ${response.status}`);
            
            if (!response.ok) {
                let errorMessage = `HTTP ${response.status}`;
                try {
                    const error = await response.json();
                    errorMessage = error.message || errorMessage;
                } catch (e) {
                    const statusText = response.statusText || `HTTP ${response.status}`;
                    errorMessage = statusText;
                }
                console.error(`🔴 API Error: ${endpoint}`, errorMessage);
                throw new Error(errorMessage);
            }

            const responseData = await response.json();
            console.log(`🟢 API Data received: ${endpoint}`, responseData);
            return responseData;
        } catch (error) {
            console.error('🔴 API Fetch Error:', {
                endpoint,
                method,
                url,
                error: error.message,
                stack: error.stack
            });
            throw error;
        }
    }

    // ==================== Authentication ====================

    async teacherLogin(teacherId, password) {
        const response = await this.request('/auth/teacher-login', 'POST', {
            teacher_id: teacherId,
            password: password
        });
        
        if (response.access_token) {
            this.setToken(response.access_token);
            localStorage.setItem('userType', 'teacher');
            localStorage.setItem('userId', response.user.teacher_id);
            localStorage.setItem('user', JSON.stringify(response.user));
        }
        
        return response;
    }

    async studentLogin(email, password) {
        const response = await this.request('/auth/student-login', 'POST', {
            email: email,
            password: password
        });
        
        if (response.access_token) {
            this.setToken(response.access_token);
            localStorage.setItem('userType', 'student');
            localStorage.setItem('userId', email);
            localStorage.setItem('user', JSON.stringify(response.user));
        }
        
        return response;
    }

    // ==================== Tests ====================

    async createTest(testData) {
        return this.request('/tests', 'POST', testData);
    }

    async getTests() {
        return this.request('/tests', 'GET');
    }

    async getTest(testId) {
        return this.request(`/tests/${testId}`, 'GET');
    }

    async updateTest(testId, testData) {
        return this.request(`/tests/${testId}`, 'PUT', testData);
    }

    async deleteTest(testId) {
        return this.request(`/tests/${testId}`, 'DELETE');
    }

    // ==================== Results ====================

    async submitTest(testId, answers, markedForReview, questionStatus = {}) {
        return this.request('/results/submit', 'POST', {
            test_id: testId,
            answers: answers,
            marked_for_review: markedForReview,
            question_status: questionStatus
        });
    }

    async getResult(resultId) {
        return this.request(`/results/${resultId}`, 'GET');
    }

    async getResults() {
        // Get current student's results
        return this.request('/results', 'GET');
    }

    async getStudentResults(studentId) {
        // For backward compatibility - now calls /results
        return this.request('/results', 'GET');
    }

    async getTestResults(testId) {
        return this.request(`/tests/${testId}/results`, 'GET');
    }

    // ==================== Health ====================

    async healthCheck() {
        return this.request('/health', 'GET');
    }
}

// Create global API instance
const api = new NanoAPI();
