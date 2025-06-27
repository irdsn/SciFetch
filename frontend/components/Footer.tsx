// frontend/components/Footer.tsx

import React from "react";

export default function Footer() {
  return (
    <footer className="w-full text-center py-6 text-sm text-gray-500 border-t mt-10 space-y-2">
      <p>
        Developed by: Íñigo Rodríguez, AI & Data Engineer.
      </p>
      <p>
        GitHub: {" "}
        <a
          href="https://github.com/irdsn"
          className="text-blue-600 hover:underline"
          target="_blank"
          rel="noopener noreferrer"
        >
          @irdsn
        </a>
      </p>
      <p>
        Powered by LangChain, FastAPI, Python & Next.js · Using OpenAI Models
      </p>
      <p>
        Integrated with APIs from arXiv, CrossRef, EuropePMC, OpenAlex & PubMed
      </p>
      <p>
        For more information, visit the project repository{" "}
        <a
          href="https://github.com/irdsn/SciFetch"
          className="text-blue-600 hover:underline"
          target="_blank"
          rel="noopener noreferrer"
        >
          here
        </a>
        .
      </p>
    </footer>
  );
}
