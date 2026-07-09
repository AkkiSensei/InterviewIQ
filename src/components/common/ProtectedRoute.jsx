import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useInterview } from '../../context/InterviewContext';

export default function ProtectedRoute({ children }) {
  const { isAuthenticated } = useInterview();
  const location = useLocation();

  if (!isAuthenticated) {
    // Redirect to login, but save the current location they were trying to access
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return children;
}
