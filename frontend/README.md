# LLM Chat to DOCX Converter web page



1. **Install dependencies:**
```bash
npm install
```

2. **Run in development mode:**
```bash
npm run dev
```

3. **Build for production (VITE env already included):**
```bash
npm run build
```

## Project Structure

```
├── eslint.config.js
├── index.html
├── package.json
├── package-lock.json
├── public
│   └── icon.webp
├── README.md
├── src
│   ├── App.tsx
│   ├── components
│   │   ├── ConversionControls
│   │   │   └── ConversionControls.tsx
│   │   ├── Header
│   │   │   └── Header.tsx
│   │   ├── MarkdownEditor
│   │   │   └── MarkdownEditor.tsx
│   │   └── MarkdownPreview
│   │       └── MarkdownPreview.tsx
│   ├── hooks
│   │   ├── useDarkMode.ts
│   │   ├── useMarkdownConverter.ts
│   │   └── useSyncScroll.ts
│   ├── index.css
│   ├── main.tsx
│   ├── services
│   │   ├── api.ts
│   │   └── markdown.ts
│   └── types
│       └── index.ts
├── tailwind.config.js
├── tsconfig.app.json
├── tsconfig.json
├── tsconfig.node.json
└── vite.config.ts

11 directories, 24 files
```