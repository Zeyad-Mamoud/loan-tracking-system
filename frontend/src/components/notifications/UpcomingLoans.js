import React, { useState, useEffect } from 'react';
import { format, parseISO } from 'date-fns';
import { fetchUpcomingLoans } from '../../services/api';
import './UpcomingLoans.css';

const UpcomingLoans = () => {
    const [upcomingLoans, setUpcomingLoans] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchLoans = async () => {
            try {
                const data = await fetchUpcomingLoans();
                setUpcomingLoans(data);
                setError(null);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchLoans();
        // Refresh every 5 minutes
        const interval = setInterval(fetchLoans, 5 * 60 * 1000);
        return () => clearInterval(interval);
    }, []);

    if (loading) return <div className="upcoming-loans loading">Loading upcoming loans...</div>;
    if (error) return <div className="upcoming-loans error">Error: {error}</div>;
    if (upcomingLoans.length === 0) return null;

    return (
        <div className="upcoming-loans">
            <h3>Upcoming Loans</h3>
            <div className="upcoming-loans-list">
                {upcomingLoans.map(loan => (
                    <div key={loan.id} className="upcoming-loan-item">
                        <div className="loan-info">
                            <span className="contact-name">{loan.contact_name}</span>
                            <span className="amount">${loan.amount.toFixed(2)}</span>
                            <span className="due-date">
                                Due: {format(parseISO(loan.due_date), 'MMM dd, yyyy')}
                            </span>
                            <span className="remaining">
                                Remaining: ${loan.remaining_balance.toFixed(2)}
                            </span>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default UpcomingLoans; 