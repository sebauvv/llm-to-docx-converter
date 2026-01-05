import React from 'react';
import { FileText, Moon, Sun, Github } from 'lucide-react';

interface HeaderProps {
  darkMode: boolean;
  onToggleDarkMode: () => void;
}

export const Header: React.FC<HeaderProps> = ({ darkMode, onToggleDarkMode }) => {
  return (
    <header className="text-center mb-8 relative">
      <a
        href="https://github.com/sebauvv/llm-to-docx-converter"
        target="_blank"
        rel="noopener noreferrer"
        className={`hidden md:flex absolute top-0 right-0 p-2 rounded-lg transition-all items-center gap-2 ${
          darkMode 
            ? 'bg-slate-700 hover:bg-slate-600 text-gray-200 hover:text-white' 
            : 'bg-white hover:bg-gray-100 text-gray-700 hover:text-gray-900 shadow-md'
        }`}
        aria-label="View on GitHub"
      >
        <Github className="w-6 h-6" />
      </a>

      <div className="flex items-center justify-center gap-3 mb-2">
        <FileText className={`w-10 h-10 ${darkMode ? 'text-blue-400' : 'text-blue-600'}`} />
        <h1 className={`text-4xl font-bold ${darkMode ? 'text-white' : 'text-gray-900'}`}>
          LLM Chat to DOCX Converter
        </h1>
        <button
          onClick={onToggleDarkMode}
          className={`ml-4 p-2 rounded-lg transition-all ${
            darkMode 
              ? 'bg-slate-700 hover:bg-slate-600 text-yellow-300' 
              : 'bg-white hover:bg-gray-100 text-gray-700 shadow-md'
          }`}
          aria-label="Toggle dark mode"
        >
          {darkMode ? <Sun className="w-6 h-6" /> : <Moon className="w-6 h-6" />}
        </button>
      </div>
      <p className={darkMode ? 'text-blue-200' : 'text-gray-700'}>
        Convert ChatGPT, Claude, Gemini or Grok chat output to Word or HTML instantly
      </p>
      
      {/* GitHub button - Mobile (below subtitle) */}
      <a
        href="https://github.com/sebauvv/llm-to-docx-converter"
        target="_blank"
        rel="noopener noreferrer"
        className={`md:hidden inline-flex mt-3 p-2 px-4 rounded-lg transition-all items-center gap-2 ${
          darkMode 
            ? 'bg-slate-700 hover:bg-slate-600 text-gray-200 hover:text-white' 
            : 'bg-white hover:bg-gray-100 text-gray-700 hover:text-gray-900 shadow-md'
        }`}
        aria-label="View on GitHub"
      >
        <Github className="w-5 h-5" />
        <span className="text-sm font-medium">View on GitHub</span>
      </a>
    </header>
  );
};
