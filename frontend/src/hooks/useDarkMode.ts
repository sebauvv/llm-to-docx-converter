import { useState, useEffect } from 'react';

export const useDarkMode = (initialValue = true) => {
  const [darkMode, setDarkMode] = useState(initialValue);

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [darkMode]);

  return { darkMode, setDarkMode };
};
