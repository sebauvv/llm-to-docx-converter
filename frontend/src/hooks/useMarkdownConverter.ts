import { useState } from 'react';
import { convertMarkdown } from '../services/api';
import type { OutputFormat } from '../types';

export const useMarkdownConverter = () => {
  const [isConverting, setIsConverting] = useState(false);
  const [copySuccess, setCopySuccess] = useState(false);

  const handleDownload = async (markdown: string, outputFormat: OutputFormat) => {
    if (!markdown.trim()) return;

    setIsConverting(true);
    try {
      const data = await convertMarkdown(markdown, outputFormat);

      if (data.success) {
        if (outputFormat === 'docx' && data.data.download_url) {
          window.open(data.data.download_url, '_blank');
        } else if (outputFormat === 'html' && data.data.html) {
          const blob = new Blob([data.data.html], { type: 'text/html' });
          const url = URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = 'document.html';
          document.body.appendChild(a);
          a.click();
          document.body.removeChild(a);
          URL.revokeObjectURL(url);
        }
      }
    } catch (error) {
      console.error('Download failed:', error);
    } finally {
      setIsConverting(false);
    }
  };

  const handleCopyForGoogleDocs = async (markdown: string) => {
    if (!markdown.trim()) return;

    try {
      const data = await convertMarkdown(markdown, 'html');

      if (data.success && data.data.html) {
        const blob = new Blob([data.data.html], { type: 'text/html' });
        const clipboardItem = new ClipboardItem({
          'text/html': blob,
          'text/plain': new Blob([markdown], { type: 'text/plain' })
        });
        
        await navigator.clipboard.write([clipboardItem]);
        setCopySuccess(true);
        setTimeout(() => setCopySuccess(false), 2000);
      }
    } catch (error) {
      console.error('Copy failed:', error);
      try {
        await navigator.clipboard.writeText(markdown);
        setCopySuccess(true);
        setTimeout(() => setCopySuccess(false), 2000);
      } catch (fallbackError) {
        console.error('Fallback copy failed:', fallbackError);
      }
    }
  };

  return {
    isConverting,
    copySuccess,
    handleDownload,
    handleCopyForGoogleDocs
  };
};
