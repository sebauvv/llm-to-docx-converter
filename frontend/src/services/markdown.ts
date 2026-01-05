import MarkdownIt from 'markdown-it';
import DOMPurify from 'dompurify';

const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true
});

export const renderMarkdown = (content: string): string => {
  const rawHtml = md.render(content);
  return DOMPurify.sanitize(rawHtml);
};
