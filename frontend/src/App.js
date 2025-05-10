import React, { useEffect } from 'react';
import './App.css';
import './styles/global.css';
import ContactList from './components/contacts/ContactList';
import LoanList from './components/loans/LoanList';
import UpcomingLoans from './components/notifications/UpcomingLoans';
import { useContacts } from './hooks/useContacts';
import { useLoans } from './hooks/useLoans';

function App() {
  const {
    contacts,
    loading: contactsLoading,
    error: contactsError,
    loadContacts,
    addContact,
    getContactName,
  } = useContacts();

  const {
    loans,
    filteredLoans,
    loading: loansLoading,
    error: loansError,
    sortBy,
    filterStatus,
    setSortBy,
    setFilterStatus,
    loadLoans,
    addLoan,
    markAsPaid,
    markAsPartiallyPaid,
  } = useLoans();

  useEffect(() => {
    loadContacts();
    loadLoans();
  }, [loadContacts, loadLoans]);

  const handleRefresh = () => {
    loadContacts();
    loadLoans();
  };

  return (
    <div className="App">
      <h1>Loan Tracking System</h1>

      {(contactsLoading || loansLoading) && <p className="loading">Loading...</p>}
      {(contactsError || loansError) && <p className="error">{contactsError || loansError}</p>}

      <button onClick={handleRefresh} className="refresh-button">Refresh Data</button>

      <UpcomingLoans />

      <ContactList
        contacts={contacts}
        loading={contactsLoading}
        error={contactsError}
        onAddContact={addContact}
      />

      <LoanList
        loans={loans}
        filteredLoans={filteredLoans}
        loading={loansLoading}
        error={loansError}
        sortBy={sortBy}
        filterStatus={filterStatus}
        onSortChange={setSortBy}
        onFilterChange={setFilterStatus}
        onAddLoan={addLoan}
        onMarkAsPaid={markAsPaid}
        onMarkAsPartiallyPaid={markAsPartiallyPaid}
        getContactName={getContactName}
      />
    </div>
  );
}

export default App;