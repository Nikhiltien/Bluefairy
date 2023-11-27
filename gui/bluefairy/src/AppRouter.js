import React from 'react';
import { Routes, Route } from 'react-router-dom';
import ParentComponent from './ParentComponent';
import ProfilesPage from './components/ProfilesPage';

const AppRouter = () => {
  return (
    <Routes>
      <Route path="/" element={<ParentComponent />} />
      <Route path="/profiles" element={<ProfilesPage />} />
    </Routes>
  );
};

export default AppRouter;
