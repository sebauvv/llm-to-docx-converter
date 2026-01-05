import React, { useState } from 'react';
import { Header } from './components/Header/Header';
import { MarkdownEditor } from './components/MarkdownEditor/MarkdownEditor';
import { MarkdownPreview } from './components/MarkdownPreview/MarkdownPreview';
import { ConversionControls } from './components/ConversionControls/ConversionControls';
import { useDarkMode } from './hooks/useDarkMode';
import { useSyncScroll } from './hooks/useSyncScroll';
import { useMarkdownConverter } from './hooks/useMarkdownConverter';
import type { OutputFormat } from './types';

const App: React.FC = () => {
  const [markdown, setMarkdown] = useState('# Hello World\n\nThis is **bold** and *italic*.');
  const [outputFormat, setOutputFormat] = useState<OutputFormat>('docx');

  const { darkMode, setDarkMode } = useDarkMode(true);
  const { textareaRef, previewRef, handleScroll } = useSyncScroll();
  const { isConverting, copySuccess, handleDownload, handleCopyForGoogleDocs } = useMarkdownConverter();

  return (
    <div className={`min-h-screen transition-colors duration-200 ${
      darkMode 
        ? 'bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900' 
        : 'bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50'
    }`}>
      <div className="container mx-auto px-4 py-8">
        <Header 
          darkMode={darkMode} 
          onToggleDarkMode={() => setDarkMode(!darkMode)} 
        />

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          <MarkdownEditor
            value={markdown}
            onChange={setMarkdown}
            onScroll={() => handleScroll('textarea')}
            textareaRef={textareaRef}
            darkMode={darkMode}
          />

          <MarkdownPreview
            content={markdown}
            previewRef={previewRef}
            darkMode={darkMode}
          />
        </div>

        <ConversionControls
          outputFormat={outputFormat}
          onOutputFormatChange={setOutputFormat}
          onDownload={() => handleDownload(markdown, outputFormat)}
          onCopyForDocs={() => handleCopyForGoogleDocs(markdown)}
          isConverting={isConverting}
          copySuccess={copySuccess}
          disabled={!markdown.trim()}
          darkMode={darkMode}
        />
      </div>
    </div>
  );
};

export default App;