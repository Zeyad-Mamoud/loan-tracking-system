// // src/pages/Home.js
// import React from 'react';
// import { useAppContext } from '../context/AppContext';
// import ContactForm from '../components/ContactForm';
// import LoanForm from '../components/LoanForm';
// import ContactList from '../components/ContactList';
// import LoanList from '../components/LoanList';
// import Filters from '../components/Filters';
// import './Home.css';

// const Home = () => {
//   const {
//     contacts,
//     loans,
//     loading,
//     addContact,
//     addLoan,
//     markLoanAsPaid,
//     makePartialPayment,
//     fetchData
//   } = useAppContext();

//   return (
//     <div className="home-container">
//       <header className="app-header">
//         <h1>Loan Tracking System</h1>
//       </header>

//       <main className="main-content">
//         <section className="forms-section">
//           <ContactForm onSubmit={addContact} />
//           <LoanForm contacts={contacts} onSubmit={addLoan} />
//         </section>

//         <section className="filters-section">
//           <Filters />
//         </section>

//         <section className="data-section">
//           <ContactList contacts={contacts} loading={loading} />
//           <LoanList 
//             loans={loans} 
//             loading={loading}
//             onMarkAsPaid={markLoanAsPaid}
//             onPartialPayment={makePartialPayment}
//             onRefresh={fetchData}
//           />
//         </section>
//       </main>
//     </div>
//   );
// };

// export default Home;