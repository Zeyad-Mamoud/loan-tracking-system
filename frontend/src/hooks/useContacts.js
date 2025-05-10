import { useState, useCallback } from 'react';
import { fetchContacts, createContact } from '../services/api';

export const useContacts = () => {
    const [contacts, setContacts] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const loadContacts = useCallback(async () => {
        setLoading(true);
        setError(null);
        try {
            const data = await fetchContacts();
            setContacts(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }, []);

    const addContact = useCallback(async (contactData) => {
        setLoading(true);
        setError(null);
        try {
            const newContact = await createContact(contactData);
            setContacts(prev => [...prev, newContact]);
            return newContact;
        } catch (err) {
            setError(err.message);
            throw err;
        } finally {
            setLoading(false);
        }
    }, []);

    const getContactName = useCallback((contactId) => {
        const contact = contacts.find(c => c.id === contactId);
        return contact ? contact.name : 'Unknown';
    }, [contacts]);

    return {
        contacts,
        loading,
        error,
        loadContacts,
        addContact,
        getContactName,
    };
}; 