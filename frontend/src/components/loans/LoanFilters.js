import React from 'react';
import './LoanFilters.css';

const LoanFilters = ({ sortBy, filterStatus, onSortChange, onFilterChange }) => {
    return (
        <div className="loan-filters">
            <div className="filter-group">
                <label>Sort by:</label>
                <select value={sortBy} onChange={(e) => onSortChange(e.target.value)}>
                    <option value="due_date">Due Date</option>
                    <option value="status">Status</option>
                    <option value="amount">Amount</option>
                </select>
            </div>
            <div className="filter-group">
                <label>Filter by Status:</label>
                <select value={filterStatus} onChange={(e) => onFilterChange(e.target.value)}>
                    <option value="">All</option>
                    <option value="ACTIVE">Active</option>
                    <option value="PARTIALLY_PAID">Partially Paid</option>
                    <option value="PAID">Paid</option>
                </select>
            </div>
        </div>
    );
};

export default LoanFilters; 