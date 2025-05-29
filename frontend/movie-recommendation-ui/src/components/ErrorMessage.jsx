import React from 'react';

const ErrorMessage = ({ message }) => {
  return (
    <div className="bg-red-900/30 border border-red-700 text-red-100 px-4 py-3 rounded-md my-4">
      <div className="flex items-center">
        <svg className="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
        </svg>
        <p>{message || 'Something went wrong. Please try again later.'}</p>
      </div>
    </div>
  );
};

export default ErrorMessage; 