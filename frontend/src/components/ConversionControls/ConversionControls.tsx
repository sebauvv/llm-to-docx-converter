import React from 'react';
import { Copy, Download, Loader2 } from 'lucide-react';
import type { OutputFormat } from '../../types';

interface ConversionControlsProps {
  outputFormat: OutputFormat;
  onOutputFormatChange: (format: OutputFormat) => void;
  onDownload: () => void;
  onCopyForDocs: () => void;
  isConverting: boolean;
  copySuccess: boolean;
  disabled: boolean;
  darkMode: boolean;
}

export const ConversionControls: React.FC<ConversionControlsProps> = ({
  outputFormat,
  onOutputFormatChange,
  onDownload,
  onCopyForDocs,
  isConverting,
  copySuccess,
  disabled,
  darkMode
}) => {
  return (
    <div className={`backdrop-blur-lg rounded-lg shadow-xl border p-6 ${
      darkMode 
        ? 'bg-white/10 border-white/20' 
        : 'bg-white border-gray-200'
    }`}>
      <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-4">
          <label className={`font-medium ${darkMode ? 'text-white' : 'text-gray-900'}`}>
            Output Format:
          </label>
          <div className="flex gap-2">
            <button
              onClick={() => onOutputFormatChange('docx')}
              className={`px-4 py-2 rounded-lg font-medium transition-all ${
                outputFormat === 'docx'
                  ? darkMode
                    ? 'bg-blue-600 text-white shadow-lg'
                    : 'bg-blue-500 text-white shadow-lg'
                  : darkMode
                    ? 'bg-slate-700/50 text-blue-200 hover:bg-slate-700'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              Word (DOCX)
            </button>
            <button
              onClick={() => onOutputFormatChange('html')}
              className={`px-4 py-2 rounded-lg font-medium transition-all ${
                outputFormat === 'html'
                  ? darkMode
                    ? 'bg-blue-600 text-white shadow-lg'
                    : 'bg-blue-500 text-white shadow-lg'
                  : darkMode
                    ? 'bg-slate-700/50 text-blue-200 hover:bg-slate-700'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              HTML
            </button>
          </div>
        </div>

        <div className="flex gap-3">
          <button
            onClick={onCopyForDocs}
            disabled={disabled}
            className={`flex items-center gap-2 px-6 py-3 rounded-lg font-medium transition-all shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed ${
              darkMode
                ? 'bg-cyan-600 text-white hover:bg-cyan-700'
                : 'bg-cyan-500 text-white hover:bg-cyan-600'
            }`}
          >
            <Copy className="w-5 h-5" />
            {copySuccess ? 'Copied!' : 'Copy for Docs'}
          </button>

          <button
            onClick={onDownload}
            disabled={isConverting || disabled}
            className={`flex items-center gap-2 px-6 py-3 rounded-lg font-medium transition-all shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed ${
              darkMode
                ? 'bg-blue-700 text-white hover:bg-blue-800'
                : 'bg-blue-600 text-white hover:bg-blue-700'
            }`}
          >
            {isConverting ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              <Download className="w-5 h-5" />
            )}
            Download {outputFormat.toUpperCase()}
          </button>
        </div>
      </div>
    </div>
  );
};
