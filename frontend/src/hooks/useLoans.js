import { useState, useCallback } from 'react';
import { fetchLoans, createLoan, updateLoanStatus } from '../services/api';

export const useLoans = () => {
    const [loans, setLoans] = useState([]);
    const [filteredLoans, setFilteredLoans] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [sortBy, setSortBy] = useState('due_date');
    const [filterStatus, setFilterStatus] = useState('');

    const loadLoans = useCallback(async () => {
        setLoading(true);
        setError(null);
        try {
            const data = await fetchLoans();
            setLoans(data);
            applyFiltersAndSort(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }, []);

    const addLoan = useCallback(async (loanData) => {
        setLoading(true);
        setError(null);
        try {
            const newLoan = await createLoan(loanData);
            setLoans(prev => {
                const updated = [...prev, newLoan];
                applyFiltersAndSort(updated);
                return updated;
            });
            return newLoan;
        } catch (err) {
            setError(err.message);
            throw err;
        } finally {
            setLoading(false);
        }
    }, []);

    const markAsPaid = useCallback(async (loanId) => {
        setLoading(true);
        setError(null);
        try {
            await updateLoanStatus(loanId, 'PAID');
            await loadLoans();
        } catch (err) {
            setError(err.message);
            throw err;
        } finally {
            setLoading(false);
        }
    }, [loadLoans]);

    const markAsPartiallyPaid = useCallback(async (loanId, paymentAmount) => {
        setLoading(true);
        setError(null);
        try {
            await updateLoanStatus(loanId, 'PARTIALLY_PAID', paymentAmount);
            await loadLoans();
        } catch (err) {
            setError(err.message);
            throw err;
        } finally {
            setLoading(false);
        }
    }, [loadLoans]);

    const applyFiltersAndSort = useCallback((loansData) => {
        let updatedLoans = [...loansData];
        if (filterStatus) {
            updatedLoans = updatedLoans.filter((loan) => loan.status === filterStatus);
        }
        updatedLoans.sort((a, b) => {
            if (sortBy === 'due_date') {
                return new Date(a.due_date) - new Date(b.due_date);
            } else if (sortBy === 'status') {
                return a.status.localeCompare(b.status);
            } else if (sortBy === 'amount') {
                return a.amount - b.amount;
            }
            return 0;
        });
        setFilteredLoans(updatedLoans);
    }, [sortBy, filterStatus]);

    return {
        loans,
        filteredLoans,
        loading,
        error,
        sortBy,
        filterStatus,
        setSortBy,
        setFilterStatus,
        loadLoans,
        addLoan,
        markAsPaid,
        markAsPartiallyPaid,
        applyFiltersAndSort,
    };
}; 