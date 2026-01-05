import { useRef } from 'react';

export const useSyncScroll = () => {
  const textareaRef = useRef<HTMLTextAreaElement | null>(null);
  const previewRef = useRef<HTMLDivElement | null>(null);
  const scrollTimeoutRef = useRef<number | null>(null);

  const handleScroll = (source: 'textarea' | 'preview') => {
    if (scrollTimeoutRef.current) {
      clearTimeout(scrollTimeoutRef.current);
    }

    scrollTimeoutRef.current = window.setTimeout(() => {
      if (source === 'textarea' && textareaRef.current && previewRef.current) {
        const { scrollTop, scrollHeight, clientHeight } = textareaRef.current;
        const scrollPercentage = scrollTop / (scrollHeight - clientHeight);
        previewRef.current.scrollTop = scrollPercentage * 
          (previewRef.current.scrollHeight - previewRef.current.clientHeight);
      } else if (source === 'preview' && previewRef.current && textareaRef.current) {
        const { scrollTop, scrollHeight, clientHeight } = previewRef.current;
        const scrollPercentage = scrollTop / (scrollHeight - clientHeight);
        textareaRef.current.scrollTop = scrollPercentage * 
          (textareaRef.current.scrollHeight - textareaRef.current.clientHeight);
      }
    }, 10);
  };

  return { textareaRef, previewRef, handleScroll };
};
