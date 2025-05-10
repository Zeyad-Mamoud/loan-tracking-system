import React, { useState } from 'react';
import { format, parseISO } from 'date-fns';
import LoanForm from './LoanForm';
import LoanFilters from './LoanFilters';
import './LoanList.css';

const LoanList = ({
  loans,
  filteredLoans,
  loading,
  error,
  sortBy,
  filterStatus,
  onSortChange,
  onFilterChange,
  onAddLoan,
  onMarkAsPaid,
  onMarkAsPartiallyPaid,
  getContactName,
}) => {
  const [partialPaymentAmount, setPartialPaymentAmount] = useState({});

  return (
    <div>
      <h2>Add Loan</h2>
      <LoanForm onSubmit={onAddLoan} loading={loading} />

      <h2>Loans</h2>
      <LoanFilters
        sortBy={sortBy}
        filterStatus={filterStatus}
        onSortChange={onSortChange}
        onFilterChange={onFilterChange}
      />

      {loading && <p className="loading">Loading...</p>}
      {error && <p className="error">{error}</p>}
      {filteredLoans.length > 0 ? (
        <table border="1">
          <thead>
            <tr>
              <th>ID</th>
              <th>Amount</th>
              <th>Due Date</th>
              <th>Loan Type</th>
              <th>Contact Name</th>
              <th>Status</th>
              <th>Remaining Balance</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredLoans.map((loan) => (
              <tr key={loan.id}>
                <td>{loan.id}</td>
                <td>{loan.amount}</td>
                <td>{format(parseISO(loan.due_date), 'MMM dd, yyyy')}</td>
                <td>{loan.loan_type}</td>
                <td>{getContactName(loan.contact_id)}</td>
                <td>{loan.status}</td>
                <td>{loan.remaining_balance}</td>
                <td>
                  {loan.status !== 'PAID' && (
                    <>
                      <button onClick={() => onMarkAsPaid(loan.id)}>Mark as Paid</button>
                      <div>
                        <input
                          type="number"
                          placeholder="Payment Amount"
                          value={partialPaymentAmount[loan.id] || ''}
                          onChange={(e) =>
                            setPartialPaymentAmount({
                              ...partialPaymentAmount,
                              [loan.id]: e.target.value,
                            })
                          }
                        />
                        <button onClick={() => onMarkAsPartiallyPaid(loan.id, partialPaymentAmount[loan.id])}>
                          Partially Pay
                        </button>
                      </div>
                    </>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No loans available.</p>
      )}
    </div>
  );
};

export default LoanList; 