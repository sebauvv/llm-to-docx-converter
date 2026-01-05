export interface ConversionResponse {
  success: boolean;
  data: {
    download_url?: string;
    html?: string;
    output_format: string;
    size_bytes: number;
    expires_in?: number;
  };
  timestamp: string;
  message: string;
}

export type OutputFormat = 'docx' | 'html';
