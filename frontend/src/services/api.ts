import type { ConversionResponse, OutputFormat } from '../types';

const API_URL = import.meta.env.VITE_API_URL;

export const convertMarkdown = async (
  content: string,
  outputFormat: OutputFormat
): Promise<ConversionResponse> => {
  const response = await fetch(API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      content,
      output_format: outputFormat,
    }),
  });

  return response.json();
};
