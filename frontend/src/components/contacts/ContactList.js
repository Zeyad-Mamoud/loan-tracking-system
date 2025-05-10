import React from 'react';
import ContactForm from './ContactForm';
import './ContactList.css';

const ContactList = ({ contacts, loading, error, onAddContact }) => {
    return (
        <div className="contact-list">
            <h2>Add Contact</h2>
            <ContactForm onSubmit={onAddContact} loading={loading} />

            <h2>Contacts</h2>
            {loading && <p className="loading">Loading...</p>}
            {error && <p className="error">{error}</p>}
            {contacts.length > 0 ? (
                <table className="contacts-table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Phone</th>
                            <th>Email</th>
                        </tr>
                    </thead>
                    <tbody>
                        {contacts.map((contact) => (
                            <tr key={contact.id}>
                                <td>{contact.id}</td>
                                <td>{contact.name}</td>
                                <td>{contact.phone}</td>
                                <td>{contact.email}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            ) : (
                <p className="no-contacts">No contacts available.</p>
            )}
        </div>
    );
};

export default ContactList; 