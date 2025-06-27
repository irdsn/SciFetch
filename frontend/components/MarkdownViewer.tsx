// frontend/components/MarkdownViewer.tsx

import React from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface MarkdownViewerProps {
  content: string;
  filename?: string;
  downloadUrl?: string;
}

export default function MarkdownViewer({
  content,
  filename,
  downloadUrl,
}: MarkdownViewerProps) {
  if (!content) return null;

  return (
    <div className="w-full max-w-4xl mx-auto mt-8 bg-white p-6 rounded-lg shadow-md">
      <h2 style={{ fontSize: "2.5rem", fontWeight: "bold", textAlign: "left", marginBottom: "1rem" }}>
        Report
      </h2>

      {downloadUrl && (
        <div className="flex justify-center mb-4">
          <a
            href={downloadUrl}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
            download={filename}
          >
            Download Report
          </a>
        </div>
      )}
      <hr className="mb-4" />
      <div className="prose max-w-none">
        <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
      </div>
    </div>
  );
}
