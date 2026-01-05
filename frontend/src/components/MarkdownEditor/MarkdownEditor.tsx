import React from 'react';

interface MarkdownEditorProps {
  value: string;
  onChange: (value: string) => void;
  onScroll: () => void;
  textareaRef: React.RefObject<HTMLTextAreaElement | null>;
  darkMode: boolean;
}

export const MarkdownEditor: React.FC<MarkdownEditorProps> = ({
  value,
  onChange,
  onScroll,
  textareaRef,
  darkMode
}) => {
  return (
    <div className={`backdrop-blur-lg rounded-lg shadow-xl border p-6 ${
      darkMode 
        ? 'bg-white/10 border-white/20' 
        : 'bg-white border-gray-200'
    }`}>
      <h2 className={`text-xl font-semibold mb-4 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
        Markdown Input
      </h2>
      <textarea
        ref={textareaRef}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onScroll={onScroll}
        className={`w-full h-[610px] rounded-lg p-4 font-mono text-sm resize-none focus:outline-none focus:ring-2 border transition-colors ${
          darkMode
            ? 'bg-slate-800/50 text-white focus:ring-blue-500 border-white/10'
            : 'bg-gray-50 text-gray-900 focus:ring-blue-500 border-gray-300'
        }`}
        placeholder="Enter your Markdown here..."
      />
    </div>
  );
};
