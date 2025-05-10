import React, { useState } from 'react';
import './LoanForm.css';

const LoanForm = ({ onSubmit, loading }) => {
    const [amount, setAmount] = useState('');
    const [dueDate, setDueDate] = useState('');
    const [loanType, setLoanType] = useState('BORROWED');
    const [contactId, setContactId] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit({
            amount: parseFloat(amount),
            due_date: dueDate,
            loan_type: loanType,
            contact_id: parseInt(contactId),
        });
        setAmount('');
        setDueDate('');
        setLoanType('BORROWED');
        setContactId('');
    };

    return (
        <form onSubmit={handleSubmit}>
            <div>
                <label>Amount:</label>
                <input
                    type="number"
                    value={amount}
                    onChange={(e) => setAmount(e.target.value)}
                    required
                />
            </div>
            <div>
                <label>Due Date:</label>
                <input
                    type="date"
                    value={dueDate}
                    onChange={(e) => setDueDate(e.target.value)}
                    required
                />
            </div>
            <div>
                <label>Loan Type:</label>
                <select value={loanType} onChange={(e) => setLoanType(e.target.value)}>
                    <option value="BORROWED">Borrowed</option>
                    <option value="LENT">Lent</option>
                </select>
            </div>
            <div>
                <label>Contact ID:</label>
                <input
                    type="number"
                    value={contactId}
                    onChange={(e) => setContactId(e.target.value)}
                    required
                />
            </div>
            <button type="submit" disabled={loading}>Add Loan</button>
        </form>
    );
};

export default LoanForm; 