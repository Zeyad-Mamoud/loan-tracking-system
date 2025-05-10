const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://20.164.51.143:8000';

const headers = {
    'Content-Type': 'application/json',
    'ngrok-skip-browser-warning': 'true',

};

export const fetchContacts = async () => {
    const response = await fetch(`${BACKEND_URL}/contacts/`, { headers });
    if (!response.ok) {
        const text = await response.text();
        try {
            const errorData = JSON.parse(text);
            throw new Error(errorData.detail || 'Failed to fetch contacts');
        } catch {
            throw new Error('Invalid response format: ' + text.substring(0, 100));
        }
    }
    return response.json();
};

export const createContact = async (contactData) => {
    const response = await fetch(`${BACKEND_URL}/contacts/`, {
        method: 'POST',
        headers,
        body: JSON.stringify(contactData),
    });
    if (!response.ok) {
        const text = await response.text();
        try {
            const errorData = JSON.parse(text);
            throw new Error(errorData.detail || 'Failed to create contact');
        } catch {
            throw new Error('Invalid response format: ' + text.substring(0, 100));
        }
    }
    return response.json();
};

export const fetchLoans = async () => {
    const response = await fetch(`${BACKEND_URL}/loans/`, { headers });
    if (!response.ok) {
        const text = await response.text();
        try {
            const errorData = JSON.parse(text);
            throw new Error(errorData.detail || 'Failed to fetch loans');
        } catch {
            throw new Error('Invalid response format: ' + text.substring(0, 100));
        }
    }
    return response.json();
};

export const createLoan = async (loanData) => {
    const response = await fetch(`${BACKEND_URL}/loans/`, {
        method: 'POST',
        headers,
        body: JSON.stringify(loanData),
    });
    if (!response.ok) {
        const text = await response.text();
        try {
            const errorData = JSON.parse(text);
            throw new Error(errorData.detail || 'Failed to create loan');
        } catch {
            throw new Error('Invalid response format: ' + text.substring(0, 100));
        }
    }
    return response.json();
};

export const updateLoanStatus = async (loanId, status, paymentAmount = null) => {
    const response = await fetch(`${BACKEND_URL}/loans/${loanId}`, {
        method: 'PATCH',
        headers,
        body: JSON.stringify({ status, payment_amount: paymentAmount }),
    });
    if (!response.ok) {
        const text = await response.text();
        try {
            const errorData = JSON.parse(text);
            throw new Error(errorData.detail || 'Failed to update loan');
        } catch {
            throw new Error('Invalid response format: ' + text.substring(0, 100));
        }
    }
    return response.json();
};

export const fetchUpcomingLoans = async () => {
    try {
        console.log('Fetching upcoming loans from:', `${BACKEND_URL}/loans/upcoming`);
        const response = await fetch(`${BACKEND_URL}/loans/upcoming`, {
            headers,
            credentials: 'include'
        });

        if (!response.ok) {
            const text = await response.text();
            console.error('Error response:', text);
            try {
                const errorData = JSON.parse(text);
                throw new Error(errorData.detail || 'Failed to fetch upcoming loans');
            } catch {
                throw new Error('Invalid response format: ' + text.substring(0, 100));
            }
        }

        const data = await response.json();
        console.log('Received upcoming loans:', data);
        return data;
    } catch (error) {
        console.error('Error in fetchUpcomingLoans:', error);
        throw error;
    }
}; 