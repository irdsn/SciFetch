// pages/index.tsx

import React, { useState } from "react";
import Head from "next/head";
import InputForm from "../components/InputForm";
import MarkdownViewer from "../components/MarkdownViewer";
import Footer from "../components/Footer";

export default function Home() {
  const [prompt, setPrompt] = useState("");
  const [apiKey, setApiKey] = useState("");
  const [markdown, setMarkdown] = useState("");
  const [downloadUrl, setDownloadUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Handles the submission of the form
  const handleRunAgent = async () => {
    setLoading(true);
    setError("");
    setMarkdown("");
    setDownloadUrl("");

    try {
      const response = await fetch("http://localhost:8000/run", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          prompt: prompt,
          api_key: apiKey
        })
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }

      const data = await response.json();
      setMarkdown(data.content);
      setDownloadUrl(data.download_url);
    } catch (err) {
      console.error(err);
      setError("❌ Failed to fetch results. Please check your API key and try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Head>
        <title>SciFetch</title>
        <meta name="description" content="Autonomous scientific research agent using LangChain & OpenAI" />
      </Head>
      <main style={{ maxWidth: "800px", margin: "0 auto", padding: "2rem" }}>
        <h1 style={{ textAlign: "center", fontSize: "3.5rem", fontWeight: "bold", marginBottom: "2rem" }}>
          SciFetch
        </h1>

        <p className="text-gray-700 max-w-2xl mb-6">
          SciFetch is an autonomous LangChain-based agent designed to search, summarize, and store scientific literature based on user-provided prompts. It intelligently selects the best academic APIs for each topic, provides a synthesized summary, and outputs results in Markdown.
        </p>

        <InputForm
          prompt={prompt}
          setPrompt={setPrompt}
          apiKey={apiKey}
          setApiKey={setApiKey}
          onSubmit={handleRunAgent}
        />
        {loading && <p>⏳ Running agent...</p>}
        {error && <p style={{ color: "red" }}>{error}</p>}
        {markdown && (
          <>
            <MarkdownViewer content={markdown} />
            {downloadUrl && (
              <div style={{ textAlign: "center", marginTop: "1.5rem" }}>
                <a
                  href={downloadUrl}
                  download
                  style={{
                    display: "inline-block",
                    fontSize: "2rem",
                    padding: "0.5rem 1rem",
                    backgroundColor: "#0070f3",
                    color: "white",
                    textDecoration: "none",
                    borderRadius: "4px"
                  }}
                >
                  💾 Download Report
                </a>
              </div>
            )}
          </>
        )}
        <Footer />
      </main>
    </>
  );
}
