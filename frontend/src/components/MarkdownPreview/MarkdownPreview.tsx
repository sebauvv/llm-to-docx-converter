import React from 'react';
import { renderMarkdown } from '../../services/markdown';

interface MarkdownPreviewProps {
  content: string;
  previewRef: React.RefObject<HTMLDivElement | null>;
  darkMode: boolean;
}

export const MarkdownPreview: React.FC<MarkdownPreviewProps> = ({
  content,
  previewRef,
  darkMode
}) => {
  return (
    <div className={`backdrop-blur-lg rounded-lg shadow-xl border p-6 ${
      darkMode 
        ? 'bg-white/10 border-white/20' 
        : 'bg-white border-gray-200'
    }`}>
      <h2 className={`text-xl font-semibold mb-4 ${darkMode ? 'text-white' : 'text-gray-900'}`}>
        Preview
      </h2>
      <div
        ref={previewRef}
        className={`w-full h-[610px] rounded-lg p-6 overflow-auto prose prose-sm text-sm max-w-none ${
          darkMode 
            ? 'bg-white prose-slate' 
            : 'bg-gray-50 prose-slate border border-gray-200'
        }`}
        dangerouslySetInnerHTML={{ __html: renderMarkdown(content) }}
      />
    </div>
  );
};
